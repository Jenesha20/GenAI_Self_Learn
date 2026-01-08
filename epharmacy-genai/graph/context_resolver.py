# graph/context_resolver.py
from graph.state import GraphState

def resolve_context(state: GraphState) -> GraphState:
    """
    Intercepts follow-up messages and forces correct intent
    based on conversation context.
    """

    

    msg = state["messages"][-1]["content"].lower()
    ctx = state.get("context", {})

    # -----------------------------
    # CART FLOW OVERRIDES
    # -----------------------------
    if any(k in msg for k in ["add", "remove", "cart"]):
        state["intent"] = "cart_action"
        return state

    # quantity reply
    if msg.isdigit() and ctx.get("pending_product"):
        state["intent"] = "cart_action"
        return state

    # prescription flow
    if ctx.get("pending_product") and "upload" in msg:
        state["intent"] = "cart_action"
        return state

    # yes / no confirmations
    if msg in ["yes", "no", "yep", "nope"]:
        if ctx.get("pending_product") or ctx.get("last_product"):
            state["intent"] = "cart_action"
            return state

    return state
