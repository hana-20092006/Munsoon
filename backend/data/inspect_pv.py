import pandas as pd

generation_path = "data/raw/Plant_1_Generation_Data.csv"
weather_path = "data/raw/Plant_1_Weather_Sensor_Data.csv"

generation = pd.read_csv(generation_path)
weather = pd.read_csv(weather_path)

print("\n========== GENERATION DATA ==========")

print("Shape:")
print(generation.shape)

print("\nColumns:")
print(generation.columns.tolist())

print("\nFirst 5 rows:")
print(generation.head())

print("\nMissing values:")
print(generation.isnull().sum())


print("\n========== WEATHER DATA ==========")

print("Shape:")
print(weather.shape)

print("\nColumns:")
print(weather.columns.tolist())

print("\nFirst 5 rows:")
print(weather.head())

print("\nMissing values:")
print(weather.isnull().sum())