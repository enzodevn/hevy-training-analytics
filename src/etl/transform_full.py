import json
import pandas as pd

# -----------------------------
# 1) Ler JSON completo do Hevy
# -----------------------------
input_path = "data/raw/hevy_workouts_full.json"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

workouts = data["workouts"]

rows = []

# -----------------------------
# 2) Explodir workouts -> exercises -> sets
# -----------------------------
for workout in workouts:
    workout_id = workout.get("id")
    workout_title = workout.get("title")
    workout_description = workout.get("description")
    workout_start = workout.get("start_time")
    workout_end = workout.get("end_time")

    for exercise in workout.get("exercises", []):
        exercise_name = exercise.get("title")
        exercise_index = exercise.get("index")
        exercise_template_id = exercise.get("exercise_template_id")
        superset_id = exercise.get("superset_id")

        for set_data in exercise.get("sets", []):
            set_index = set_data.get("index")
            set_type = set_data.get("type")
            weight_kg = set_data.get("weight_kg")
            reps = set_data.get("reps")
            distance_meters = set_data.get("distance_meters")
            duration_seconds = set_data.get("duration_seconds")
            rpe = set_data.get("rpe")
            custom_metric = set_data.get("custom_metric")

            # volume simples para musculação
            volume = 0
            if weight_kg is not None and reps is not None:
                volume = weight_kg * reps

            rows.append({
                "workout_id": workout_id,
                "workout_title": workout_title,
                "workout_description": workout_description,
                "workout_start": workout_start,
                "workout_end": workout_end,
                "exercise_index": exercise_index,
                "exercise": exercise_name,
                "exercise_template_id": exercise_template_id,
                "superset_id": superset_id,
                "set_index": set_index,
                "set_type": set_type,
                "weight_kg": weight_kg,
                "reps": reps,
                "distance_meters": distance_meters,
                "duration_seconds": duration_seconds,
                "rpe": rpe,
                "custom_metric": custom_metric,
                "volume": volume
            })

# -----------------------------
# 3) Criar DataFrame
# -----------------------------
df = pd.DataFrame(rows)

# Converter datas
df["workout_start"] = pd.to_datetime(df["workout_start"], errors="coerce")
df["workout_end"] = pd.to_datetime(df["workout_end"], errors="coerce")

# Criar colunas auxiliares
df["workout_date"] = df["workout_start"].dt.date
df["workout_year"] = df["workout_start"].dt.year
df["workout_month"] = df["workout_start"].dt.month
df["workout_week"] = df["workout_start"].dt.isocalendar().week

# duração do treino em minutos
df["workout_duration_min"] = (
    (df["workout_end"] - df["workout_start"]).dt.total_seconds() / 60
)

# -----------------------------
# 4) Salvar CSV completo
# -----------------------------
output_path = "data/processed/hevy_exercises_full.csv"
df.to_csv(output_path, index=False)

# -----------------------------
# 5) Logs
# -----------------------------
print("\n===== TRANSFORMAÇÃO CONCLUÍDA =====")
print(f"Arquivo salvo em: {output_path}")
print(f"Total de linhas: {len(df)}")
print(f"Total de treinos únicos: {df['workout_id'].nunique()}")
print(f"Total de exercícios únicos: {df['exercise'].nunique()}")

print("\nPrévia:")
print(df.head(10))