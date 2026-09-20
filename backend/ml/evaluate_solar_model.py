import pandas as pd
import joblib

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =================================
# Configuration
# =================================

DATA_PATH = "data/processed/ml_solar_dataset.csv"
MODEL_PATH = "ml/solar_generation_model.pkl"


# =================================
# Load data
# =================================

df = pd.read_csv(DATA_PATH)

df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

df = df.sort_values("DATE_TIME").reset_index(drop=True)


# =================================
# Features and target
# =================================

features = [
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION",
    "hour",
    "minute",
    "day_of_year"
]

target = "total_ac_power_kw"


# =================================
# Same chronological split
# =================================

split_index = int(len(df) * 0.80)

test_df = df.iloc[split_index:].copy()

X_test = test_df[features]
y_test = test_df[target]


# =================================
# Load model
# =================================

model = joblib.load(MODEL_PATH)

y_pred = model.predict(X_test)


# =================================
# Overall metrics
# =================================

overall_mae = mean_absolute_error(y_test, y_pred)

overall_rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

overall_r2 = r2_score(y_test, y_pred)


print("===================================")
print("OVERALL TEST PERFORMANCE")
print("===================================")

print(f"MAE  : {overall_mae:.2f} kW")
print(f"RMSE : {overall_rmse:.2f} kW")
print(f"R²   : {overall_r2:.4f}")


# =================================
# Daylight evaluation
# =================================

daylight_mask = test_df["IRRADIATION"] > 0

daylight_df = test_df[daylight_mask].copy()

y_day = daylight_df[target]

X_day = daylight_df[features]

y_day_pred = model.predict(X_day)


day_mae = mean_absolute_error(
    y_day,
    y_day_pred
)

day_rmse = mean_squared_error(
    y_day,
    y_day_pred
) ** 0.5

day_r2 = r2_score(
    y_day,
    y_day_pred
)


print("\n===================================")
print("DAYLIGHT TEST PERFORMANCE")
print("===================================")

print("Daylight samples:", len(daylight_df))

print(f"MAE  : {day_mae:.2f} kW")
print(f"RMSE : {day_rmse:.2f} kW")
print(f"R²   : {day_r2:.4f}")


# =================================
# Error relative to maximum power
# =================================

max_power = df[target].max()

mae_percentage = (day_mae / max_power) * 100

print("\nMAE as percentage of maximum power:")
print(f"{mae_percentage:.2f}%")


# =================================
# Actual vs predicted
# =================================

comparison = pd.DataFrame({
    "DATE_TIME": daylight_df["DATE_TIME"].values,
    "actual_kw": y_day.values,
    "predicted_kw": y_day_pred
})

comparison["absolute_error_kw"] = (
    comparison["actual_kw"]
    - comparison["predicted_kw"]
).abs()


print("\n===================================")
print("SAMPLE PREDICTIONS")
print("===================================")

print(comparison.head(15).to_string(index=False))


# =================================
# Worst predictions
# =================================

print("\n===================================")
print("LARGEST PREDICTION ERRORS")
print("===================================")

print(
    comparison
    .nlargest(10, "absolute_error_kw")
    .to_string(index=False)
)