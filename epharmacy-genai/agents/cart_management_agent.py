# from graph.state import GraphState
# from tools.cart_tools.add_to_cart import add_to_cart
# from tools.cart_tools.view_cart import view_cart

# def cart_management_node(state: GraphState) -> GraphState:
#     user_id = state["user_id"]
#     action = state.get("cart_action")
#     if not state.get("product_data"):
#         state["error_message"] = (
#             "Please select a product before adding it to your cart."
#         )
#         return state


#     if action == "view":
#         res = view_cart(user_id)
#         state["cart_items"] = res["data"]["cart_items"]

#     elif action == "add":
#         if not state.get("quantity_confirmed"):
#             # pause for human input
#             state["awaiting_quantity"] = True
#             return state

#         product = state["product_data"]
#         qty = state.get("quantity", 1)
#         res = add_to_cart(user_id, product, qty)

#         state["cart_items"] = res["data"]["cart_items"]
#         state["requires_prescription"] = res["data"]["requires_prescription"]

#     state["current_node"] = "cart_management"
#     return state


from graph.state import GraphState

def cart_management_node(state: GraphState) -> GraphState:
    product = state.get("product_data")

    if not product:
        return {"final_answer": "Select a product first."}

    # waiting for quantity
    if state.get("awaiting_quantity"):
        qty = int(state["messages"][-1]["content"])
        items = state.get("cart_items", [])
        product["qty"] = qty
        items.append(product)

        return {
            "cart_items": items,
            "awaiting_quantity": False,
            "final_answer": f"Added {qty} units of {product['name']} to cart."
        }

    # first time ask quantity
    return {
        "awaiting_quantity": True,
        "final_answer": "How many units do you want to add?"
    }

