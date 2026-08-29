from pathlib import Path
from simulation.human_ai_generator import generate_human_ai_study
df=generate_human_ai_study(); out=Path('data/synthetic'); out.mkdir(parents=True,exist_ok=True); df.to_csv(out/'human_ai_study.csv',index=False)
print(f'Generated {len(df)} simulated human-AI cases. Not real clinicians or patients.')
