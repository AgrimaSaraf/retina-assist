import os, torch
from pathlib import Path
from .model import RetinaAssistNet
from .preprocessing import preprocess
LABELS=['No DR','Mild','Moderate','Severe','Proliferative DR']
class ScreeningEngine:
    def __init__(self,path=None):
        self.path=Path(path or os.getenv('RETINA_MODEL_PATH','models/retinaassist_dr.pth')); self.model=None
        self.device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if self.path.exists():
            m=RetinaAssistNet(len(LABELS)); m.load_state_dict(torch.load(self.path,map_location=self.device)); m.to(self.device).eval(); self.model=m
    @property
    def ready(self): return self.model is not None
    def analyze(self,image):
        if not self.ready: raise RuntimeError('MODEL_NOT_TRAINED')
        with torch.no_grad(): probs=torch.softmax(self.model(preprocess(image).to(self.device)),dim=1)[0].cpu().numpy()
        i=int(probs.argmax())
        return {'predicted_class':i,'label':LABELS[i],'confidence':round(float(probs[i]),4),'warning':'Research output only. Not for diagnosis.'}
