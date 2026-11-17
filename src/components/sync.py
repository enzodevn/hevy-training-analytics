import subprocess
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
PIPELINE_PATH = ROOT_DIR / "src" / "pipeline.py"
SYNC_TIMEOUT_SECONDS = 600


def _run_pipeline():
    try:
        result = subprocess.run(
            [sys.executable, str(PIPELINE_PATH)],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            timeout=SYNC_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stderr or exc.stdout or ""
        return (
            False,
            f"A sincronização excedeu {SYNC_TIMEOUT_SECONDS} segundos.\n{output}",
        )
    except OSError as exc:
        return False, f"Não foi possível iniciar a sincronização: {exc}"

    output = "\n".join(
        part for part in (result.stdout, result.stderr) if part
    )
    return result.returncode == 0, output or "Pipeline concluído sem mensagens."


def _show_sync_result():
    sync_result = st.session_state.pop("hevy_sync_result", None)
    if sync_result:
        succeeded, output = sync_result
        if succeeded:
            st.success("Dados do Hevy atualizados com sucesso.")
        else:
            st.error("Falha ao atualizar os dados do Hevy.")
        with st.expander("Detalhes da sincronização"):
            st.code(output)


def render_sync_button():
    if not st.session_state.get("hevy_auto_sync_attempted"):
        st.session_state["hevy_auto_sync_attempted"] = True
        with st.spinner("Atualizando dados do Hevy ao abrir o dashboard..."):
            st.session_state["hevy_sync_result"] = _run_pipeline()

    if st.button("🔄 Atualizar dados do Hevy"):
        with st.spinner("Buscando treinos no Hevy e atualizando o dashboard..."):
            st.session_state["hevy_sync_result"] = _run_pipeline()

        if st.session_state["hevy_sync_result"][0]:
            st.rerun()

    _show_sync_result()
