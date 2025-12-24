def safety_condition(state):
    if "unsafe" in state["safety"].lower():
        return "escalate"
    return "end"
