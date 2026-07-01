import streamlit as st
import matplotlib.pyplot as plt
from src.queries.overview_queries import (
    get_summary,
    get_weekly_volume,
    get_weekly_frequency,
    get_volume_per_workout,
    get_recent_workouts
)

st.set_page_config(
    page_title="Overview | Hevy Tracker",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Overview")
st.caption("Visão geral da sua atividade de treino no Hevy.")

summary = get_summary()
weekly_volume = get_weekly_volume()
weekly_frequency = get_weekly_frequency()
volume_per_workout = get_volume_per_workout()
recent_workouts = get_recent_workouts(limit=10)

total_workouts = int(summary.loc[0, "total_workouts"])
total_sets = int(summary.loc[0, "total_sets"])
total_exercises = int(summary.loc[0, "total_exercises"])
total_volume = float(summary.loc[0, "total_volume"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Treinos", total_workouts)
col2.metric("Séries", total_sets)
col3.metric("Exercícios", total_exercises)
col4.metric("Volume total", f"{total_volume:,.1f} kg")

st.markdown("---")

weekly_volume["year_week"] = (
    weekly_volume["workout_year"].astype(str)
    + "-W" +
    weekly_volume["workout_week"].astype(str)
)

weekly_frequency["year_week"] = (
    weekly_frequency["workout_year"].astype(str)
    + "-W" +
    weekly_frequency["workout_week"].astype(str)
)

colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Volume semanal")

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(
        weekly_volume["year_week"],
        weekly_volume["weekly_volume"],
        marker="o"
    )
    ax1.set_title("Volume semanal")
    ax1.set_xlabel("Semana")
    ax1.set_ylabel("Volume (kg)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with colB:
    st.subheader("📅 Frequência semanal")

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(
        weekly_frequency["year_week"],
        weekly_frequency["workouts_count"]
    )
    ax2.set_title("Treinos por semana")
    ax2.set_xlabel("Semana")
    ax2.set_ylabel("Quantidade de treinos")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.markdown("---")

st.subheader("📦 Volume por treino")

fig3, ax3 = plt.subplots(figsize=(12, 4))
ax3.plot(
    volume_per_workout["workout_date"],
    volume_per_workout["total_volume"],
    marker="o"
)
ax3.set_title("Volume por treino")
ax3.set_xlabel("Data")
ax3.set_ylabel("Volume (kg)")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.markdown("---")

st.subheader("🕒 Últimos treinos")
st.dataframe(recent_workouts, use_container_width=True)