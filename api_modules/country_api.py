import requests
import os
import pandas as pd
import pycountry

def get_language_details(code):
    """
    Attempts to convert a language code (like 'en' or 'fr') into a full language name and its ISO code.
    Returns a tuple: (language_name, iso_code)
    """
    try:
        language = pycountry.languages.get(alpha_2=code[:2])
        if language:
            return language.name, code[:2]
    except:
        pass
    return "Unknown", code

def fetch_language_market():
    """
    Fetches country and language data from the GeoNames API and saves it as a CSV.
    Each record links a country to the languages spoken there, including population size.
    """

    # GeoNames public API endpoint (requires a free username)
    url = "http://api.geonames.org/countryInfoJSON?username=bullibulli"
    output_path = os.path.join("data", "language_market.csv")

    try:
        print("🌐 Fetching from GeoNames Country Info API...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("geonames", [])
    except Exception as e:
        print(f"GeoNames API request failed: {e}")
        return []

    result = []

    for country in data:
        try:
            name = country.get("countryName", "").strip()
            capital = country.get("capital", "").strip()
            population = int(country.get("population", 0))
            languages = country.get("languages", "")

            # Skip entries without a country name or languages
            if not name or not languages:
                continue

            # Some countries have multiple languages separated by commas
            language_list = [lang.strip() for lang in languages.split(",") if lang.strip()]
            if not language_list:
                language_list = ["Unknown"]

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
            # Skip and log any bad records
            print(f"Skipping malformed entry: {err}")
            continue

    # Make sure the data folder exists
    os.makedirs("data", exist_ok=True)

    # Save the resulting language-country-population records to CSV
    df = pd.DataFrame(result)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} records to 'data/language_market.csv'")

    return result