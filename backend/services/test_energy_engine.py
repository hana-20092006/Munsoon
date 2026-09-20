from energy_engine import simulate_energy


# --------------------------------
# Example 24-hour simulation
# --------------------------------

solar_generation = [
    0, 0, 0, 0,
    0, 0, 0.2, 0.5,
    0.8, 1.0, 1.2, 1.4,
    1.5, 1.4, 1.2, 1.0,
    0.7, 0.3, 0.1, 0,
    0, 0, 0, 0
]


household_demand = [
    0.3, 0.3, 0.3, 0.3,
    0.5, 0.7, 0.6, 0.5,
    0.3, 0.3, 0.3, 0.3,
    0.3, 0.3, 0.3, 0.4,
    0.6, 0.8, 1.0, 0.8,
    0.6, 0.5, 0.4, 0.3
]


# --------------------------------
# Scenario 1: Grid available
# --------------------------------

normal = simulate_energy(
    solar_generation,
    household_demand,
    battery_capacity_kwh=10,
    initial_battery_soc=70,
    minimum_reserve_kwh=2,
    grid_available=True
)

print("\n===================================")
print("NORMAL GRID SCENARIO")
print("===================================")

print("Solar:", normal["total_solar_kwh"], "kWh")
print("Demand:", normal["total_demand_kwh"], "kWh")
print("Grid:", normal["grid_energy_kwh"], "kWh")
print("Shortage:", normal["shortage_kwh"], "kWh")
print("Energy coverage:", normal["energy_coverage_percent"], "%")
print("Final battery:", normal["final_battery_soc_percent"], "%")


# --------------------------------
# Scenario 2: Grid outage
# --------------------------------

outage = simulate_energy(
    solar_generation,
    household_demand,
    battery_capacity_kwh=10,
    initial_battery_soc=70,
    minimum_reserve_kwh=2,
    grid_available=False
)

print("\n===================================")
print("GRID OUTAGE SCENARIO")
print("===================================")

print("Solar:", outage["total_solar_kwh"], "kWh")
print("Demand:", outage["total_demand_kwh"], "kWh")
print("Grid:", outage["grid_energy_kwh"], "kWh")
print("Shortage:", outage["shortage_kwh"], "kWh")
print("Energy coverage:", outage["energy_coverage_percent"], "%")
print("Final battery:", outage["final_battery_soc_percent"], "%")