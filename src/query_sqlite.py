import sqlite3
import pandas as pd

DB_PATH = "data/hevy.db"

conn = sqlite3.connect(DB_PATH)

# -----------------------------
# 1) Resumo geral
# -----------------------------
summary_query = """
SELECT
    (SELECT COUNT(*) FROM workouts) AS total_workouts,
    (SELECT COUNT(*) FROM exercise_sets) AS total_sets,
    (SELECT COUNT(DISTINCT exercise_name) FROM exercise_sets) AS total_exercises,
    (SELECT ROUND(SUM(volume), 2) FROM exercise_sets) AS total_volume
"""

summary = pd.read_sql_query(summary_query, conn)

# -----------------------------
# 2) Top exercícios por volume
# -----------------------------
top_volume_query = """
SELECT
    exercise_name,
    ROUND(SUM(volume), 2) AS total_volume
FROM exercise_sets
GROUP BY exercise_name
ORDER BY total_volume DESC
LIMIT 10
"""

top_volume = pd.read_sql_query(top_volume_query, conn)

# -----------------------------
# 3) Top exercícios por número de séries
# -----------------------------
top_sets_query = """
SELECT
    exercise_name,
    COUNT(*) AS total_sets
FROM exercise_sets
GROUP BY exercise_name
ORDER BY total_sets DESC
LIMIT 10
"""

top_sets = pd.read_sql_query(top_sets_query, conn)

# -----------------------------
# 4) PRs (maior carga por exercício)
# -----------------------------
prs_query = """
SELECT
    exercise_name,
    MAX(weight_kg) AS max_weight_kg
FROM exercise_sets
WHERE weight_kg IS NOT NULL
GROUP BY exercise_name
ORDER BY max_weight_kg DESC
LIMIT 15
"""

prs = pd.read_sql_query(prs_query, conn)

# -----------------------------
# 5) Volume por treino
# -----------------------------
volume_per_workout_query = """
SELECT
    w.workout_id,
    w.title,
    DATE(w.start_time) AS workout_date,
    ROUND(SUM(es.volume), 2) AS total_volume
FROM workouts w
JOIN exercise_sets es
    ON w.workout_id = es.workout_id
GROUP BY w.workout_id, w.title, DATE(w.start_time)
ORDER BY total_volume DESC
"""

volume_per_workout = pd.read_sql_query(volume_per_workout_query, conn)

# -----------------------------
# 6) Frequência semanal
# -----------------------------
weekly_frequency_query = """
SELECT
    STRFTIME('%Y', start_time) AS workout_year,
    STRFTIME('%W', start_time) AS workout_week,
    COUNT(*) AS workouts_count
FROM workouts
GROUP BY workout_year, workout_week
ORDER BY workout_year, workout_week
"""

weekly_frequency = pd.read_sql_query(weekly_frequency_query, conn)

# -----------------------------
# 7) Volume semanal
# -----------------------------
weekly_volume_query = """
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

weekly_volume = pd.read_sql_query(weekly_volume_query, conn)

conn.close()

# -----------------------------
# 8) Exibir resultados
# -----------------------------
print("\n" + "=" * 50)
print("HEVY SQLITE REPORT")
print("=" * 50)

print("\n[RESUMO GERAL]")
print(summary)

print("\n[TOP EXERCÍCIOS POR VOLUME]")
print(top_volume)

print("\n[TOP EXERCÍCIOS POR NÚMERO DE SÉRIES]")
print(top_sets)

print("\n[PRs POR EXERCÍCIO]")
print(prs)

print("\n[VOLUME POR TREINO]")
print(volume_per_workout)

print("\n[FREQUÊNCIA SEMANAL]")
print(weekly_frequency)

print("\n[VOLUME SEMANAL]")
print(weekly_volume)