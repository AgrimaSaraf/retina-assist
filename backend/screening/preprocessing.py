from PIL import Image
from torchvision import transforms
import numpy as np

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

def preprocess(image: Image.Image):
    return transform(image.convert("RGB")).unsqueeze(0)

def engineering_quality_score(image: Image.Image):
    gray = np.asarray(image.convert("L").resize((224,224)), dtype="float32")
    return round(max(0.0, min(1.0, float(gray.std()) / 64.0)), 3)
