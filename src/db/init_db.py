import sqlite3
from pathlib import Path

DB_PATH = Path("data/hevy.db")
SCHEMA_PATH = Path("src/db/schema.sql")

print("Inicializando banco...")
print(f"DB_PATH: {DB_PATH.resolve()}")
print(f"SCHEMA_PATH: {SCHEMA_PATH.resolve()}")

# garantir que a pasta data existe
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# verificar se schema existe
if not SCHEMA_PATH.exists():
    raise FileNotFoundError(f"Arquivo schema não encontrado: {SCHEMA_PATH}")

# ler schema
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = f.read()

print("\nConteúdo do schema carregado com sucesso.")
print("-" * 50)
print(schema)
print("-" * 50)

# conectar e executar schema
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript(schema)
conn.commit()

# verificar tabelas criadas
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""")
tables = cursor.fetchall()

conn.close()

print("\nBanco criado com sucesso!")
print(f"Arquivo: {DB_PATH}")
print("Tabelas encontradas:")
for table in tables:
    print("-", table[0])