CONTROL_FIELDS = [
    # routing / flow
    "intent",
    "sub_intent",
    "product_data",
    "cart_action",
    "awaiting_quantity",
    "needs_clarification",

    # 🔥 execution outputs (must NOT persist)
    "faq_result",
    "drug_interaction_result",
    "final_answer",
]

def reset_control_state(state):
    for f in CONTROL_FIELDS:
        state.pop(f, None)
    return state
