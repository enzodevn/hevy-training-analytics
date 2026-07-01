import pandas as pd

# -----------------------------
# 1) Ler base tratada completa
# -----------------------------
df = pd.read_csv("data/processed/hevy_exercises_full.csv")

# -----------------------------
# 2) Garantir tipos
# -----------------------------
df["workout_start"] = pd.to_datetime(df["workout_start"], errors="coerce")
df["workout_end"] = pd.to_datetime(df["workout_end"], errors="coerce")
df["workout_date"] = pd.to_datetime(df["workout_date"], errors="coerce")

# -----------------------------
# 3) Métricas gerais
# -----------------------------
total_rows = len(df)
total_workouts = df["workout_id"].nunique()
total_exercises = df["exercise"].nunique()
total_sets = len(df)

total_volume = df["volume"].fillna(0).sum()

avg_workout_duration = (
    df.groupby("workout_id")["workout_duration_min"]
    .max()
    .mean()
)

longest_workout = (
    df.groupby(["workout_id", "workout_title"])["workout_duration_min"]
    .max()
    .sort_values(ascending=False)
    .head(1)
)

# -----------------------------
# 4) Exercícios mais frequentes
# -----------------------------
top_exercises_by_sets = (
    df.groupby("exercise")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

# -----------------------------
# 5) Exercícios com maior volume
# -----------------------------
top_exercises_by_volume = (
    df.groupby("exercise")["volume"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# -----------------------------
# 6) PRs (maior carga por exercício)
# -----------------------------
prs = (
    df.groupby("exercise")["weight_kg"]
    .max()
    .sort_values(ascending=False)
    .head(15)
)

# -----------------------------
# 7) Volume por treino
# -----------------------------
volume_per_workout = (
    df.groupby(["workout_date", "workout_title"])["volume"]
    .sum()
    .sort_values(ascending=False)
)

# -----------------------------
# 8) Volume semanal
# -----------------------------
weekly_volume = (
    df.groupby(["workout_year", "workout_week"])["volume"]
    .sum()
    .reset_index()
    .sort_values(["workout_year", "workout_week"])
)

weekly_workouts = (
    df.groupby(["workout_year", "workout_week"])["workout_id"]
    .nunique()
    .reset_index(name="workouts_count")
    .sort_values(["workout_year", "workout_week"])
)

# -----------------------------
# 9) Resumo por tipo de set
# -----------------------------
set_type_summary = (
    df.groupby("set_type")
    .size()
    .sort_values(ascending=False)
)

# -----------------------------
# 10) Impressão do relatório
# -----------------------------
print("\n" + "=" * 50)
print("HEVY ANALYTICS REPORT")
print("=" * 50)

print("\n[GERAL]")
print(f"Linhas na base: {total_rows}")
print(f"Treinos únicos: {total_workouts}")
print(f"Exercícios únicos: {total_exercises}")
print(f"Séries totais: {total_sets}")
print(f"Volume total levantado: {total_volume:,.2f} kg")
print(f"Duração média dos treinos: {avg_workout_duration:.2f} min")

print("\n[MAIOR TREINO POR DURAÇÃO]")
print(longest_workout)

print("\n[TOP 10 EXERCÍCIOS POR NÚMERO DE SÉRIES]")
print(top_exercises_by_sets)

print("\n[TOP 10 EXERCÍCIOS POR VOLUME]")
print(top_exercises_by_volume)

print("\n[TOP 15 PRs (maior carga por exercício)]")
print(prs)

print("\n[VOLUME POR TREINO - TOP 10]")
print(volume_per_workout.head(10))

print("\n[VOLUME SEMANAL]")
print(weekly_volume)

print("\n[FREQUÊNCIA SEMANAL DE TREINOS]")
print(weekly_workouts)

print("\n[RESUMO POR TIPO DE SÉRIE]")
print(set_type_summary)

# -----------------------------
# 11) Salvar outputs analíticos
# -----------------------------
top_exercises_by_sets.to_csv(
    "data/processed/top_exercises_by_sets.csv",
    header=["sets_count"]
)

top_exercises_by_volume.to_csv(
    "data/processed/top_exercises_by_volume.csv",
    header=["total_volume"]
)

prs.to_csv(
    "data/processed/prs_by_exercise.csv",
    header=["max_weight_kg"]
)

volume_per_workout.to_csv(
    "data/processed/volume_per_workout.csv",
    header=["total_volume"]
)

weekly_volume.to_csv(
    "data/processed/weekly_volume.csv",
    index=False
)

weekly_workouts.to_csv(
    "data/processed/weekly_workouts.csv",
    index=False
)

print("\nArquivos analíticos salvos em data/processed/")
print("- top_exercises_by_sets.csv")
print("- top_exercises_by_volume.csv")
print("- prs_by_exercise.csv")
print("- volume_per_workout.csv")
print("- weekly_volume.csv")
print("- weekly_workouts.csv")