import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

RAW_DATA_DIR = Path("data/raw")

DDL = """
CREATE TABLE IF NOT EXISTS raw_weather (
    city                TEXT NOT NULL,
    weather_date        DATE NOT NULL,
    temperature_2m_max  DOUBLE PRECISION,
    temperature_2m_min  DOUBLE PRECISION,
    precipitation_sum   DOUBLE PRECISION,
    windspeed_10m_max  DOUBLE PRECISION,
    PRIMARY KEY (city, weather_date)
);
"""

UPSERT = text("""
    INSERT INTO
            raw_weather (city, weather_date, temperature_2m_max, temperature_2m_min, precipitation_sum, windspeed_10m_max)
    VALUES
            (:city, :weather_date, :temperature_2m_max, :temperature_2m_min, :precipitation_sum, :windspeed_10m_max)
    ON CONFLICT (city, weather_date) DO UPDATE SET
            temperature_2m_max = EXCLUDED.temperature_2m_max,
            temperature_2m_min = EXCLUDED.temperature_2m_min,
            precipitation_sum = EXCLUDED.precipitation_sum,
            windspeed_10m_max = EXCLUDED.windspeed_10m_max
""")
    
def get_engine():
    u, p = os.environ["POSTGRES_USER"], os.environ["POSTGRES_PASSWORD"]
    h, port = os.environ["POSTGRES_HOST"], os.environ["POSTGRES_PORT"]
    db = os.environ["POSTGRES_DB"]
    return create_engine(f"postgresql+psycopg2://{u}:{p}@{h}:{port}/{db}")

def latest_parquet_file() -> Path:
    files = sorted(RAW_DATA_DIR.glob("weather_*.parquet"))
    if not files:
        raise FileNotFoundError("No parquet files found in data/raw")
    return files[-1]

def main() -> None:
    engine = get_engine()
    df = pd.read_parquet(latest_parquet_file())
    records = df.to_dict(orient="records")
    with engine.begin() as conn:
        conn.execute(text(DDL))
        conn.execute(UPSERT, records)
    logger.info("Upserted %d records into raw_weather (idempotently)", len(records))

if __name__ == "__main__":
    main()