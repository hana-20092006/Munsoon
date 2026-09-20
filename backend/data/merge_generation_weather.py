import pandas as pd

GENERATION_PATH = "data/processed/plant1_generation_clean.csv"
WEATHER_PATH = "data/raw/Plant_1_Weather_Sensor_Data.csv"
OUTPUT_PATH = "data/processed/plant1_solar_weather.csv"


# -----------------------------
# Load datasets
# -----------------------------

generation = pd.read_csv(GENERATION_PATH)
weather = pd.read_csv(WEATHER_PATH)


# -----------------------------
# Convert timestamps
# -----------------------------

generation["DATE_TIME"] = pd.to_datetime(
    generation["DATE_TIME"],
    errors="coerce"
)

weather["DATE_TIME"] = pd.to_datetime(
    weather["DATE_TIME"],
    errors="coerce"
)


# -----------------------------
# Check timestamp validity
# -----------------------------

print("Generation timestamp range:")
print(generation["DATE_TIME"].min(), "to", generation["DATE_TIME"].max())

print("\nWeather timestamp range:")
print(weather["DATE_TIME"].min(), "to", weather["DATE_TIME"].max())


# -----------------------------
# Check duplicate timestamps
# -----------------------------

print("\nGeneration duplicate timestamps:")
print(generation["DATE_TIME"].duplicated().sum())

print("\nWeather duplicate timestamps:")
print(weather["DATE_TIME"].duplicated().sum())


# -----------------------------
# Merge
# -----------------------------

merged = pd.merge(
    generation,
    weather,
    on="DATE_TIME",
    how="inner"
)


# -----------------------------
# Sort chronologically
# -----------------------------

merged = merged.sort_values("DATE_TIME")


# -----------------------------
# Save
# -----------------------------

merged.to_csv(OUTPUT_PATH, index=False)


# -----------------------------
# Report
# -----------------------------

print("\n===================================")
print("MERGE COMPLETED")
print("===================================")

print("\nGeneration rows:", len(generation))
print("Weather rows:", len(weather))
print("Merged rows:", len(merged))

print("\nMerged columns:")
print(merged.columns.tolist())

print("\nMissing values:")
print(merged.isnull().sum())

print("\nFirst 10 merged rows:")
print(merged.head(10))