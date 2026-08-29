import pandas as pd

AGE_ORDER = ["0-17", "18-39", "40-59", "60+"]
VISIT_TYPES = ["routine", "retina", "glaucoma", "post_op", "other"]

def build_feature_frame(payload: dict) -> pd.DataFrame:
    row = {
        "previous_missed_visits": int(payload["previous_missed_visits"]),
        "lead_time_days": int(payload["lead_time_days"]),
        "recommended_followup_days": int(payload["recommended_followup_days"]),
        "contact_available": int(bool(payload["contact_available"])),
    }
    for band in AGE_ORDER:
        row[f"age_{band}"] = int(payload["age_band"] == band)
    for v in VISIT_TYPES:
        row[f"visit_{v}"] = int(payload["visit_type"] == v)
    return pd.DataFrame([row])

def feature_columns():
    return [
        "previous_missed_visits","lead_time_days",
        "recommended_followup_days","contact_available"
    ] + [f"age_{b}" for b in AGE_ORDER] + [f"visit_{v}" for v in VISIT_TYPES]
