import joblib,pandas as pd
from backend.followup.features import build_feature_frame,feature_columns
from analytics.followup_metrics import followup_metrics
df=pd.read_csv('data/synthetic/visits.csv'); df=df[df.followup_recommended==1]; rows=[]
for r in df.to_dict('records'): rows.append(build_feature_frame({'age_band':r['age_band'],'previous_missed_visits':int(r['previous_missed_visits']),'lead_time_days':int(r['lead_time_days']),'recommended_followup_days':int(r['recommended_followup_days']),'visit_type':r['visit_type'],'contact_available':bool(r['contact_available'])}).iloc[0])
X=pd.DataFrame(rows).reindex(columns=feature_columns(),fill_value=0); y=df.missed_followup.astype(int); m=joblib.load('models/followup_logistic.joblib'); p=m.predict_proba(X)[:,1]; print('SYNTHETIC FOLLOW-UP BENCHMARK'); [print(f'{k}: {v:.4f}') for k,v in followup_metrics(y,p).items()]
