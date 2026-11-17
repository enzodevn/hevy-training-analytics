import sys
from pathlib import Path

# ==========================================================
# CONFIGURAÇÃO DO PROJETO
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st

from src.components.sync import render_sync_button

from src.queries.exercise_queries import (
    get_all_exercises,
    get_exercise_history,
    get_exercise_summary
)

from src.components.exercises.exercise_selector import (
    render_exercise_selector
)

from src.components.charts.exercise_progress import (
    exercise_progress_chart
)

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Exercise Analytics",
    page_icon="💪",
    layout="wide"
)

render_sync_button()

# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("💪 Exercise Analytics")

st.caption(
    "Escolha um exercício para visualizar sua evolução ao longo do tempo."
)

st.divider()

# ==========================================================
# SELETOR
# ==========================================================

exercise_df = get_all_exercises()

selected = render_exercise_selector(exercise_df)

st.success(f"Exercício selecionado: {selected}")

st.divider()

# ==========================================================
# HISTÓRICO
# ==========================================================

history = get_exercise_history(selected)

# ==========================================================
# GRÁFICO
# ==========================================================

st.subheader("📈 Evolução da Carga")

exercise_progress_chart(history, selected)

st.divider()

# ==========================================================
# TABELA
# ==========================================================

st.subheader("📅 Histórico do Exercício")

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# PRÓXIMAS FEATURES
# ==========================================================

st.subheader("🚧 Em desenvolvimento")

st.write("""
Nas próximas versões esta página exibirá:

- 🏆 Personal Record (PR)
- 📊 Volume total
- 🔥 Volume acumulado
- 📈 Evolução do volume
- 📅 Frequência do exercício
- 💪 Melhor série
- 🤖 Insights automáticos
""")

from src.components.cards.exercise_cards import render_exercise_cards

summary = get_exercise_summary(selected)

render_exercise_cards(summary)