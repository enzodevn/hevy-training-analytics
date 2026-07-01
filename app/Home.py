import sys
from pathlib import Path

# adiciona a raiz do projeto ao path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
from src.queries.overview_queries import get_summary, get_recent_workouts

st.set_page_config(
    page_title="Hevy Tracker App",
    page_icon="🏋️",
    layout="wide"
)

summary = get_summary()
recent_workouts = get_recent_workouts()

total_workouts = int(summary.loc[0, "total_workouts"])
total_sets = int(summary.loc[0, "total_sets"])
total_exercises = int(summary.loc[0, "total_exercises"])
total_volume = float(summary.loc[0, "total_volume"])

st.title("🏋️ Hevy Tracker App")
st.caption("Seu aplicativo pessoal de evolução de treinos, analytics e histórico do Hevy.")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Treinos", total_workouts)
col2.metric("Séries", total_sets)
col3.metric("Exercícios", total_exercises)
col4.metric("Volume total", f"{total_volume:,.1f} kg")

st.markdown("---")

st.subheader("📌 Sobre este app")
st.write(
    """
    Este app foi criado para acompanhar sua evolução de treino a partir dos dados do Hevy.

    Ele será a base de um produto pessoal com:
    - histórico completo de treinos
    - evolução por exercício
    - recordes pessoais (PRs)
    - análises semanais de volume e frequência
    - atualização automática após novos treinos
    """
)

st.markdown("---")

st.subheader("🕒 Últimos treinos registrados")
st.dataframe(recent_workouts, use_container_width=True)

st.info("Use a barra lateral para navegar entre as páginas do app.")