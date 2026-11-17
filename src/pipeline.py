"""
Pipeline principal do Hevy Training Analytics

Fluxo:

1. Extrai dados da API
2. Transforma os dados
3. Atualiza o SQLite
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def run_step(script_name, description):
    print("\n" + "=" * 60)
    print(description)
    print("=" * 60)

    script = BASE_DIR / "etl" / script_name

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=BASE_DIR.parent
    )

    if result.returncode != 0:
        print(f"\nERRO durante: {description}")
        sys.exit(result.returncode)

    print(f"{description} concluído.")


def main():

    print("\nHEVY TRAINING ANALYTICS")
    print("Iniciando Pipeline...\n")

    run_step(
        "extract.py",
        "1/3 Extraindo dados da API"
    )

    run_step(
        "transform_full.py",
        "2/3 Transformando dados"
    )

    run_step(
        "load_to_sqlite.py",
        "3/3 Atualizando banco SQLite"
    )

    print("\n" + "=" * 60)
    print("PIPELINE EXECUTADO COM SUCESSO")
    print("=" * 60)


if __name__ == "__main__":
    main()