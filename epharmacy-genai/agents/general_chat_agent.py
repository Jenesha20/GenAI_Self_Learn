# from graph.state import GraphState

# def general_chat_node(state: GraphState) -> GraphState:
#     query = state.get("user_query", "").lower()

#     if any(k in query for k in ["together", "interaction", "mix"]):
#         state["sub_intent"] = "drug_interaction"
#     elif any(k in query for k in ["how", "what", "when", "where"]):
#         state["sub_intent"] = "faq"
#     else:
#         state["sub_intent"] = "normal_chat"

#     state["current_node"] = "general_chat"
#     return state


from graph.state import GraphState

def general_chat_node(state: GraphState) -> GraphState:
    q = state["messages"][-1]["content"].lower()

    if any(k in q for k in ["together", "interaction"]):
        return {"sub_intent": "drug_interaction"}

    if any(k in q for k in ["how", "what", "when", "where"]):
        return {"sub_intent": "faq"}

    return {"sub_intent": "normal_chat"}
