import json
import pandas as pd

# Ler JSON salvo
with open(
    "data/raw/hevy_workouts.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

rows = []

for workout in data["workouts"]:

    workout_date = workout["start_time"]

    for exercise in workout["exercises"]:

        exercise_name = exercise["title"]

        for set_data in exercise["sets"]:

            weight = set_data.get("weight_kg")
            reps = set_data.get("reps")

            volume = 0

            if weight and reps:
                volume = weight * reps

            rows.append({
           "date": workout_date,
           "exercise": exercise_name,
           "weight_kg": weight,
           "reps": reps,
           "volume": volume,
           "set_type": set_data.get("type")
})
df = pd.DataFrame(rows)

print(df.head())

df.to_csv(
    "data/processed/hevy_exercises.csv",
    index=False
)

print("\nCSV salvo com sucesso!")
print(f"Total de registros: {len(df)}")