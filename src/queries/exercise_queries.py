import sqlite3
import pandas as pd

DB_PATH = "data/hevy.db"


# ==========================================================
# LISTA DE EXERCÍCIOS
# ==========================================================

def get_all_exercises():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT DISTINCT
        exercise_name

    FROM exercise_sets

    ORDER BY exercise_name
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ==========================================================
# HISTÓRICO
# ==========================================================

def get_exercise_history(exercise_name):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        DATE(workouts.start_time) AS workout_date,

        exercise_sets.weight_kg,

        exercise_sets.reps,

        exercise_sets.volume,

        exercise_sets.set_type

    FROM exercise_sets

    JOIN workouts
        ON workouts.workout_id = exercise_sets.workout_id

    WHERE exercise_name = ?

    ORDER BY workouts.start_time
    """

    df = pd.read_sql(
        query,
        conn,
        params=(exercise_name,)
    )

    conn.close()

    return df


# ==========================================================
# RESUMO DO EXERCÍCIO
# ==========================================================

def get_exercise_summary(exercise_name):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        MAX(weight_kg)               AS pr,

        SUM(volume)                  AS total_volume,

        COUNT(*)                     AS total_sets,

        MAX(DATE(workouts.start_time)) AS last_workout

    FROM exercise_sets

    JOIN workouts
        ON workouts.workout_id = exercise_sets.workout_id

    WHERE exercise_name = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(exercise_name,)
    )

    conn.close()

    return df