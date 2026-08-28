from PIL import Image
from torchvision.models import EfficientNet_B0_Weights

def get_transform():
    # Uses torchvision's preprocessing associated with EfficientNet-B0 weights.
    return EfficientNet_B0_Weights.DEFAULT.transforms()

def prepare_image(image: Image.Image):
    image = image.convert("RGB")
    return get_transform()(image).unsqueeze(0)
