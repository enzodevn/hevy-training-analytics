import pandas as pd

df = pd.read_csv(
    "data/processed/hevy_exercises.csv"
)

print("\n===== RESUMO =====")

print(f"\nTotal de séries: {len(df)}")

print(f"\nVolume total levantado: {df['volume'].sum():,.2f} kg")

print("\nTop 10 exercícios por volume:")

exercise_volume = (
    df.groupby("exercise")["volume"]
    .sum()
    .sort_values(ascending=False)
)

print(exercise_volume.head(10))

print("\nTop 10 exercícios por número de séries:")

exercise_sets = (
    df.groupby("exercise")
    .size()
    .sort_values(ascending=False)
)

print(exercise_sets.head(10))