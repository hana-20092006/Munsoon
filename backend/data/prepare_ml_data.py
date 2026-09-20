import pandas as pd

INPUT_PATH = "data/processed/plant1_solar_weather.csv"
OUTPUT_PATH = "data/processed/ml_solar_dataset.csv"


# ---------------------------------
# Load data
# ---------------------------------

df = pd.read_csv(INPUT_PATH)

df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

df = df.sort_values("DATE_TIME").reset_index(drop=True)


# ---------------------------------
# Create time features
# ---------------------------------

df["hour"] = df["DATE_TIME"].dt.hour

df["minute"] = df["DATE_TIME"].dt.minute

df["day_of_year"] = df["DATE_TIME"].dt.dayofyear


# ---------------------------------
# Select ML features
# ---------------------------------

features = [
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION",
    "hour",
    "minute",
    "day_of_year"
]

target = "total_ac_power_kw"


ml_df = df[
    ["DATE_TIME"] + features + [target]
].copy()


# ---------------------------------
# Remove missing values
# ---------------------------------

ml_df = ml_df.dropna()


# ---------------------------------
# Save
# ---------------------------------

ml_df.to_csv(OUTPUT_PATH, index=False)


# ---------------------------------
# Report
# ---------------------------------

print("===================================")
print("ML DATASET PREPARED")
print("===================================")

print("\nShape:")
print(ml_df.shape)

print("\nFeatures:")
print(features)

print("\nTarget:")
print(target)

print("\nMissing values:")
print(ml_df.isnull().sum())

print("\nFirst 10 rows:")
print(ml_df.head(10))

print("\nTarget statistics:")
print(ml_df[target].describe())

print("\nSaved to:")
print(OUTPUT_PATH)