import pandas as pd

INPUT_PATH = "data/raw/Plant_1_Generation_Data.csv"
OUTPUT_PATH = "data/processed/plant1_generation_clean.csv"

EXPECTED_INVERTERS = 22

# Load data
df = pd.read_csv(INPUT_PATH)

# Parse timestamp
df["DATE_TIME"] = pd.to_datetime(
    df["DATE_TIME"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

# Check timestamp conversion
if df["DATE_TIME"].isna().any():
    print("WARNING: Some timestamps could not be parsed.")

# Count inverter records per timestamp
records_per_timestamp = (
    df.groupby("DATE_TIME")["SOURCE_KEY"]
    .nunique()
)

# Keep timestamps with all 22 inverter readings
valid_timestamps = records_per_timestamp[
    records_per_timestamp == EXPECTED_INVERTERS
].index

clean_df = df[df["DATE_TIME"].isin(valid_timestamps)].copy()

# Aggregate plant-level generation
plant_generation = (
    clean_df
    .groupby("DATE_TIME")
    .agg(
        total_dc_power_kw=("DC_POWER", "sum"),
        total_ac_power_kw=("AC_POWER", "sum"),
        total_daily_yield=("DAILY_YIELD", "sum")
    )
    .reset_index()
)

# Sort chronologically
plant_generation = plant_generation.sort_values("DATE_TIME")

# Save
plant_generation.to_csv(OUTPUT_PATH, index=False)

print("Generation data prepared successfully!")

print("\nOriginal rows:", len(df))
print("Clean rows:", len(clean_df))
print("Unique timestamps retained:", len(plant_generation))

print("\nPrepared columns:")
print(plant_generation.columns.tolist())

print("\nFirst 10 rows:")
print(plant_generation.head(10))

print("\nMissing values:")
print(plant_generation.isnull().sum())