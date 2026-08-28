import cv2
import numpy as np
from PIL import Image

def assess_image_quality(image: Image.Image) -> dict:
    """
    Engineering quality heuristic only; not a validated clinical quality model.
    """
    rgb = np.asarray(image.convert("RGB"))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    brightness = float(gray.mean())

    sharpness_score = min(sharpness / 250.0, 1.0)
    brightness_score = max(0.0, 1.0 - abs(brightness - 115.0) / 115.0)
    score = round(10.0 * (0.65 * sharpness_score + 0.35 * brightness_score), 1)

    issues = []
    if sharpness < 50:
        issues.append("possible_blur")
    if brightness < 45:
        issues.append("underexposed")
    if brightness > 210:
        issues.append("overexposed")

    return {
        "score": score,
        "sharpness": round(sharpness, 2),
        "brightness": round(brightness, 2),
        "issues": issues,
        "validated_clinically": False,
    }
