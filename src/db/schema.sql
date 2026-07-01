DROP TABLE IF EXISTS workouts;
DROP TABLE IF EXISTS exercise_sets;

CREATE TABLE workouts (
    workout_id TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    start_time TEXT,
    end_time TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE exercise_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id TEXT,
    exercise_index INTEGER,
    exercise_name TEXT,
    exercise_template_id TEXT,
    superset_id TEXT,
    set_index INTEGER,
    set_type TEXT,
    weight_kg REAL,
    reps INTEGER,
    distance_meters REAL,
    duration_seconds REAL,
    rpe REAL,
    custom_metric TEXT,
    volume REAL,
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id)
);