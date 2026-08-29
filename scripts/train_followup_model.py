from pathlib import Path
import joblib,pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from backend.followup.features import build_feature_frame,feature_columns
p=Path('data/synthetic/visits.csv')
if not p.exists(): raise SystemExit('Run python scripts/generate_synthetic_clinic.py first')
df=pd.read_csv(p); df=df[df.followup_recommended==1].copy(); rows=[]
for r in df.to_dict('records'): rows.append(build_feature_frame({'age_band':r['age_band'],'previous_missed_visits':int(r['previous_missed_visits']),'lead_time_days':int(r['lead_time_days']),'recommended_followup_days':int(r['recommended_followup_days']),'visit_type':r['visit_type'],'contact_available':bool(r['contact_available'])}).iloc[0])
X=pd.DataFrame(rows).reindex(columns=feature_columns(),fill_value=0); y=df.missed_followup.astype(int); Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y); m=LogisticRegression(max_iter=2000).fit(Xtr,ytr); prob=m.predict_proba(Xte)[:,1]; Path('models').mkdir(exist_ok=True); joblib.dump(m,'models/followup_logistic.joblib'); print('Synthetic holdout AUROC:',round(roc_auc_score(yte,prob),3)); print('Do not report as clinical performance.')
