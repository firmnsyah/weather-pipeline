import json
import logging
from datetime import date
from pathlib import Path
from venv import logger

import pandas as pd
import requests

from config.cities import CITIES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

FORECAST_URL = "https://api.open-meteo.com/v1/forecast" 
DAILY_VARS = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "windspeed_10m_max"]
RAW_DATA_DIR = Path("data/raw")

def fetch_city(city: dict) -> dict:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "daily": ",".join(DAILY_VARS),
        "timezone": "auto",
        "past_days": 7,
        "forecast_days": 7,
    }
    logger.info(f"Fetching weather data for {city['city']}")
    response = requests.get(FORECAST_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def to_dataframe(city_name: str, payload: dict) -> pd.DataFrame:
    daily = payload["daily"]
    df = pd.DataFrame(daily)
    df = df.rename(columns={"time": "weather_date"})
    df.insert(0, "city", city_name)
    return df

def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    run_date = date.today().isoformat()
    frames = []

    for city in CITIES:
        payload = fetch_city(city)
        raw_path = RAW_DATA_DIR / f"{city['city'].lower()}_{run_date}.json"
        raw_path.write_text(json.dumps(payload), encoding="utf-8")
        frames.append(to_dataframe(city["city"], payload))
    
    combined_df = pd.concat(frames, ignore_index=True)
    output_path = RAW_DATA_DIR / f"weather_{run_date}.parquet"
    combined_df.to_parquet(output_path, index=False)
    logger.info(f"Weather data saved %d rows to %s", len(combined_df), output_path)

if __name__ == "__main__":
    main()