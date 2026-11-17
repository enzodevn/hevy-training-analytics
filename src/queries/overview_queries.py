import sqlite3
import pandas as pd
from src.config import DB_PATH


def run_query(query: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_summary():
    query = """
    SELECT
        (SELECT COUNT(*) FROM workouts) AS total_workouts,
        (SELECT COUNT(*) FROM exercise_sets) AS total_sets,
        (SELECT COUNT(DISTINCT exercise_name) FROM exercise_sets) AS total_exercises,
        (SELECT ROUND(SUM(volume), 2) FROM exercise_sets) AS total_volume
    """
    return run_query(query)


def get_weekly_volume():
    query = """
    SELECT
        STRFTIME('%Y', w.start_time) AS workout_year,
        STRFTIME('%W', w.start_time) AS workout_week,
        ROUND(SUM(es.volume), 2) AS weekly_volume
    FROM workouts w
    JOIN exercise_sets es
        ON w.workout_id = es.workout_id
    GROUP BY workout_year, workout_week
    ORDER BY workout_year, workout_week
    """
    return run_query(query)


def get_weekly_frequency():
    query = """
    SELECT
        STRFTIME('%Y', start_time) AS workout_year,
        STRFTIME('%W', start_time) AS workout_week,
        COUNT(*) AS workouts_count
    FROM workouts
    GROUP BY workout_year, workout_week
    ORDER BY workout_year, workout_week
    """
    return run_query(query)


def get_volume_per_workout():
    query = """
    SELECT
        w.workout_id,
        w.title,
        DATE(w.start_time) AS workout_date,
        ROUND(SUM(es.volume), 2) AS total_volume
    FROM workouts w
    JOIN exercise_sets es
        ON w.workout_id = es.workout_id
    GROUP BY w.workout_id, w.title, DATE(w.start_time)
    ORDER BY workout_date
    """
    return run_query(query)


def get_recent_workouts(limit=5):
    query = f"""
    SELECT
        w.workout_id,
        w.title,
        DATE(w.start_time) AS workout_date,
        ROUND(SUM(es.volume), 2) AS total_volume,
        COUNT(DISTINCT es.exercise_name) AS exercises_count
    FROM workouts w
    JOIN exercise_sets es
        ON w.workout_id = es.workout_id
    GROUP BY w.workout_id, w.title, DATE(w.start_time)
    ORDER BY w.start_time DESC
    LIMIT {limit}
    """
    return run_query(query)