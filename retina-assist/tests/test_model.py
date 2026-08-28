import torch
from backend.ml.model import build_model

def test_model_has_five_outputs():
    model, _ = build_model()
    model.eval()
    with torch.no_grad():
        out = model(torch.zeros(1, 3, 224, 224))
    assert out.shape == (1, 5)
