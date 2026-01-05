def memory_agent(state):
    """
    Lightweight memory hook.
    Can later be backed by Redis / DB.
    """

    history = state.get("memory", [])
    history.append({
        "query": state["user_query"],
        "intent": state.get("intent"),
        "risk": state.get("risk_level")
    })

    state["memory"] = history[-10:]  # rolling memory
    return state
