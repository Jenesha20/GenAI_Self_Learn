# from graph.state import GraphState

# def supervisor_node(state: GraphState) -> GraphState:
#     query = state.get("user_query", "").lower()

#     # -----------------------------
#     # COMMERCE FLOW (highest priority)
#     # -----------------------------
#     if any(k in query for k in ["add", "cart", "buy", "purchase"]):
#         state["intent"] = "product_info"
#         return state

#     # -----------------------------
#     # PRODUCT INFO FLOW
#     # -----------------------------
#     if any(k in query for k in ["product", "price", "cost", "info", "details"]):
#         state["intent"] = "product_info"
#         return state

#     # -----------------------------
#     # GENERAL CHAT
#     # -----------------------------
#     state["intent"] = "general_chat"
#     return state


from graph.state import GraphState

def supervisor_node(state: GraphState) -> dict:
    q = state["messages"][-1]["content"].lower()

    commerce_words = ["buy", "add", "cart", "price", "tablet", "medicine", "paracetamol", "info"]

    if any(w in q for w in commerce_words):
        return {"intent": "product_info"}

    return {"intent": "general_chat"}
