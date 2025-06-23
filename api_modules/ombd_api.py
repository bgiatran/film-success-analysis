import requests
import os
import pandas as pd
import pycountry

def get_language_details(code):
    """
    Converts a language code (e.g., 'en', 'fr') into a full language name using the pycountry library.
    Only the first two characters of the code are used (GeoNames sometimes returns compound codes like 'en-US').
    Returns a tuple of the form: (language_name, iso_code)
    If the code can't be resolved, it returns ("Unknown", code).
    """
    try:
        language = pycountry.languages.get(alpha_2=code[:2])
        if language:
            return language.name, code[:2]
    except:
        pass  # Silently skip any bad codes or lookup errors
    return "Unknown", code

def fetch_language_market():
    """
    Fetches a list of countries from the GeoNames CountryInfo API and extracts language + population info.
    For each language spoken in a country, we store:
        - country name
        - capital
        - language name
        - ISO language code
        - total country population
    Saves the data into a CSV file at: data/language_market.csv
    """

    # GeoNames public API endpoint. A valid username is required (here, using 'bullibulli')
    url = "http://api.geonames.org/countryInfoJSON?username=bullibulli"
    output_path = os.path.join("data", "language_market.csv")

    try:
        print("🌐 Fetching from GeoNames Country Info API...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error if the HTTP response was unsuccessful
        data = response.json().get("geonames", [])
    except Exception as e:
        print(f"GeoNames API request failed: {e}")
        return []

    result = []

    # Loop through each country in the GeoNames response
    for country in data:
        try:
            name = country.get("countryName", "").strip()
            capital = country.get("capital", "").strip()
            population = int(country.get("population", 0))
            languages = country.get("languages", "")

            # Skip if required fields are missing
            if not name or not languages:
                continue

            # Some countries have multiple languages listed like 'en,fr,de'
            language_list = [lang.strip() for lang in languages.split(",") if lang.strip()]
            if not language_list:
                language_list = ["Unknown"]

            # Add a row for each language spoken in the country
            for lang_code in language_list:
                lang_name, iso_code = get_language_details(lang_code)

                result.append({
                    "country": name,
                    "capital": capital,
                    "language_code": iso_code,
                    "language": lang_name,
                    "population": population
                })

        except Exception as err:
            # If anything goes wrong with this country entry, just skip it
            print(f"Skipping malformed entry: {err}")
            continue

    # Ensure the output directory exists before saving
    os.makedirs("data", exist_ok=True)

    # Convert result list to a DataFrame and write to CSV
    df = pd.DataFrame(result)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} records to 'data/language_market.csv'")

    return result