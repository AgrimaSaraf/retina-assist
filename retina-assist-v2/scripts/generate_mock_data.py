from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 500
age_band = rng.choice(["0-17","18-39","40-59","60+"], n, p=[.05,.28,.38,.29])
visit_type = rng.choice(["routine","retina","glaucoma","post_op","other"], n, p=[.28,.28,.18,.16,.10])
prev = np.clip(rng.poisson(.55,n),0,5)
lead = np.clip(rng.gamma(2,10,n).round(),0,120).astype(int)
rec = rng.choice([7,14,30,60,90,180], n, p=[.08,.10,.28,.18,.24,.12])
contact = rng.binomial(1,.87,n)
eligible = rng.binomial(1,.82,n)

logit = -1.55 + .72*prev + .012*lead + .002*rec - .52*contact + .18*(age_band=="60+")
prob = 1/(1+np.exp(-logit))
missed = (rng.random(n)<prob).astype(int) * eligible
days_late = np.where(
    missed==1,
    np.clip(rng.gamma(2,15,n).round(),1,180),
    np.clip(rng.normal(2,4,n).round(),0,30)
).astype(int) * eligible

df = pd.DataFrame({
    "research_id":[f"R{i:04d}" for i in range(1,n+1)],
    "age_band":age_band,
    "visit_type":visit_type,
    "previous_missed_visits":prev,
    "lead_time_days":lead,
    "recommended_followup_days":rec,
    "contact_available":contact,
    "followup_recommended":eligible,
    "missed_followup":missed,
    "days_late":days_late,
})
Path("data").mkdir(exist_ok=True)
df.to_csv("data/mock_visits.csv", index=False)
print("Created 500 synthetic records. These are not clinic observations.")
