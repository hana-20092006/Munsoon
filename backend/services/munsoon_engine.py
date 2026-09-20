from services.energy_engine import simulate_energy


def assess_energy_risk(
    solar_generation,
    household_demand,
    battery_capacity_kwh,
    battery_soc,
    grid_available=False
):
    result = simulate_energy(
        solar_generation=solar_generation,
        household_demand=household_demand,
        battery_capacity_kwh=battery_capacity_kwh,
        initial_battery_soc=battery_soc,
        minimum_reserve_kwh=1.0,
        grid_available=grid_available
    )

    shortage = result["shortage_kwh"]
    coverage = result["energy_coverage_percent"]

    # -----------------------------
    # Risk classification
    # -----------------------------

    if shortage == 0:
        risk = "LOW"
    elif coverage >= 70:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    # -----------------------------
    # Recommendation
    # -----------------------------

    if risk == "LOW":
        recommendation = (
            "Energy availability is sufficient. "
            "Use solar generation for flexible loads "
            "when available."
        )

    elif risk == "MEDIUM":
        recommendation = (
            "Energy availability may become constrained. "
            "Preserve battery reserve and shift flexible "
            "loads toward periods of higher solar generation."
        )

    else:
        recommendation = (
            "High energy-shortage risk detected. "
            "Prioritize essential loads, preserve battery "
            "reserve, and charge the battery before the "
            "expected low-generation period when possible."
        )

    return {
        "risk": risk,
        "recommendation": recommendation,
        "shortage_kwh": shortage,
        "energy_coverage_percent": coverage,
        "final_battery_soc_percent":
            result["final_battery_soc_percent"],
        "total_solar_kwh":
            result["total_solar_kwh"],
        "total_demand_kwh":
            result["total_demand_kwh"]
    }