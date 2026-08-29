import joblib, pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from backend.followup.features import build_feature_frame, feature_columns

df=pd.read_csv("data/mock_visits.csv")
rows=[]
for r in df.to_dict("records"):
    rows.append(build_feature_frame({
        "age_band":r["age_band"],
        "previous_missed_visits":int(r["previous_missed_visits"]),
        "lead_time_days":int(r["lead_time_days"]),
        "recommended_followup_days":int(r["recommended_followup_days"]),
        "visit_type":r["visit_type"],
        "contact_available":bool(r["contact_available"]),
    }).iloc[0])

X=pd.DataFrame(rows).reindex(columns=feature_columns(),fill_value=0)
y=df.missed_followup.astype(int)
model=joblib.load("models/followup_logistic.joblib")
p=model.predict_proba(X)[:,1]

print("SYNTHETIC DATA ONLY")
print("AUROC:", round(roc_auc_score(y,p),4))
print("Average precision:", round(average_precision_score(y,p),4))
print("Brier:", round(brier_score_loss(y,p),4))
