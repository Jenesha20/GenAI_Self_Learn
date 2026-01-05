from graph.state import GraphState

def safety_agent(state: GraphState) -> GraphState:
    query = state["user_query"].lower()
    profile = state.get("user_profile", {})

    flags = []
    risk = "LOW"

    # ---- query-based risk ----
    if any(k in query for k in ["overdose", "too much", "double dose"]):
        flags.append("Overdose risk")
        risk = "HIGH"

    if any(k in query for k in ["pregnant", "pregnancy"]):
        flags.append("Pregnancy risk")
        risk = "HIGH"

    if any(k in query for k in ["child", "baby", "infant"]):
        flags.append("Pediatric risk")
        risk = "HIGH"

    # ---- profile-based risk ----
    if profile.get("pregnant"):
        flags.append("Pregnancy risk")
        risk = "HIGH"

    if profile.get("age", 100) < 12:
        flags.append("Pediatric risk")
        risk = "HIGH"

    if profile.get("current_medications"):
        flags.append("Possible drug interaction")
        risk = "HIGH"

    # ---- persist (CRITICAL) ----
    state["risk_level"] = risk
    state["safety_flags"] = list(set(flags))
    state["is_safety_refusal"] = (risk == "HIGH")

    return state
