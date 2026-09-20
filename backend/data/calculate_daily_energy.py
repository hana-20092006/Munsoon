import pandas as pd

INPUT_PATH = "data/processed/plant1_solar_weather.csv"
OUTPUT_PATH = "data/processed/daily_solar_energy.csv"


# ---------------------------------
# Load data
# ---------------------------------

df = pd.read_csv(INPUT_PATH)

df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

df = df.sort_values("DATE_TIME")


# ---------------------------------
# Calculate time interval
# ---------------------------------

df["interval_hours"] = (
    df["DATE_TIME"]
    .diff()
    .dt.total_seconds()
    / 3600
)


# ---------------------------------
# Keep only normal 15-minute intervals
# ---------------------------------

# We don't want large missing-data gaps
# to create incorrect energy calculations.

df["energy_kwh"] = (
    df["total_ac_power_kw"]
    * df["interval_hours"]
)

# Remove first row (no previous timestamp)
df = df.dropna(subset=["interval_hours"])

# Keep intervals of 15 minutes only
df = df[df["interval_hours"] == 0.25].copy()


# ---------------------------------
# Extract date
# ---------------------------------

df["DATE"] = df["DATE_TIME"].dt.date


# ---------------------------------
# Aggregate daily energy
# ---------------------------------

daily = (
    df.groupby("DATE")
    .agg(
        solar_energy_kwh=("energy_kwh", "sum"),
        peak_ac_power_kw=("total_ac_power_kw", "max"),
        total_irradiation=("IRRADIATION", "sum"),
        avg_irradiation=("IRRADIATION", "mean"),
    )
    .reset_index()
)


# ---------------------------------
# Save
# ---------------------------------

daily.to_csv(OUTPUT_PATH, index=False)


# ---------------------------------
# Display results
# ---------------------------------

print("===================================")
print("DAILY ENERGY CALCULATION")
print("===================================")

print("\nNumber of days:", len(daily))

print("\nDaily solar energy:")
print(daily.head(10))

print("\nStatistics:")
print(daily.describe())

print("\nHighest energy days:")
print(
    daily.nlargest(5, "solar_energy_kwh")
)

print("\nLowest energy days:")
print(
    daily.nsmallest(5, "solar_energy_kwh")
)

print("\nSaved to:")
print(OUTPUT_PATH)