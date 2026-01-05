from graph.state import GraphState

def intent_classifier(state: GraphState) -> GraphState:
    query = state["user_query"].lower()

    if any(k in query for k in ["dose", "dosage", "how much"]):
        intent = "DOSAGE"
    elif any(k in query for k in ["side effect", "reaction"]):
        intent = "SIDE_EFFECTS"
    elif any(k in query for k in ["interaction", "mix", "together"]):
        intent = "INTERACTION"
    elif any(k in query for k in ["pregnant", "child", "baby"]):
        intent = "HIGH_RISK"
    else:
        intent = "GENERAL_INFO"

    state["intent"] = intent
    return state
