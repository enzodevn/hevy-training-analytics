import streamlit as st


def render_exercise_selector(df):
    """
    Renderiza o seletor de exercícios.
    """

    exercise = st.selectbox(
        "Escolha um exercício",
        df["exercise_name"]
    )

    return exercise