import numpy as np, pandas as pd

def generate_clinic_cohort(n=1000,seed=42):
    r=np.random.default_rng(seed)
    age=r.choice(['0-17','18-39','40-59','60+'],n,p=[.05,.28,.38,.29]); vt=r.choice(['routine','retina','glaucoma','post_op','other'],n,p=[.28,.28,.18,.16,.10])
    prev=np.clip(r.poisson(.55,n),0,5); lead=np.clip(r.gamma(2,10,n).round(),0,120).astype(int); rec=r.choice([7,14,30,60,90,180],n,p=[.08,.10,.28,.18,.24,.12]); contact=r.binomial(1,.87,n); eligible=r.binomial(1,.82,n)
    logit=-1.55+.72*prev+.012*lead+.002*rec-.52*contact+.18*(age=='60+')+.14*(vt=='retina'); p=1/(1+np.exp(-logit)); missed=(r.random(n)<p).astype(int)*eligible
    late=np.where(missed==1,np.clip(r.gamma(2,15,n).round(),1,180),np.clip(r.normal(2,4,n).round(),0,30)).astype(int)*eligible
    visits=pd.DataFrame({'research_id':[f'SIM-R{i:05d}' for i in range(1,n+1)],'age_band':age,'visit_type':vt,'previous_missed_visits':prev,'lead_time_days':lead,'recommended_followup_days':rec,'contact_available':contact,'followup_recommended':eligible,'missed_followup':missed,'days_late':late,'synthetic':1})
    appt=visits[visits.followup_recommended==1][['research_id','recommended_followup_days','missed_followup','days_late']].copy(); appt['appointment_id']=[f'SIM-A{i:05d}' for i in range(1,len(appt)+1)]; appt['completed']=1-appt.missed_followup; appt['synthetic']=1
    return visits,appt
