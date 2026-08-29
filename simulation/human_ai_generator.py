import numpy as np, pandas as pd
LABELS=[0,1,2,3,4]; CONDITIONS=['no_ai','ai_prediction','ai_plus_explanation']
def generate_human_ai_study(n_cases=600,seed=7):
    r=np.random.default_rng(seed); rows=[]
    def pred(y,acc): return y if r.random()<acc else int(r.choice([x for x in LABELS if x!=y]))
    for i in range(n_cases):
        y=int(r.choice(LABELS,p=[.48,.13,.20,.11,.08])); c=str(r.choice(CONDITIONS)); ai=pred(y,.80); h=pred(y,.72); aic=int(ai==y); hic=int(h==y)
        aicf=float(np.clip(r.normal(.83 if aic else .62,.10),.35,.99)); hcf=float(np.clip(r.normal(.76 if hic else .60,.12),.25,.99)); exp=0; final=h; fcf=hcf
        if c!='no_ai':
            d=h!=ai; exp=int(c=='ai_plus_explanation' and r.random() < (.76 if d else .48)); sp=.10 if not d else .34+.22*max(aicf-hcf,0)+.10*exp
            if r.random()<min(sp,.85): final=ai
            fcf=float(np.clip(hcf+r.normal(.05 if final==h else .10,.05),.20,.99))
        t=float(np.clip(r.normal(31+8*int(c!='no_ai')+6*exp,8),8,120))
        rows.append({'case_id':f'SIM-C{i+1:05d}','condition':c,'reference_label':y,'ai_prediction':ai,'ai_confidence':round(aicf,3),'ai_correct':aic,'clinician_initial':h,'clinician_initial_confidence':round(hcf,3),'initial_correct':hic,'ai_revealed':int(c!='no_ai'),'explanation_opened':exp,'clinician_final':final,'clinician_final_confidence':round(fcf,3),'final_correct':int(final==y),'decision_switched':int(final!=h),'ai_agreement_final':int(final==ai),'decision_time_sec':round(t,1),'synthetic':1})
    return pd.DataFrame(rows)
