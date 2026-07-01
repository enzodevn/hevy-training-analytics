import json
import sqlite3

DB_PATH = "data/hevy.db"
JSON_PATH = "data/raw/hevy_workouts_full.json"

# -----------------------------
# 1) Conectar no banco
# -----------------------------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# -----------------------------
# 2) Ler JSON
# -----------------------------
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

workouts = data["workouts"]

workouts_inserted = 0
sets_inserted = 0

# -----------------------------
# 3) Inserir dados
# -----------------------------
for workout in workouts:
    workout_id = workout.get("id")
    title = workout.get("title")
    description = workout.get("description")
    start_time = workout.get("start_time")
    end_time = workout.get("end_time")
    created_at = workout.get("created_at")
    updated_at = workout.get("updated_at")

    # inserir workout
    cursor.execute("""
        INSERT INTO workouts (
            workout_id, title, description, start_time, end_time, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        workout_id, title, description, start_time, end_time, created_at, updated_at
    ))
    workouts_inserted += 1

    # inserir exercícios / sets
    for exercise in workout.get("exercises", []):
        exercise_index = exercise.get("index")
        exercise_name = exercise.get("title")
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

            volume = 0
            if weight_kg is not None and reps is not None:
                volume = weight_kg * reps

            cursor.execute("""
                INSERT INTO exercise_sets (
                    workout_id,
                    exercise_index,
                    exercise_name,
                    exercise_template_id,
                    superset_id,
                    set_index,
                    set_type,
                    weight_kg,
                    reps,
                    distance_meters,
                    duration_seconds,
                    rpe,
                    custom_metric,
                    volume
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                workout_id,
                exercise_index,
                exercise_name,
                exercise_template_id,
                superset_id,
                set_index,
                set_type,
                weight_kg,
                reps,
                distance_meters,
                duration_seconds,
                rpe,
                custom_metric,
                volume
            ))
            sets_inserted += 1

# -----------------------------
# 4) Salvar
# -----------------------------
conn.commit()
conn.close()

print("Carga no SQLite concluída!")
print(f"Treinos inseridos: {workouts_inserted}")
print(f"Séries inseridas: {sets_inserted}")
print(f"Banco salvo em: {DB_PATH}")