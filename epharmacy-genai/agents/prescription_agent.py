from graph.state import GraphState

def prescription_node(state: GraphState) -> GraphState:

    # waiting for prescription
    if state.get("awaiting_prescription"):
        msg = state["messages"][-1]["content"]

        if "uploaded" in msg.lower():
            return {
                "prescription_verified": True,
                "awaiting_prescription": False,
                "final_answer": "Prescription verified. Order can proceed."
            }

        return {
            "final_answer": "Please upload your prescription to continue."
        }

    # start prescription flow
    return {
        "awaiting_prescription": True,
        "final_answer": "This medicine requires a prescription. Please upload it."
    }
