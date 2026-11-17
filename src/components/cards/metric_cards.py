import streamlit as st


def render_metric_cards(summary):
    """
    Renderiza os cards principais do dashboard.
    """

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏋️ Treinos",
            value=summary["total_workouts"]
        )

    with col2:
        st.metric(
            label="💪 Exercícios",
            value=summary["total_exercises"]
        )

    with col3:
        st.metric(
            label="📊 Séries",
            value=summary["total_sets"]
        )

    with col4:
        st.metric(
            label="🔥 Volume",
            value=f'{summary["total_volume"]:,.0f} kg'
        )