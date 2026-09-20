import pandas as pd


def simulate_energy(
    solar_generation,
    household_demand,
    battery_capacity_kwh=10.0,
    initial_battery_soc=70.0,
    minimum_reserve_kwh=2.0,
    grid_available=True
):
    """
    Simulate household energy availability.

    solar_generation:
        List of predicted solar generation in kWh per time interval.

    household_demand:
        List of household energy demand in kWh per time interval.

    battery_capacity_kwh:
        Total battery capacity.

    initial_battery_soc:
        Initial battery charge percentage.

    minimum_reserve_kwh:
        Energy reserve that should be protected.

    grid_available:
        Whether grid electricity is available.
    """

    battery_kwh = (
        battery_capacity_kwh
        * initial_battery_soc
        / 100
    )

    results = []

    total_solar = 0
    total_demand = 0
    grid_energy = 0
    battery_used = 0
    battery_charged = 0
    shortage_energy = 0

    for i in range(len(solar_generation)):

        solar = max(0, solar_generation[i])
        demand = max(0, household_demand[i])

        total_solar += solar
        total_demand += demand

        # --------------------------------
        # Solar supplies household first
        # --------------------------------

        solar_used = min(solar, demand)

        remaining_demand = demand - solar_used
        excess_solar = solar - solar_used

        # --------------------------------
        # Charge battery with excess solar
        # --------------------------------

        available_capacity = (
            battery_capacity_kwh - battery_kwh
        )

        battery_charge = min(
            excess_solar,
            available_capacity
        )

        battery_kwh += battery_charge
        battery_charged += battery_charge

        # --------------------------------
        # Battery supplies remaining demand
        # --------------------------------

        battery_available_for_use = max(
            0,
            battery_kwh - minimum_reserve_kwh
        )

        battery_discharge = min(
            remaining_demand,
            battery_available_for_use
        )

        battery_kwh -= battery_discharge
        remaining_demand -= battery_discharge

        battery_used += battery_discharge

        # --------------------------------
        # Grid supplies remaining demand
        # --------------------------------

        grid_supply = 0

        if remaining_demand > 0 and grid_available:
            grid_supply = remaining_demand
            grid_energy += grid_supply
            remaining_demand = 0

        # --------------------------------
        # Remaining demand = shortage
        # --------------------------------

        shortage = remaining_demand

        shortage_energy += shortage

        # --------------------------------
        # Save timestep
        # --------------------------------

        results.append({
            "interval": i,
            "solar_kwh": round(solar, 3),
            "demand_kwh": round(demand, 3),
            "battery_kwh": round(battery_kwh, 3),
            "grid_kwh": round(grid_supply, 3),
            "shortage_kwh": round(shortage, 3)
        })

    result_df = pd.DataFrame(results)

    # --------------------------------
    # Overall metrics
    # --------------------------------

    if total_demand > 0:
        energy_coverage = (
            (total_demand - shortage_energy)
            / total_demand
        ) * 100
    else:
        energy_coverage = 100

    if battery_capacity_kwh > 0:
        final_soc = (
            battery_kwh / battery_capacity_kwh
        ) * 100
    else:
        final_soc = 0

    return {
        "timeline": result_df,

        "total_solar_kwh": round(total_solar, 3),
        "total_demand_kwh": round(total_demand, 3),

        "grid_energy_kwh": round(grid_energy, 3),
        "battery_used_kwh": round(battery_used, 3),
        "battery_charged_kwh": round(battery_charged, 3),

        "shortage_kwh": round(shortage_energy, 3),
        "energy_coverage_percent": round(
            energy_coverage,
            2
        ),

        "final_battery_kwh": round(
            battery_kwh,
            3
        ),

        "final_battery_soc_percent": round(
            final_soc,
            2
        )
    }