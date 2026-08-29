import pandas as pd

df = pd.read_csv("data/mock_visits.csv")
eligible = df[df.followup_recommended == 1]
print("MOCK DATA ONLY")
print("Total visits:", len(df))
print("Eligible:", len(eligible))
print("Missed follow-up rate:", round(float(eligible.missed_followup.mean()),4))
print("Median days late:", round(float(eligible.days_late.median()),2))
