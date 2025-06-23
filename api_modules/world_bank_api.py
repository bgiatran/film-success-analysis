import requests
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# Custom HTTPS adapter to handle strict SSL settings that can cause issues with some endpoints
class CustomHTTPAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # Relax SSL security level to avoid certificate verification failures
        context = create_urllib3_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")
        context.check_hostname = False
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

# Wrapper to handle GET requests to the World Bank API with basic error handling
def robust_world_bank_request(url, session):
    try:
        res = session.get(url, timeout=30)
        res.raise_for_status()
        return res
    except Exception as e:
        print(f"World Bank request failed: {e}")
        return None

# Fetch GDP and population data for all countries for a given year from the World Bank API
def fetch_gdp_population():
    # Define which indicators to pull from World Bank
    indicators = {
        "gdp": "NY.GDP.MKTP.CD",          # GDP (current US$)
        "population": "SP.POP.TOTL"       # Total population
    }
    year = "2022"  # Target year for data collection

    # Template for building the API request URL
    base_url = "http://api.worldbank.org/v2/country/all/indicator/{indicator}?date={year}&format=json"

    # Set up HTTP session with SSL override and a browser-like User-Agent
    session = requests.Session()
    session.mount("https://", CustomHTTPAdapter())
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    session.verify = certifi.where()

    data = {}

    # Loop over each indicator (GDP and Population)
    for key, indicator in indicators.items():
        url = base_url.format(indicator=indicator, year=year)
        res = robust_world_bank_request(url, session)
        if not res:
            continue
        json_data = res.json()

        # Ensure valid response format with expected data
        if len(json_data) < 2 or not json_data[1]:
            continue

        # Iterate over each country entry and store the data
        for entry in json_data[1]:
            code = entry.get("countryiso3code")
            value = entry.get("value")
            if code and value is not None:
                if code not in data:
                    data[code] = {}
                data[code][key] = value

    # Format the collected data into a clean list of dictionaries
    enriched = []
    for code, values in data.items():
        enriched.append({
            "iso_code": code,
            "gdp": values.get("gdp"),
            "population_gdp": values.get("population")
        })

    return enriched