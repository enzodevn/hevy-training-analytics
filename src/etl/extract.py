import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_PATH = BASE_DIR / "data" / "raw" / "hevy_workouts_full.json"
API_URL = "https://api.hevyapp.com/v1/workouts"
PAGE_SIZE = 10


def main():
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("HEVY_API_KEY")

    if not api_key:
        raise ValueError(
            "HEVY_API_KEY não encontrada. Configure a chave no arquivo .env."
        )

    headers = {"api-key": api_key}
    all_workouts = []

    print("Buscando treinos do Hevy...\n")

    response = requests.get(
        API_URL,
        headers=headers,
        params={"page": 1, "pageSize": PAGE_SIZE},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    page_count = data["page_count"]
    workouts = data["workouts"]
    all_workouts.extend(workouts)

    print(f"Página 1 carregada com {len(workouts)} treinos.")
    print(f"Total de páginas encontradas: {page_count}\n")

    for page in range(2, page_count + 1):
        response = requests.get(
            API_URL,
            headers=headers,
            params={"page": page, "pageSize": PAGE_SIZE},
            timeout=20,
        )
        response.raise_for_status()
        page_workouts = response.json()["workouts"]
        all_workouts.extend(page_workouts)
        print(f"Página {page} carregada com {len(page_workouts)} treinos.")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    final_data = {
        "total_workouts": len(all_workouts),
        "page_count": page_count,
        "workouts": all_workouts,
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as output_file:
        json.dump(final_data, output_file, ensure_ascii=False, indent=4)

    print("\n==============================")
    print("Extração concluída com sucesso!")
    print(f"Treinos totais baixados: {len(all_workouts)}")
    print(f"Arquivo salvo em: {OUTPUT_PATH}")
    print("==============================")


if __name__ == "__main__":
    main()