import pandas as pd
from analytics.hci_metrics import summarize_hci
df=pd.read_csv('data/synthetic/human_ai_study.csv'); print('SIMULATED HUMAN-AI BENCHMARK');
for k,v in summarize_hci(df).items(): print(f'{k}: {v:.4f}' if isinstance(v,float) else f'{k}: {v}')
