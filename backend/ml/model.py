from pathlib import Path
import torch
from torch import nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

CLASSES = ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"]

def build_model(num_classes: int = 5):
    # ImageNet weights initialize the feature extractor only.
    # They are NOT retinal-disease weights.
    weights = EfficientNet_B0_Weights.DEFAULT
    model = efficientnet_b0(weights=weights)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model, weights

def load_retina_model(checkpoint_path: str, device: torch.device):
    checkpoint = Path(checkpoint_path)
    if not checkpoint.exists():
        raise FileNotFoundError(
            f"RetinaAssist checkpoint not found: {checkpoint}. "
            "Train/validate a retinal model before enabling medical inference."
        )

    model, weights = build_model()
    state = torch.load(checkpoint, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.to(device).eval()
    return model, weights
