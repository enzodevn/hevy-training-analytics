import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------------------------------
# Configuração da página
# ---------------------------------
st.set_page_config(
    page_title="Hevy Workout Analytics",
    layout="wide"
)

st.title("🏋️ Hevy Workout Analytics Dashboard")
st.caption("Projeto de análise de treinos com Python + Pandas + Streamlit")

# ---------------------------------
# Carregar dados
# ---------------------------------
df = pd.read_csv("data/processed/hevy_exercises_full.csv")
weekly_volume = pd.read_csv("data/processed/weekly_volume.csv")
weekly_workouts = pd.read_csv("data/processed/weekly_workouts.csv")
prs = pd.read_csv("data/processed/prs_by_exercise.csv")
top_volume = pd.read_csv("data/processed/top_exercises_by_volume.csv")
top_sets = pd.read_csv("data/processed/top_exercises_by_sets.csv")

# ---------------------------------
# Tratamento básico
# ---------------------------------
df["workout_start"] = pd.to_datetime(df["workout_start"], errors="coerce")
df["workout_end"] = pd.to_datetime(df["workout_end"], errors="coerce")
df["workout_date"] = pd.to_datetime(df["workout_date"], errors="coerce")

# ---------------------------------
# Métricas principais
# ---------------------------------
total_workouts = df["workout_id"].nunique()
total_exercises = df["exercise"].nunique()
total_sets = len(df)
total_volume = df["volume"].fillna(0).sum()

avg_duration = (
    df.groupby("workout_id")["workout_duration_min"]
    .max()
    .mean()
)

# ---------------------------------
# Cards
# ---------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Treinos únicos", f"{total_workouts}")
col2.metric("Exercícios únicos", f"{total_exercises}")
col3.metric("Séries totais", f"{total_sets}")
col4.metric("Volume total", f"{total_volume:,.1f} kg")

st.metric("Duração média dos treinos", f"{avg_duration:.1f} min")

st.divider()

# ---------------------------------
# Sidebar filtros
# ---------------------------------
st.sidebar.header("Filtros")

exercise_options = sorted(df["exercise"].dropna().unique())
selected_exercise = st.sidebar.selectbox(
    "Selecione um exercício",
    options=["Todos"] + exercise_options
)

if selected_exercise != "Todos":
    filtered_df = df[df["exercise"] == selected_exercise].copy()
else:
    filtered_df = df.copy()

# ---------------------------------
# Volume semanal
# ---------------------------------
st.subheader("📈 Volume semanal")

weekly_volume["year_week"] = (
    weekly_volume["workout_year"].astype(str)
    + "-W" +
    weekly_volume["workout_week"].astype(str)
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(
    weekly_volume["year_week"],
    weekly_volume["volume"],
    marker="o"
)
ax1.set_title("Volume por semana")
ax1.set_xlabel("Semana")
ax1.set_ylabel("Volume (kg)")
plt.xticks(rotation=45)

st.pyplot(fig1)

# ---------------------------------
# Frequência semanal
# ---------------------------------
st.subheader("📅 Frequência semanal de treinos")

weekly_workouts["year_week"] = (
    weekly_workouts["workout_year"].astype(str)
    + "-W" +
    weekly_workouts["workout_week"].astype(str)
)

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(
    weekly_workouts["year_week"],
    weekly_workouts["workouts_count"]
)
ax2.set_title("Treinos por semana")
ax2.set_xlabel("Semana")
ax2.set_ylabel("Quantidade de treinos")
plt.xticks(rotation=45)

st.pyplot(fig2)

# ---------------------------------
# Top exercícios por volume
# ---------------------------------
st.subheader("🏆 Top exercícios por volume")

top_volume_sorted = top_volume.sort_values("total_volume", ascending=True)

fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.barh(
    top_volume_sorted["exercise"],
    top_volume_sorted["total_volume"]
)
ax3.set_title("Top exercícios por volume")
ax3.set_xlabel("Volume total (kg)")

st.pyplot(fig3)

# ---------------------------------
# Top exercícios por número de séries
# ---------------------------------
st.subheader("🔁 Top exercícios por número de séries")

top_sets_sorted = top_sets.sort_values("sets_count", ascending=True)

fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.barh(
    top_sets_sorted["exercise"],
    top_sets_sorted["sets_count"]
)
ax4.set_title("Top exercícios por número de séries")
ax4.set_xlabel("Quantidade de séries")

st.pyplot(fig4)

# ---------------------------------
# PRs
# ---------------------------------
st.subheader("💪 PRs por exercício")

prs_sorted = prs.sort_values("max_weight_kg", ascending=False).head(15)

st.dataframe(prs_sorted, use_container_width=True)

# ---------------------------------
# Evolução do exercício selecionado
# ---------------------------------
st.subheader("📊 Evolução por exercício")

if selected_exercise != "Todos":
    exercise_progress = (
        filtered_df.groupby("workout_date")["weight_kg"]
        .max()
        .reset_index()
        .sort_values("workout_date")
    )

    fig5, ax5 = plt.subplots(figsize=(10, 4))
    ax5.plot(
        exercise_progress["workout_date"],
        exercise_progress["weight_kg"],
        marker="o"
    )
    ax5.set_title(f"Evolução de carga máxima - {selected_exercise}")
    ax5.set_xlabel("Data")
    ax5.set_ylabel("Carga máxima (kg)")
    plt.xticks(rotation=45)

    st.pyplot(fig5)

    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("Selecione um exercício na barra lateral para ver a evolução específica.")

# ---------------------------------
# Tabela geral
# ---------------------------------
st.subheader("🧾 Base completa de treinos")

st.dataframe(df, use_container_width=True)