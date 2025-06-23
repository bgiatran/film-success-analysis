# scripts/init_db.py
import sqlite3
import os

def run_schema():
    """
    Applies the database schema from schema.sql to film.db.
    This script sets up the structure for the film analysis database.
    """

    # Get the root directory of the project so we can build paths reliably
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Build absolute paths to the database file and schema file
    db_path = os.path.join(base_dir, "database", "film.db")
    schema_path = os.path.join(base_dir, "database", "schema.sql")

    # Read the entire schema.sql file as one string of SQL commands
    with open(schema_path, "r") as f:
        schema = f.read()
    conn = sqlite3.connect(db_path)

    # Run all SQL statements in schema.sql at once (e.g., CREATE TABLEs, indexes, etc.)
    conn.executescript(schema)

    # Commit changes to ensure the schema is fully applied to the database
    conn.commit()
    conn.close()
    print("Schema applied successfully to film.db")

# Only run the function if this script is executed directly (not imported)
if __name__ == "__main__":
    run_schema()