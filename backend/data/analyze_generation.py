import pandas as pd

generation_path = "data/raw/Plant_1_Generation_Data.csv"

df = pd.read_csv(generation_path)

print("Number of unique sources:")
print(df["SOURCE_KEY"].nunique())

print("\nSources:")
print(df["SOURCE_KEY"].unique())

print("\nNumber of unique timestamps:")
print(df["DATE_TIME"].nunique())

print("\nNumber of unique plant IDs:")
print(df["PLANT_ID"].nunique())

records_per_timestamp = df.groupby("DATE_TIME").size()

print("\nRecords per timestamp:")
print(records_per_timestamp.describe())

print("\nMost common record counts:")
print(records_per_timestamp.value_counts().head(10))