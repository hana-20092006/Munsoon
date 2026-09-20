from services.munsoon_engine import assess_energy_risk


solar_generation = [
    0, 0, 0, 0,
    0, 0.05, 0.10, 0.15,
    0.20, 0.25, 0.30, 0.35,
    0.40, 0.35, 0.30, 0.20,
    0.15, 0.08, 0.03, 0,
    0, 0, 0, 0
]


household_demand = [
    0.30, 0.30, 0.30, 0.30,
    0.50, 0.70, 0.60, 0.50,
    0.30, 0.30, 0.30, 0.30,
    0.30, 0.30, 0.30, 0.40,
    0.60, 0.80, 1.00, 0.80,
    0.60, 0.50, 0.40, 0.30
]


result = assess_energy_risk(
    solar_generation=solar_generation,
    household_demand=household_demand,
    battery_capacity_kwh=5,
    battery_soc=50,
    grid_available=False
)


print("\n===================================")
print("MUNSOON ENERGY ASSESSMENT")
print("===================================")

print("Risk:", result["risk"])

print(
    "Expected solar:",
    result["total_solar_kwh"],
    "kWh"
)

print(
    "Expected demand:",
    result["total_demand_kwh"],
    "kWh"
)

print(
    "Energy shortage:",
    result["shortage_kwh"],
    "kWh"
)

print(
    "Energy coverage:",
    result["energy_coverage_percent"],
    "%"
)

print(
    "Final battery:",
    result["final_battery_soc_percent"],
    "%"
)

print("\nRecommendation:")
print(result["recommendation"])