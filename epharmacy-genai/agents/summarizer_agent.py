# from graph.state import GraphState

# def summarizer_node(state: GraphState) -> GraphState:

#     if state.get("is_safety_refusal"):
#         state["final_answer"] = (
#             "I can’t provide verified information on that. "
#             "Please consult a pharmacist or doctor."
#         )
#         return state

#     if state.get("drug_interaction_result"):
#         msg = state["drug_interaction_result"]
#         msg += "\n\nThis is for awareness only, not medical advice."
#         state["final_answer"] = msg

#     elif state.get("faq_result"):
#         state["final_answer"] = state["faq_result"]

#     elif "normal_chat" in state.get("tool_outputs", {}):
#         state["final_answer"] = state["tool_outputs"]["normal_chat"]

#     elif state.get("error_message"):
#         state["final_answer"] = state["error_message"]

#     elif state.get("product_data"):
#         p = state["product_data"]
#         state["final_answer"] = (
#             f"{p['name']} costs ₹{p['price']} and has {p['stock']} units available."
#         )

#     elif state.get("cart_items"):
#         state["final_answer"] = f"Your cart has {len(state['cart_items'])} items."

#     else:
#         state["final_answer"] = (
#         "I couldn’t find the information you requested. "
#         "Could you please rephrase?"
#     )

#     state["current_node"] = "summarizer"
#     return state



from graph.state import GraphState

def summarizer_node(state: GraphState) -> dict:

    answer = None   # 🔥 always initialize

    # -----------------------------
    # PRODUCT RESPONSE
    # -----------------------------
    if state.get("product_data"):
        p = state["product_data"]

        # Case 1: multiple products
        if isinstance(p, list):
            lines = []
            for item in p[:3]:
                stock = item.get("stock_qty", 0)
                stock_msg = "In stock" if stock > 0 else "Out of stock"
                rx = "Prescription required" if item.get("requires_prescription") else "OTC"

                lines.append(
                    f"- {item['name']} — ₹{item['price']} ({rx}, {stock_msg})"
                )

            answer = (
                "Here are some options:\n" + "\n".join(lines) +
                "\n\nWould you like details for any of these?"
            )

        # Case 2: single product
        else:
            answer = (
                f"{p['name']} costs ₹{p['price']}. "
                "Do you want to add it to your cart?"
            )

    # -----------------------------
    # FAQ RESPONSE
    # -----------------------------
    elif state.get("faq_result"):
        answer = state["faq_result"]

    # -----------------------------
    # DRUG INTERACTION RESPONSE
    # -----------------------------
    elif state.get("drug_interaction_result"):
        answer = state["drug_interaction_result"]

    # -----------------------------
    # FALLBACK / PRESET ANSWER
    # -----------------------------
    elif state.get("final_answer"):
        answer = state["final_answer"]

    # -----------------------------
    # DEFAULT
    # -----------------------------
    else:
        answer = "How can I help you today?"

    # -----------------------------
    # UPDATE STATE
    # -----------------------------
    return {
        "final_answer": answer,
        "messages": [{"role": "assistant", "content": answer}]
    }
