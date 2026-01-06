CONTROL_FIELDS = [
    "intent",
    "sub_intent",
    "product_data",
    "cart_action",
    "awaiting_quantity",
    "needs_clarification",
]

def reset_control_state(state):
    for f in CONTROL_FIELDS:
        state.pop(f, None)
    return state
