KNOWLEDGE_BASE = [
    {
        "topic": "battery_reserve",
        "content": (
            "MUNSOON should preserve a configurable battery reserve "
            "during predicted periods of low solar generation. "
            "The reserve level is a user-configurable planning parameter "
            "and does not replace manufacturer battery safety limits."
        )
    },
    {
        "topic": "load_shifting",
        "content": (
            "Flexible household electricity usage can be shifted toward "
            "periods when solar generation is expected to be higher. "
            "Essential loads should receive priority during energy shortages."
        )
    },
    {
        "topic": "energy_risk",
        "content": (
            "MUNSOON classifies energy risk using predicted energy shortage "
            "and household energy coverage. A high-risk situation indicates "
            "that available solar and stored energy may not cover expected demand."
        )
    },
    {
        "topic": "responsible_ai",
        "content": (
            "MUNSOON predictions are estimates rather than guarantees. "
            "The system should explain the basis of recommendations, "
            "avoid unsupported claims, protect household privacy, "
            "and never provide unsafe electrical installation instructions."
        )
    }
]


def retrieve_knowledge(query: str, top_k: int = 2):
    """
    Lightweight retrieval for the MUNSOON prototype.
    Returns the most relevant knowledge entries based on keyword overlap.
    """

    query_words = set(query.lower().split())

    scored = []

    for item in KNOWLEDGE_BASE:
        text = item["content"].lower()
        score = sum(1 for word in query_words if word in text)

        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in scored[:top_k]]