import pandas as pd

PATH = "data/processed/plant1_solar_weather.csv"

df = pd.read_csv(PATH)

print("===================================")
print("WEATHER FEATURES")
print("===================================")

features = [
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION"
]

for feature in features:
    print(f"\n{feature}")
    print(df[feature].describe())


print("\n===================================")
print("CORRELATION WITH AC POWER")
print("===================================")

weather_columns = [
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION"
]

print(
    df[
        weather_columns + ["total_ac_power_kw"]
    ].corr()["total_ac_power_kw"]
    .sort_values(ascending=False)
)


print("\n===================================")
print("TIME FEATURES")
print("===================================")

df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

df["hour"] = df["DATE_TIME"].dt.hour
df["minute"] = df["DATE_TIME"].dt.minute

print("\nHours present:")
print(sorted(df["hour"].unique()))

print("\nMinutes present:")
print(sorted(df["minute"].unique()))