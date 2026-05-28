import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

RAW_DATA_DIR = Path("data/raw")

def get_engine():
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    db = os.environ["POSTGRES_DB"]
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

def latest_parquet_file() -> Path:
    files = sorted(RAW_DATA_DIR.glob("weather_*.parquet"))
    if not files:
        raise FileNotFoundError("No parquet files found in data/raw")
    return files[-1]

def main() -> None:
    engine = get_engine()
    path = latest_parquet_file()
    df = pd.read_parquet(path)
    df.to_sql("raw_weather", engine, if_exists="replace", index=False)
    logger.info("Loaded %d rows from %s to raw_weather", len(df), path.name)

if __name__ == "__main__":
    main()