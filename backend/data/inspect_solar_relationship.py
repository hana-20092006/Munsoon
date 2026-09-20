import pandas as pd

PATH = "data/processed/plant1_solar_weather.csv"

df = pd.read_csv(PATH)

df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

# ---------------------------------
# Basic statistics
# ---------------------------------

print("===================================")
print("BASIC STATISTICS")
print("===================================")

print("\nShape:")
print(df.shape)

print("\nNumeric statistics:")
print(
    df[
        [
            "total_dc_power_kw",
            "total_ac_power_kw",
            "total_daily_yield",
            "AMBIENT_TEMPERATURE",
            "MODULE_TEMPERATURE",
            "IRRADIATION",
        ]
    ].describe()
)


# ---------------------------------
# Zero-generation analysis
# ---------------------------------

print("\n===================================")
print("ZERO GENERATION ANALYSIS")
print("===================================")

zero_ac = (df["total_ac_power_kw"] == 0).sum()
zero_dc = (df["total_dc_power_kw"] == 0).sum()
zero_irradiation = (df["IRRADIATION"] == 0).sum()

print("Zero AC power:", zero_ac)
print("Zero DC power:", zero_dc)
print("Zero irradiation:", zero_irradiation)


# ---------------------------------
# Correlation
# ---------------------------------

print("\n===================================")
print("CORRELATION WITH AC POWER")
print("===================================")

correlations = df[
    [
        "total_ac_power_kw",
        "total_dc_power_kw",
        "total_daily_yield",
        "AMBIENT_TEMPERATURE",
        "MODULE_TEMPERATURE",
        "IRRADIATION",
    ]
].corr()

print(
    correlations["total_ac_power_kw"]
    .sort_values(ascending=False)
)


# ---------------------------------
# Time interval analysis
# ---------------------------------

print("\n===================================")
print("TIME INTERVAL ANALYSIS")
print("===================================")

time_diff = df["DATE_TIME"].diff().dt.total_seconds() / 60

print("\nTime difference statistics (minutes):")
print(time_diff.describe())

print("\nMost common time intervals:")
print(time_diff.value_counts().head(10))


# ---------------------------------
# Daily aggregation
# ---------------------------------

print("\n===================================")
print("DAILY GENERATION")
print("===================================")

df["DATE"] = df["DATE_TIME"].dt.date

daily = (
    df.groupby("DATE")
    .agg(
        max_ac_power=("total_ac_power_kw", "max"),
        total_ac_power=("total_ac_power_kw", "sum"),
        max_irradiation=("IRRADIATION", "max"),
        total_irradiation=("IRRADIATION", "sum"),
    )
    .reset_index()
)

print("\nNumber of days:", len(daily))

print("\nFirst 10 days:")
print(daily.head(10))

print("\nDaily generation statistics:")
print(daily.describe())


# ---------------------------------
# Highest / lowest generation days
# ---------------------------------

print("\n===================================")
print("EXTREME GENERATION DAYS")
print("===================================")

print("\nHighest generation days:")
print(
    daily.nlargest(5, "total_ac_power")[
        ["DATE", "total_ac_power", "max_ac_power"]
    ]
)

print("\nLowest generation days:")
print(
    daily.nsmallest(5, "total_ac_power")[
        ["DATE", "total_ac_power", "max_ac_power"]
    ]
)