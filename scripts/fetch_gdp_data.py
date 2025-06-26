# fetch_gdp_data.py – Fixed column names + enhancements
# Author: Bria Tran
# Description: This script fetches the most recent GDP and population data per country
# using the World Bank API, skips already-existing entries, caches results, and stores
# values in a SQLite database for downstream analysis.

import sqlite3
import requests
import time
import os
import pycountry
import pandas as pd
from tqdm import tqdm  # Visual progress bar for loops

# Configuration Constants

# Year to fetch data for (can be changed based on availability)
YEAR = 2023

# Paths for database and cache file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "film.db")
CACHE_CSV = "gdp_population_cache.csv"

# API endpoints (World Bank indicators)
GDP_API = "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json"
POP_API = "https://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?format=json"

# Helper Function: API Request

def fetch_latest_value(api_url, code):
    """
    Queries the specified World Bank API endpoint for a given ISO country code.
    Returns the value for the configured year (e.g., 2023) if available.
    """
    try:
        resp = requests.get(api_url.format(code), timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Validate API response structure
        if not data or len(data) < 2 or not data[1]:
            return None

        # Return first valid value from the correct year
        for entry in data[1]:
            if entry["value"] is not None and int(entry["date"]) == YEAR:
                return float(entry["value"])
        return None
    except Exception as e:
        print(f"[ERROR] {code}: {e}")
        return None

# Main Pipeline

def main():
    # Establish SQLite connection and initialize table if not exists
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS world_bank_data (
            iso_code TEXT PRIMARY KEY,
            gdp REAL,
            population_gdp INTEGER
        )
    """)
    conn.commit()

    # Get list of ISO codes already stored to avoid duplicate requests
    cur.execute("SELECT iso_code FROM world_bank_data")
    existing = {row[0] for row in cur.fetchall()}

    cached = []  # In-memory cache to write out to CSV

    # Loop through all recognized countries using pycountry
    for country in tqdm(pycountry.countries, desc="Fetching GDP & Population"):
        code = country.alpha_3
        if code in existing:
            continue  # Skip already-inserted countries

        # Fetch GDP and population data (with slight delay to avoid rate limits)
        gdp = fetch_latest_value(GDP_API, code)
        time.sleep(0.05)
        pop = fetch_latest_value(POP_API, code)
        time.sleep(0.05)

        # Only insert if at least one value was successfully fetched
        if gdp is not None or pop is not None:
            cur.execute("""
                INSERT INTO world_bank_data (iso_code, gdp, population_gdp)
                VALUES (?, ?, ?)
            """, (code, gdp, int(pop) if pop is not None else None))
            conn.commit()

            # Track this entry for the CSV cache
            cached.append({"iso_code": code, "gdp": gdp, "population_gdp": pop})

    # Save cached results to CSV for future debugging and re-runs
    if cached:
        pd.DataFrame(cached).to_csv(CACHE_CSV, index=False)
        print(f"Cached new data to {CACHE_CSV}")
    else:
        print("No new countries were added.")

    # Close DB connection
    conn.close()

# Entry Point
if __name__ == "__main__":
    main()