import os
import pandas as pd
import sqlite3

# Define paths relative to the project root
# This keeps the script portable no matter where it's run from
project_root = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(project_root, "database", "film.db")
data_dir = os.path.join(project_root, "data")

# Establish connection to the SQLite database
conn = sqlite3.connect(db_path)
print(f"Connected to {db_path}")

# Dictionary mapping table names in the database to their corresponding CSV files
tables = {
    "movies": "movies.csv",
    "genres": "genres.csv",
    "cast": "cast.csv",
    "language_market": "language_market.csv",
    "world_bank_data": "world_bank_data.csv"
}

# Loop through each table and load data from its CSV file
for table, file in tables.items():
    file_path = os.path.join(data_dir, file)

    if os.path.exists(file_path):
        # Read the CSV into a DataFrame and write it to the corresponding SQL table
        df = pd.read_csv(file_path)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"Loaded {len(df)} rows into '{table}' from {file}")
    else:
        # Warn if any expected CSV file is missing
        print(f"Missing: {file}")

# Close the database connection
conn.close()
print("Database now populated from CSVs!")