import pandas as pd

file_path = "data/raw/kochi_weather_2025.csv"

df = pd.read_csv(file_path)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset statistics:")
print(df.describe())

print("\nData types:")
print(df.dtypes)