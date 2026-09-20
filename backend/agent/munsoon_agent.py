from rag.knowledge_base import retrieve_knowledge


def run_munsoon_agent(analysis):
    """
    MUNSOON agentic workflow.

    The agent:
    1. Reads the energy assessment.
    2. Determines the main energy risk.
    3. Retrieves relevant knowledge.
    4. Produces an explainable recommendation.
    """

    risk = analysis["risk"]
    shortage = analysis["shortage_kwh"]
    coverage = analysis["energy_coverage_percent"]
    battery_soc = analysis["final_battery_soc_percent"]

    # Build a query for the RAG system
    query = (
        f"energy risk {risk} "
        f"battery reserve "
        f"load shifting "
        f"shortage {shortage} "
        f"coverage {coverage}"
    )

    retrieved_knowledge = retrieve_knowledge(query, top_k=3)

    # Agent reasoning
    if risk == "HIGH":
        actions = [
            "Prioritize essential household loads.",
            "Preserve the remaining battery reserve.",
            "Shift flexible electricity usage toward periods of higher solar generation.",
            "Charge the battery before the expected low-generation period when possible."
        ]

    elif risk == "MEDIUM":
        actions = [
            "Preserve part of the battery for essential loads.",
            "Shift flexible electricity usage toward higher-solar periods.",
            "Monitor expected solar generation and household demand."
        ]

    else:
        actions = [
            "Energy availability is currently sufficient.",
            "Use available solar generation for flexible loads when practical.",
            "Maintain the configured battery reserve."
        ]

    return {
        "risk": risk,
        "reason": (
            f"Expected demand is {analysis['total_demand_kwh']} kWh "
            f"while predicted solar generation is "
            f"{analysis['total_solar_kwh']} kWh. "
            f"The estimated energy shortage is {shortage} kWh."
        ),
        "energy_coverage_percent": coverage,
        "remaining_battery_soc_percent": battery_soc,
        "recommended_actions": actions,
        "retrieved_knowledge": [
            {
                "topic": item["topic"],
                "content": item["content"]
            }
            for item in retrieved_knowledge
        ]
    }