import os, joblib, numpy as np
from pathlib import Path
from .features import build_feature_frame, feature_columns

class FollowUpRiskModel:
    def __init__(self, model_path=None):
        self.path=Path(model_path or os.getenv('FOLLOWUP_MODEL_PATH','models/followup_logistic.joblib'))
        self.model=joblib.load(self.path) if self.path.exists() else None
    def predict(self,payload):
        X=build_feature_frame(payload).reindex(columns=feature_columns(),fill_value=0)
        if self.model is not None:
            p=float(self.model.predict_proba(X)[0,1]); status='trained_model'; note='Research model output. Synthetic-trained models are not clinically meaningful.'
        else:
            s=-1.35+0.78*min(payload['previous_missed_visits'],4)+0.012*min(payload['lead_time_days'],90)+0.002*min(payload['recommended_followup_days'],365)-0.55*int(payload['contact_available'])
            p=float(1/(1+np.exp(-s))); status='research_baseline'; note='Engineering-only baseline with hand-set coefficients.'
        band='low' if p<.30 else 'medium' if p<.60 else 'high'
        return {'probability':round(p,4),'risk_band':band,'model_status':status,'note':note}
