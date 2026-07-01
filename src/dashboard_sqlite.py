import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DB_PATH = "data/hevy.db"

# ---------------------------------
# Configuração da página
# ---------------------------------
st.set_page_config(
    page_title="Hevy Tracker",
    layout="wide"
)

st.title("🏋️ Hevy Tracker")
st.caption("Dashboard de evolução de treinos conectado ao SQLite")

# ---------------------------------
# Função para ler SQL
# ---------------------------------
def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---------------------------------
# QUERY 1 - Resumo geral
# ---------------------------------
summary_query = """
SELECT
    (SELECT COUNT(*) FROM workouts) AS total_workouts,
    (SELECT COUNT(*) FROM exercise_sets) AS total_sets,
    (SELECT COUNT(DISTINCT exercise_name) FROM exercise_sets) AS total_exercises,
    (SELECT ROUND(SUM(volume), 2) FROM exercise_sets) AS total_volume
"""

summary = run_query(summary_query)

# ---------------------------------
# QUERY 2 - Lista de exercícios
# ---------------------------------
exercise_list_query = """
SELECT DISTINCT exercise_name
FROM exercise_sets
WHERE exercise_name IS NOT NULL
ORDER BY exercise_name
"""

exercise_list = run_query(exercise_list_query)

# ---------------------------------
# QUERY 3 - Top exercícios por volume
# ---------------------------------
top_volume_query = """
SELECT
    exercise_name,
    ROUND(SUM(volume), 2) AS total_volume
FROM exercise_sets
GROUP BY exercise_name
ORDER BY total_volume DESC
LIMIT 10
"""

top_volume = run_query(top_volume_query)

# ---------------------------------
# QUERY 4 - Top exercícios por séries
# ---------------------------------
top_sets_query = """
SELECT
    exercise_name,
    COUNT(*) AS total_sets
FROM exercise_sets
GROUP BY exercise_name
ORDER BY total_sets DESC
LIMIT 10
"""

top_sets = run_query(top_sets_query)

# ---------------------------------
# QUERY 5 - PRs
# ---------------------------------
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

prs = run_query(prs_query)

# ---------------------------------
# QUERY 6 - Frequência semanal
# ---------------------------------
weekly_frequency_query = """
SELECT
    STRFTIME('%Y', start_time) AS workout_year,
    STRFTIME('%W', start_time) AS workout_week,
    COUNT(*) AS workouts_count
FROM workouts
GROUP BY workout_year, workout_week
ORDER BY workout_year, workout_week
"""

weekly_frequency = run_query(weekly_frequency_query)

# ---------------------------------
# QUERY 7 - Volume semanal
# ---------------------------------
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

weekly_volume = run_query(weekly_volume_query)

# ---------------------------------
# QUERY 8 - Volume por treino
# ---------------------------------
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
ORDER BY workout_date
"""

volume_per_workout = run_query(volume_per_workout_query)

# ---------------------------------
# Cards principais
# ---------------------------------
total_workouts = int(summary.loc[0, "total_workouts"])
total_sets = int(summary.loc[0, "total_sets"])
total_exercises = int(summary.loc[0, "total_exercises"])
total_volume = float(summary.loc[0, "total_volume"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Treinos", total_workouts)
col2.metric("Séries", total_sets)
col3.metric("Exercícios", total_exercises)
col4.metric("Volume total", f"{total_volume:,.1f} kg")

st.divider()

# ---------------------------------
# Sidebar - filtro por exercício
# ---------------------------------
exercise_options = exercise_list["exercise_name"].tolist()
selected_exercise = st.sidebar.selectbox(
    "Selecione um exercício",
    ["Todos"] + exercise_options
)

# ---------------------------------
# Linha 1 - Volume semanal / Frequência semanal
# ---------------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Volume semanal")

    weekly_volume["year_week"] = (
        weekly_volume["workout_year"].astype(str)
        + "-W" +
        weekly_volume["workout_week"].astype(str)
    )

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(
        weekly_volume["year_week"],
        weekly_volume["weekly_volume"],
        marker="o"
    )
    ax1.set_xlabel("Semana")
    ax1.set_ylabel("Volume")
    ax1.set_title("Volume semanal")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with colB:
    st.subheader("📅 Frequência semanal")

    weekly_frequency["year_week"] = (
        weekly_frequency["workout_year"].astype(str)
        + "-W" +
        weekly_frequency["workout_week"].astype(str)
    )

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(
        weekly_frequency["year_week"],
        weekly_frequency["workouts_count"]
    )
    ax2.set_xlabel("Semana")
    ax2.set_ylabel("Treinos")
    ax2.set_title("Frequência semanal")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# ---------------------------------
# Linha 2 - Top volume / top séries
# ---------------------------------
colC, colD = st.columns(2)

with colC:
    st.subheader("🏆 Top exercícios por volume")

    top_volume_sorted = top_volume.sort_values("total_volume", ascending=True)

    fig3, ax3 = plt.subplots(figsize=(8, 6))
    ax3.barh(top_volume_sorted["exercise_name"], top_volume_sorted["total_volume"])
    ax3.set_xlabel("Volume total (kg)")
    ax3.set_title("Top exercícios por volume")
    st.pyplot(fig3)

with colD:
    st.subheader("🔁 Top exercícios por séries")

    top_sets_sorted = top_sets.sort_values("total_sets", ascending=True)

    fig4, ax4 = plt.subplots(figsize=(8, 6))
    ax4.barh(top_sets_sorted["exercise_name"], top_sets_sorted["total_sets"])
    ax4.set_xlabel("Número de séries")
    ax4.set_title("Top exercícios por séries")
    st.pyplot(fig4)

# ---------------------------------
# Linha 3 - Volume por treino
# ---------------------------------
st.subheader("📦 Volume por treino")

fig5, ax5 = plt.subplots(figsize=(12, 4))
ax5.plot(
    volume_per_workout["workout_date"],
    volume_per_workout["total_volume"],
    marker="o"
)
ax5.set_xlabel("Data")
ax5.set_ylabel("Volume")
ax5.set_title("Volume por treino")
plt.xticks(rotation=45)
st.pyplot(fig5)

# ---------------------------------
# PRs
# ---------------------------------
st.subheader("💪 PRs por exercício")
st.dataframe(prs, use_container_width=True)

# ---------------------------------
# Bloco de evolução por exercício
# ---------------------------------
st.subheader("📊 Evolução por exercício")

if selected_exercise != "Todos":
    exercise_progress_query = f"""
    SELECT
        DATE(w.start_time) AS workout_date,
        es.weight_kg,
        es.reps,
        es.volume,
        es.set_type
    FROM exercise_sets es
    JOIN workouts w
        ON es.workout_id = w.workout_id
    WHERE es.exercise_name = '{selected_exercise.replace("'", "''")}'
      AND es.weight_kg IS NOT NULL
    ORDER BY workout_date
    """

    exercise_progress = run_query(exercise_progress_query)

    if not exercise_progress.empty:
        max_weight_per_day = (
            exercise_progress.groupby("workout_date", as_index=False)["weight_kg"]
            .max()
            .sort_values("workout_date")
        )

        fig6, ax6 = plt.subplots(figsize=(10, 4))
        ax6.plot(
            max_weight_per_day["workout_date"],
            max_weight_per_day["weight_kg"],
            marker="o"
        )
        ax6.set_xlabel("Data")
        ax6.set_ylabel("Carga máxima (kg)")
        ax6.set_title(f"Evolução de carga - {selected_exercise}")
        plt.xticks(rotation=45)
        st.pyplot(fig6)

        st.markdown("### Histórico bruto do exercício")
        st.dataframe(exercise_progress, use_container_width=True)
    else:
        st.info("Não há dados suficientes para esse exercício.")
else:
    st.info("Selecione um exercício na barra lateral para ver a evolução específica.")