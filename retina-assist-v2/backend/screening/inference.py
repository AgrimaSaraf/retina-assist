import os
from pathlib import Path
import torch
from .model import RetinaAssistNet
from .preprocessing import preprocess, engineering_quality_score

LABELS = ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"]

class ScreeningEngine:
    def __init__(self, checkpoint_path=None):
        self.path = Path(
            checkpoint_path or os.getenv("RETINA_MODEL_PATH", "models/retinaassist_dr.pth")
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

        if self.path.exists():
            model = RetinaAssistNet(len(LABELS))
            state = torch.load(self.path, map_location=self.device)
            model.load_state_dict(state)
            model.to(self.device).eval()
            self.model = model

    @property
    def ready(self):
        return self.model is not None

    def analyze(self, image):
        if not self.ready:
            raise RuntimeError("MODEL_NOT_TRAINED")
        x = preprocess(image).to(self.device)
        with torch.no_grad():
            probs = torch.softmax(self.model(x), dim=1)[0].cpu().numpy()
        idx = int(probs.argmax())
        return {
            "predicted_class": idx,
            "label": LABELS[idx],
            "confidence": round(float(probs[idx]), 4),
            "probabilities": {
                label: round(float(p), 4) for label, p in zip(LABELS, probs)
            },
            "engineering_quality_score": engineering_quality_score(image),
            "warning": "Research output only. Not for diagnosis or patient-care decisions.",
        }
