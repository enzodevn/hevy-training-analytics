import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HEVY_API_KEY")

if not api_key:
    raise ValueError("HEVY_API_KEY não encontrada no arquivo .env")

headers = {
    "api-key": api_key
}

base_url = "https://api.hevyapp.com/v1/workouts"
page_size = 10

all_workouts = []

print("Buscando treinos do Hevy...\n")

# ---------
# 1) Busca a primeira página
# ---------
first_page_url = f"{base_url}?page=1&pageSize={page_size}"

response = requests.get(first_page_url, headers=headers, timeout=20)
response.raise_for_status()

data = response.json()

page_count = data["page_count"]
workouts = data["workouts"]

all_workouts.extend(workouts)

print(f"Página 1 carregada com {len(workouts)} treinos.")
print(f"Total de páginas encontradas: {page_count}\n")

# ---------
# 2) Busca as demais páginas
# ---------
for page in range(2, page_count + 1):
    url = f"{base_url}?page={page}&pageSize={page_size}"

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    page_data = response.json()
    page_workouts = page_data["workouts"]

    all_workouts.extend(page_workouts)

    print(f"Página {page} carregada com {len(page_workouts)} treinos.")

# ---------
# 3) Monta JSON final
# ---------
final_data = {
    "total_workouts": len(all_workouts),
    "page_count": page_count,
    "workouts": all_workouts
}

# ---------
# 4) Salva JSON completo
# ---------
output_path = "data/raw/hevy_workouts_full.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print("\n==============================")
print("Extração concluída com sucesso!")
print(f"Treinos totais baixados: {len(all_workouts)}")
print(f"Arquivo salvo em: {output_path}")
print("==============================")