from services.energy_engine import simulate_energy


def compare_strategies():

    # --------------------------------
    # MONSOON SCENARIO
    # --------------------------------

    solar_generation = [
        0,
        0,
        0,
        0,
        0,
        0.05,
        0.10,
        0.15,
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.35,
        0.30,
        0.20,
        0.15,
        0.08,
        0.03,
        0,
        0,
        0,
        0,
        0
    ]

    household_demand = [
        0.30,
        0.30,
        0.30,
        0.30,
        0.50,
        0.70,
        0.60,
        0.50,
        0.30,
        0.30,
        0.30,
        0.30,
        0.30,
        0.30,
        0.30,
        0.40,
        0.60,
        0.80,
        1.00,
        0.80,
        0.60,
        0.50,
        0.40,
        0.30
    ]

    # --------------------------------
    # REACTIVE STRATEGY
    # --------------------------------

    reactive = simulate_energy(
        solar_generation=solar_generation,
        household_demand=household_demand,
        battery_capacity_kwh=5,
        initial_battery_soc=50,
        minimum_reserve_kwh=1,
        grid_available=False
    )

    # --------------------------------
    # MUNSOON PROACTIVE STRATEGY
    # --------------------------------

    munsoon = simulate_energy(
        solar_generation=solar_generation,
        household_demand=household_demand,
        battery_capacity_kwh=5,
        initial_battery_soc=90,
        minimum_reserve_kwh=1,
        grid_available=False
    )

    # --------------------------------
    # COMPARISON
    # --------------------------------

    shortage_reduction = (
        reactive["shortage_kwh"]
        - munsoon["shortage_kwh"]
    )

    coverage_improvement = (
        munsoon["energy_coverage_percent"]
        - reactive["energy_coverage_percent"]
    )

    return {
        "reactive": reactive,
        "munsoon": munsoon,
        "shortage_reduction_kwh": round(
            shortage_reduction,
            2
        ),
        "coverage_improvement_percentage_points": round(
            coverage_improvement,
            2
        )
    }