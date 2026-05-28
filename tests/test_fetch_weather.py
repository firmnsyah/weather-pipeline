from ingestion.fetch_weather import to_dataframe

def test_to_dataframe_shape():
    payload = {
        "daily": {
            "time": ["2026-05-28", "2026-05-29"],
            "temperature_2m_max": [31.0, 32.5],
            "temperature_2m_min": [24.0, 24.5],
            "precipitation_sum": [0.0, 3.2],
            "windspeed_10m_max": [12.0, 15.0],
        }
    }
    df = to_dataframe("Jakarta", payload)
    assert list(df["city"].unique()) == ["Jakarta"]
    assert "weather_date" in df.columns
    assert len(df) == 2