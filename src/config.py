from pathlib import Path

# raiz do projeto: hevy_pipeline/
BASE_DIR = Path(__file__).resolve().parent.parent

# caminhos úteis
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "hevy.db"