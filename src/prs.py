import pandas as pd

df = pd.read_csv(
    "data/processed/hevy_exercises.csv"
)

prs = (
    df.groupby("exercise")["weight_kg"]
    .max()
    .sort_values(ascending=False)
)

print("\n===== PERSONAL RECORDS =====\n")

print(prs.head(20))
