from torch import nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
class RetinaAssistNet(nn.Module):
    def __init__(self,num_classes=5):
        super().__init__(); self.net=efficientnet_b0(weights=EfficientNet_B0_Weights.IMAGENET1K_V1)
        self.net.classifier[1]=nn.Linear(self.net.classifier[1].in_features,num_classes)
    def forward(self,x): return self.net(x)
