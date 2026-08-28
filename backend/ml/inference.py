import os
import torch
from PIL import Image

from .model import CLASSES, load_retina_model
from .preprocessing import prepare_image
from .quality import assess_image_quality
from .gradcam import GradCAM, overlay_as_data_url

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CHECKPOINT = os.getenv("RETINA_MODEL_PATH", "models/retinaassist_dr.pth")

class RetinaInferenceService:
    def __init__(self):
        self.model = None
        self.weights = None
        self.ready = False
        self.error = None
        try:
            self.model, self.weights = load_retina_model(CHECKPOINT, DEVICE)
            self.ready = True
        except Exception as exc:
            self.error = str(exc)

    def status(self):
        return {
            "ready": self.ready,
            "device": str(DEVICE),
            "checkpoint": CHECKPOINT,
            "message": None if self.ready else self.error,
        }

    def analyze(self, image: Image.Image):
        if not self.ready:
            raise RuntimeError(self.error or "Retinal model is not ready.")

        tensor = prepare_image(image).to(DEVICE)
        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0]

        index = int(probabilities.argmax().item())
        confidence = float(probabilities[index].item())

        # Last convolutional feature block in torchvision EfficientNet.
        cam_engine = GradCAM(self.model, self.model.features[-1])
        cam, _ = cam_engine.generate(tensor, class_index=index)

        return {
            "prediction": CLASSES[index],
            "class_index": index,
            "confidence": round(confidence, 4),
            "probabilities": {
                label: round(float(probabilities[i].item()), 4)
                for i, label in enumerate(CLASSES)
            },
            "image_quality": assess_image_quality(image),
            "gradcam": overlay_as_data_url(image, cam),
            "disclaimer": (
                "Research prototype only. Output is not a diagnosis and must not "
                "be used for patient-care decisions."
            ),
        }

service = RetinaInferenceService()
