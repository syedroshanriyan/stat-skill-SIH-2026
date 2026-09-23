import sqlite3
import os

db_paths = ['statskill.db', 'apps/api/statskill.db']

for db_path in db_paths:
    if not os.path.exists(db_path):
        continue
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(learning_resources)")
    cols = [r[1] for r in cursor.fetchall()]
    print(db_path, "existing columns:", cols)

    columns_to_add = [
        ("visibility", "TEXT DEFAULT 'PUBLIC'"),
        ("track_code", "TEXT DEFAULT 'GOVERNMENT'"),
        ("organization_id", "TEXT DEFAULT NULL"),
        ("owner_id", "TEXT DEFAULT NULL"),
        ("metadata_json", "TEXT DEFAULT '{}'")
    ]

    for col_name, col_def in columns_to_add:
        if col_name not in cols:
            try:
                cursor.execute(f"ALTER TABLE learning_resources ADD COLUMN {col_name} {col_def}")
                conn.commit()
                print(f"Added column {col_name} to {db_path}")
            except Exception as e:
                print(f"Error adding {col_name} to {db_path}: {e}")

    conn.close()

print("Schema migration complete.")
