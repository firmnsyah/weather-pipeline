-- City Dimension
CREATE TABLE dim_city (
    city_id     SERIAL PRIMARY KEY,
    city_name   TEXT NOT NULL UNIQUE,
    latitude    DOUBLE PRECISION,
    longitude   DOUBLE PRECISION
);

-- Date Dimension
CREATE TABLE dim_date (
    date_key    INTEGER PRIMARY KEY,
    full_date   DATE NOT NULL,
    year        INTEGER,
    month       INTEGER,
    day         INTEGER,
    day_of_week INTEGER,
);

-- Fact Table: Weather Daily per City (grain: 1 city x 1 day)
CREATE TABLE fact_weather_daily (
    city_key            INTEGER REFERENCES dim_city(city_id),
    date_key            INTEGER REFERENCES dim_date(date_key),
    temp_max            DOUBLE PRECISION,
    temp_min            DOUBLE PRECISION,
    precipitation_sum   DOUBLE PRECISION,
    windspeed_max       DOUBLE PRECISION,
    PRIMARY KEY (city_key, date_key)
);