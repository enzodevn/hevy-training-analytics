import sqlite3
import pandas as pd

DB_PATH = "data/hevy.db"


def get_weekly_volume():
    """
    Retorna o volume semanal de treino.
    """

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        strftime('%Y', start_time) AS workout_year,
        strftime('%W', start_time) AS workout_week,
        SUM(volume) AS weekly_volume

    FROM workouts

    JOIN exercise_sets
        ON workouts.workout_id = exercise_sets.workout_id

    GROUP BY workout_year, workout_week

    ORDER BY workout_year, workout_week
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df