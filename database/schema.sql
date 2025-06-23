-- Updated Film Analysis Schema

-- Stores core metadata for each film. Each movie gets a unique ID.
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,  -- Unique identifier for each movie
    title TEXT,                    -- Movie title
    release_date DATE,            -- When the movie was released
    budget REAL,                  -- Production budget in dollars
    revenue REAL,                 -- Box office revenue in dollars
    language TEXT                 -- Primary spoken language
);

-- Holds genre info per movie. Allows multiple genres per movie.
CREATE TABLE IF NOT EXISTS genres (
    movie_id INTEGER,             -- Links to the corresponding movie
    genre TEXT,                   -- One genre per row (e.g., Action, Drama)
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

-- Stores cast information for each movie. Also allows many-to-one relationships.
CREATE TABLE IF NOT EXISTS cast (
    movie_id INTEGER,             -- Movie reference
    actor TEXT,                   -- Name of an actor in the cast
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

-- Maps languages to global market data.
-- Useful for analyzing potential audience size and regional revenue insights.
CREATE TABLE IF NOT EXISTS language_market (
    language TEXT,                -- Language code or name (e.g., "en", "Spanish")
    population INTEGER,           -- Total population of speakers or regional reach
    country TEXT                  -- Associated country (used for mapping or breakdown)
);

-- Stores macroeconomic data used for context in revenue analysis.
-- Tied to country codes rather than movies.
CREATE TABLE IF NOT EXISTS world_bank_data (
    iso_code TEXT PRIMARY KEY,    -- ISO Alpha-3 country code (e.g., "USA", "FRA")
    gdp REAL,                     -- Gross Domestic Product of the country
    population_gdp REAL           -- Population figure associated with GDP data
);