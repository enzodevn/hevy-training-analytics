import streamlit as st
import plotly.express as px


def weekly_volume_chart(df):
    """
    Gráfico do volume semanal.
    """

    if df.empty:
        st.warning("Nenhum dado encontrado.")
        return

    x = (
        df["workout_year"].astype(str)
        + "-S"
        + df["workout_week"].astype(str)
    )

    fig = px.bar(
        df,
        x=x,
        y="weekly_volume",
        text="weekly_volume",
        title="📈 Volume semanal"
    )

    fig.update_layout(
        xaxis_title="Semana",
        yaxis_title="Volume (kg)",
        height=450
    )

    fig.update_traces(
        texttemplate="%{text:.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )