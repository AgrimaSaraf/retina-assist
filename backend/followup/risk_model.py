import os
from pathlib import Path
import joblib
import numpy as np
from .features import build_feature_frame, feature_columns

class FollowUpRiskModel:
    def __init__(self, model_path=None):
        self.model_path = Path(
            model_path or os.getenv("FOLLOWUP_MODEL_PATH", "models/followup_logistic.joblib")
        )
        self.model = joblib.load(self.model_path) if self.model_path.exists() else None

    def predict(self, payload):
        frame = build_feature_frame(payload).reindex(columns=feature_columns(), fill_value=0)

        if self.model is not None:
            probability = float(self.model.predict_proba(frame)[0, 1])
            status = "trained_model"
            note = (
                "Research model output only. Clinical validity must be established "
                "separately before any patient-care use."
            )
        else:
            score = (
                -1.35
                + 0.78 * min(payload["previous_missed_visits"], 4)
                + 0.012 * min(payload["lead_time_days"], 90)
                + 0.002 * min(payload["recommended_followup_days"], 365)
                - 0.55 * int(payload["contact_available"])
                + 0.20 * int(payload["age_band"] == "60+")
            )
            probability = float(1 / (1 + np.exp(-score)))
            status = "research_baseline"
            note = (
                "Engineering-only baseline with hand-set coefficients. "
                "Not learned from clinic data and not clinically valid."
            )

        band = "low" if probability < .30 else "medium" if probability < .60 else "high"
        return {
            "probability": round(probability, 4),
            "risk_band": band,
            "model_status": status,
            "note": note,
        }
