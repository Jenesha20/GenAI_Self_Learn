from graph.state import GraphState
def route_by_risk(state: GraphState):
    if state["risk_level"] == "HIGH":
        return "safety_agent"
    return "retrieval_agent"
