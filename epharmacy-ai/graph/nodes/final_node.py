def final_answer_node(state):
    if state.get("is_safety_refusal"):
        state["final_answer"] = (
            "This query involves high medical risk. "
            "Please consult a licensed physician."
        )
        state["confidence_score"] = 0.2
        return state

    state["final_answer"] = state["agent_outputs"].get("clinical", "")
    state["confidence_score"] = state.get("confidence_score", 0.8)
    return state
