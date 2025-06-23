import requests
import time
import os
import certifi
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Custom HTTPS adapter to work around SSL issues on some machines
class CustomHTTPSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # Lower SSL security level to avoid handshake issues
        context = create_urllib3_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")
        context.check_hostname = False
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

# Create a requests session with better error handling and certs
def create_robust_session():
    session = requests.Session()
    session.mount("https://", CustomHTTPSAdapter())
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    session.verify = certifi.where()  # Use certifi for trusted SSL certs
    return session

# Wrapper to retry GET requests a few times if they fail
def robust_get(session, url, retries=2):
    for attempt in range(retries):
        try:
            res = session.get(url, timeout=30)
            res.raise_for_status()
            return res
        except Exception as e:
            print(f"Request failed (attempt {attempt + 1}): {e}")
            time.sleep(1)
    return None  # Return None after final attempt fails

# Fetch top-grossing movies sorted by revenue (descending)
def fetch_top_movies(pages=3):
    if not API_KEY:
        print("TMDB_API_KEY not found")
        return []

    session = create_robust_session()
    movies = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&sort_by=revenue.desc&page={page}"
        res = robust_get(session, url)
        if res:
            data = res.json()
            if "results" in data:
                movies.extend(data["results"])
                print(f"Fetched page {page}")
        else:
            print(f"Failed to fetch page {page}")

    return movies

# Fetch low-revenue movies (likely flops), with a minimum vote count filter
def fetch_flop_movies(pages=3):
    """
    Fetch low-revenue movies (potential flops) using TMDB API.
    These are sorted in ascending order by revenue.
    Only includes movies with at least 10 votes to avoid noise.
    """
    if not API_KEY:
        print("TMDB_API_KEY not found")
        return []

    session = create_robust_session()
    movies = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&sort_by=revenue.asc&page={page}&vote_count.gte=10"
        res = robust_get(session, url)
        if res:
            data = res.json()
            if "results" in data:
                movies.extend(data["results"])
                print(f"Fetched flop page {page}")
        else:
            print(f"Failed to fetch flop page {page}")

    return movies

# Get detailed movie metadata including credits (cast, crew, etc.)
def get_movie_details(movie_id):
    if not API_KEY:
        return None

    session = create_robust_session()
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"
    res = robust_get(session, url)
    return res.json() if res else None