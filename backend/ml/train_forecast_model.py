import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


DATA_PATH = "data/processed/ml_solar_dataset.csv"
MODEL_PATH = "ml/forecast_solar_model.pkl"


# Load data
df = pd.read_csv(DATA_PATH)

df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

df = df.sort_values("DATE_TIME").reset_index(drop=True)


# Forecast-available features
features = [
    "AMBIENT_TEMPERATURE",
    "IRRADIATION",
    "hour",
    "minute",
    "day_of_year"
]

target = "total_ac_power_kw"


X = df[features]
y = df[target]


# Chronological split
split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("===================================")
print("FORECAST MODEL DATA SPLIT")
print("===================================")

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nTraining period:")
print(df["DATE_TIME"].iloc[0])
print("to")
print(df["DATE_TIME"].iloc[split_index - 1])

print("\nTesting period:")
print(df["DATE_TIME"].iloc[split_index])
print("to")
print(df["DATE_TIME"].iloc[-1])


# Train model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

print("\n===================================")
print("TRAINING FORECAST MODEL")
print("===================================")

model.fit(X_train, y_train)

print("Training completed!")


# Predictions
y_pred = model.predict(X_test)


# Overall metrics
mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(y_test, y_pred)


print("\n===================================")
print("OVERALL PERFORMANCE")
print("===================================")

print(f"MAE  : {mae:.2f} kW")
print(f"RMSE : {rmse:.2f} kW")
print(f"R²   : {r2:.4f}")


# Daylight performance
test_df = df.iloc[split_index:].copy()

daylight_mask = test_df["IRRADIATION"] > 0

daylight_y = y_test[daylight_mask]
daylight_pred = y_pred[daylight_mask]


day_mae = mean_absolute_error(
    daylight_y,
    daylight_pred
)

day_rmse = mean_squared_error(
    daylight_y,
    daylight_pred
) ** 0.5

day_r2 = r2_score(
    daylight_y,
    daylight_pred
)


print("\n===================================")
print("DAYLIGHT PERFORMANCE")
print("===================================")

print("Daylight samples:", len(daylight_y))

print(f"MAE  : {day_mae:.2f} kW")
print(f"RMSE : {day_rmse:.2f} kW")
print(f"R²   : {day_r2:.4f}")


# Feature importance
importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)


print("\n===================================")
print("FEATURE IMPORTANCE")
print("===================================")

print(importance)


# Save
joblib.dump(model, MODEL_PATH)

print("\n===================================")
print("MODEL SAVED")
print("===================================")

print(MODEL_PATH)