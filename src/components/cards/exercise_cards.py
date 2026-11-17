import streamlit as st


def render_exercise_cards(summary_df):
    """
    Renderiza os cards com as estatísticas do exercício.
    """

    if summary_df.empty:
        st.warning("Nenhuma informação encontrada.")
        return

    summary = summary_df.iloc[0]

    pr = summary["pr"] if summary["pr"] is not None else 0
    total_volume = summary["total_volume"] if summary["total_volume"] is not None else 0
    total_sets = summary["total_sets"] if summary["total_sets"] is not None else 0
    last_workout = summary["last_workout"] if summary["last_workout"] else "-"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🏆 PR",
            f"{pr:.1f} kg"
        )

    with col2:
        st.metric(
            "🔥 Volume Total",
            f"{total_volume:,.1f} kg"
        )

    with col3:
        st.metric(
            "💪 Séries",
            int(total_sets)
        )

    with col4:
        st.metric(
            "📅 Último treino",
            last_workout
        )