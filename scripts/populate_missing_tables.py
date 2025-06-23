import pandas as pd
import sqlite3

# Connect to the SQLite database where all project data is stored
# Assumes the 'film.db' database already exists and schema is defined
conn = sqlite3.connect("database/film.db")

# Read the cleaned CSV data into DataFrames
# These files should already be preprocessed and formatted to match the table schemas
lang_df = pd.read_csv("data/language_market.csv")
gdp_df = pd.read_csv("data/world_bank_data.csv")

# Insert data into the corresponding tables in the database
# if_exists="replace" will drop the existing table (if any) and recreate it with new data
lang_df.to_sql("language_market", conn, if_exists="replace", index=False)
gdp_df.to_sql("world_bank_data", conn, if_exists="replace", index=False)

# Print confirmation message for feedback
print("language_market and world_bank_data inserted into film.db")
conn.close()