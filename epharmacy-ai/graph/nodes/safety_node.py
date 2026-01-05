from graph.state import GraphState

def safety_agent(state: GraphState) -> GraphState:
    query = state["user_query"].lower()
    profile = state.get("user_profile", {})

    flags = []
    risk = "LOW"

    if "alcohol" in query:
        flags.append("Alcohol interaction")
        risk = "HIGH"

    if "overdose" in query or "too much" in query:
        flags.append("Overdose risk")
        risk = "HIGH"

    # 🔥 MUTATE EXISTING STATE
    state["risk_level"] = risk
    state["safety_flags"] = flags
    state["is_safety_refusal"] = (risk == "HIGH")

    print("✅ SAFETY AGENT SET:", state["risk_level"], state["safety_flags"])

    return state
