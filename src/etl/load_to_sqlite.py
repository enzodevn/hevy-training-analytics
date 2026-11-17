import json
import sqlite3
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "data" / "hevy.db"
JSON_PATH = BASE_DIR / "data" / "raw" / "hevy_workouts_full.json"

# ==========================================================
# BANCO
# ==========================================================

def connect_database():
    """Conecta ao banco SQLite."""
    return sqlite3.connect(DB_PATH)


# ==========================================================
# UTILIDADES
# ==========================================================

# ==========================================================
# UPSERT WORKOUT
# ==========================================================

def insert_workout(cursor, workout):

    cursor.execute("""
        INSERT INTO workouts (
            workout_id,
            title,
            description,
            start_time,
            end_time,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(workout_id) DO UPDATE SET
            title = excluded.title,
            description = excluded.description,
            start_time = excluded.start_time,
            end_time = excluded.end_time,
            created_at = excluded.created_at,
            updated_at = excluded.updated_at
    """, (
        workout.get("id"),
        workout.get("title"),
        workout.get("description"),
        workout.get("start_time"),
        workout.get("end_time"),
        workout.get("created_at"),
        workout.get("updated_at")
    ))


# ==========================================================
# INSERT SETS
# ==========================================================

def insert_sets(cursor, workout):

    workout_id = workout["id"]

    inserted = 0

    for exercise in workout.get("exercises", []):

        exercise_index = exercise.get("index")
        exercise_name = exercise.get("title")
        exercise_template_id = exercise.get("exercise_template_id")
        superset_id = exercise.get("superset_id")

        for set_data in exercise.get("sets", []):

            weight = set_data.get("weight_kg")
            reps = set_data.get("reps")

            volume = 0

            if weight is not None and reps is not None:
                volume = weight * reps

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

                set_data.get("index"),
                set_data.get("type"),
                weight,
                reps,
                set_data.get("distance_meters"),
                set_data.get("duration_seconds"),
                set_data.get("rpe"),
                set_data.get("custom_metric"),

                volume

            ))

            inserted += 1

    return inserted


# ==========================================================
# LOAD
# ==========================================================

def load_workouts():

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    workouts = data["workouts"]

    conn = connect_database()
    cursor = conn.cursor()

    workouts_inserted = 0
    sets_inserted = 0
    workouts_updated = 0

    try:
        for workout in workouts:
            workout_id = workout.get("id")
            if not workout_id:
                raise ValueError("A resposta do Hevy contém um treino sem ID.")

            cursor.execute(
                "SELECT 1 FROM workouts WHERE workout_id = ?",
                (workout_id,)
            )
            exists = cursor.fetchone() is not None

            insert_workout(cursor, workout)

            if exists:
                cursor.execute(
                    "DELETE FROM exercise_sets WHERE workout_id = ?",
                    (workout_id,)
                )
                workouts_updated += 1
            else:
                workouts_inserted += 1

            sets_inserted += insert_sets(cursor, workout)

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print("\n===================================")
    print("LOAD FINALIZADO")
    print("===================================")
    print(f"Treinos inseridos : {workouts_inserted}")
    print(f"Treinos atualizados: {workouts_updated}")
    print(f"Séries inseridas  : {sets_inserted}")
    print(f"Banco             : {DB_PATH}")
    print("===================================\n")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("Iniciando carga no SQLite...")

    load_workouts()


if __name__ == "__main__":
    main()