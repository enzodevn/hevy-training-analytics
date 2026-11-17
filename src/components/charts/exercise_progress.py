import plotly.express as px
import streamlit as st


def exercise_progress_chart(df, exercise_name):
    """
    Exibe a evolução da carga máxima do exercício.
    """

    if df.empty:
        st.warning("Nenhum dado encontrado para este exercício.")
        return

    # mantém apenas séries com peso
    df = df[df["weight_kg"].notna()].copy()

    if df.empty:
        st.warning("Este exercício não possui registros de carga.")
        return

    # maior carga registrada em cada treino
    progress = (
        df.groupby("workout_date", as_index=False)["weight_kg"]
        .max()
        .sort_values("workout_date")
    )

    fig = px.line(
        progress,
        x="workout_date",
        y="weight_kg",
        markers=True,
        title=f"Evolução da carga — {exercise_name}"
    )

    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Carga (kg)",
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )