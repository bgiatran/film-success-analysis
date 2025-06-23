# scripts/fetch_gdp_data.py

import sqlite3, requests, time, os
import pycountry

# Constants
YEAR = 2023  # Target year for GDP and population data
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "film.db")

# World Bank API endpoints for GDP (in current US$) and total population
GDP_API = "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json"
POP_API = "https://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?format=json"

def fetch_latest_value(api_url, code):
    """
    Fetches the latest available value for a given indicator and country ISO code.
    Filters for the specific target year (e.g., 2023) and returns None if unavailable.
    """
    try:
        resp = requests.get(api_url.format(code), timeout=10)
        resp.raise_for_status()  # Raise an error for bad HTTP status
        data = resp.json()

        # Check if the response is well-formed and contains data
        if not data or len(data) < 2 or not data[1]:
            return None

        # Loop through the entries and find the value for the specific year
        for entry in data[1]:
            if entry["value"] is not None and int(entry["date"]) == YEAR:
                return float(entry["value"])
        return None
    except Exception as e:
        print(f"[ERROR] {code}: {e}")
        return None

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Clear any existing data in the world_bank_data table
    cur.execute("DELETE FROM world_bank_data")

    success, fail = 0, 0  # Counters for tracking insert success/failure

    # Loop through all countries defined by ISO using pycountry
    for country in pycountry.countries:
        code = country.alpha_3  # Use the ISO Alpha-3 code (e.g., "USA", "JPN")
        gdp = fetch_latest_value(GDP_API, code)
        pop = fetch_latest_value(POP_API, code)

        # Only insert data if we got at least one value
        if gdp is not None or pop is not None:
            cur.execute("""
                INSERT INTO world_bank_data (iso_code, gdp, population_gdp)
                VALUES (?, ?, ?)
            """, (code, gdp, pop))
            success += 1
        else:
            fail += 1

        # Pause to avoid hitting API rate limits (very basic throttle)
        time.sleep(0.2)

    # Commit changes and close DB connection
    conn.commit()
    conn.close()
    print(f"Inserted {success} rows. Missed {fail}.")

# Run script only if executed directly (not imported)
if __name__ == "__main__":
    main()