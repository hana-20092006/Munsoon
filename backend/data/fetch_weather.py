import requests
import pandas as pd

LATITUDE = 9.9312
LONGITUDE = 76.2673

START_DATE = "2025-06-01"
END_DATE = "2025-08-31"

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": [
        "temperature_2m",
        "precipitation",
        "cloud_cover",
        "shortwave_radiation",
        "wind_speed_10m"
    ],
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    raise Exception(
        f"Weather API request failed: {response.status_code}"
    )

data = response.json()

df = pd.DataFrame(data["hourly"])

df.rename(
    columns={
        "time": "timestamp",
        "temperature_2m": "temperature_c",
        "precipitation": "rainfall_mm",
        "cloud_cover": "cloud_cover_percent",
        "shortwave_radiation": "solar_radiation_wm2",
        "wind_speed_10m": "wind_speed_kmh"
    },
    inplace=True
)

output_path = "data/raw/kochi_weather_2025.csv"

df.to_csv(output_path, index=False)

print("Weather data downloaded successfully!")
print(f"Rows: {len(df)}")
print(f"Saved to: {output_path}")

print("\nFirst 5 rows:")
print(df.head())