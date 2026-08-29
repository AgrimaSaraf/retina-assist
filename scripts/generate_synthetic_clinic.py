from pathlib import Path
from simulation.clinic_generator import generate_clinic_cohort
v,a=generate_clinic_cohort(); out=Path('data/synthetic'); out.mkdir(parents=True,exist_ok=True); v.to_csv(out/'visits.csv',index=False); a.to_csv(out/'appointments.csv',index=False)
print(f'Generated {len(v)} synthetic visits and {len(a)} synthetic appointments. Not clinic observations.')
