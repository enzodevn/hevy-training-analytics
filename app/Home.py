import sys
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO DO PROJETO
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st

from src.components.sync import render_sync_button
from src.queries.overview_queries import (
    get_summary,
    get_recent_workouts
)

from src.queries.charts_queries import (
    get_weekly_volume
)

from src.components.cards.metric_cards import (
    render_metric_cards
)

from src.components.charts.weekly_volume import (
    weekly_volume_chart
)
# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Hevy Training Analytics",
    page_icon="🏋️",
    layout="wide"
)

render_sync_button()

# ==========================================================
# CONSULTAS
# ==========================================================

summary_df = get_summary()
recent_workouts = get_recent_workouts()

summary = {
    "total_workouts": int(summary_df.loc[0, "total_workouts"]),
    "total_sets": int(summary_df.loc[0, "total_sets"]),
    "total_exercises": int(summary_df.loc[0, "total_exercises"]),
    "total_volume": float(summary_df.loc[0, "total_volume"]),
}

# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("🏋️ Hevy Training Analytics")

st.caption(
    "Dashboard pessoal para acompanhar sua evolução de treinos utilizando a API do Hevy."
)

st.divider()

# ==========================================================
# CARDS
# ==========================================================

render_metric_cards(summary)
st.divider()

weekly_volume = get_weekly_volume()

weekly_volume_chart(weekly_volume)
st.divider()

# ==========================================================
# SOBRE O PROJETO
# ==========================================================

st.subheader("📌 Sobre o projeto")

st.write("""
O **Hevy Training Analytics** é um projeto desenvolvido para transformar os dados do Hevy em uma plataforma completa de análise de desempenho.

O objetivo é evoluir este projeto até incluir:

- 📈 Evolução por exercício
- 🏆 Personal Records (PRs)
- 📅 Frequência semanal
- 🔥 Volume de treino
- 💪 Análise por grupo muscular
- 🤖 Insights automáticos
- ☁️ Atualização automática após cada treino
""")

st.divider()

# ==========================================================
# ÚLTIMOS TREINOS
# ==========================================================

st.subheader("🕒 Últimos treinos")

st.dataframe(
    recent_workouts,
    use_container_width=True,
    hide_index=True
)

st.info("Utilize o menu lateral para navegar entre as páginas do dashboard.")