from graph.state import GraphState

def summarizer_node(state: GraphState) -> dict:
    answer = None
    updates = {}

    # 🔥 PRIORITY 1: If cart is awaiting quantity, show that message
    if state.get("awaiting_quantity") and state.get("current_product"):
        product = state.get("current_product")
        answer = f"How many units of {product.get('name', 'this product')} would you like to add?"
        return {
            "final_answer": answer,
            "messages": [{"role": "assistant", "content": answer}],
            "context": state.get("context", {})  # Preserve context
        }
    
    # 🔥 PRIORITY 2: If cart management already provided a final answer
    if state.get("final_answer"):
        answer = state["final_answer"]
        # Also store product data in context if available
        if state.get("product_data"):
            product_data = state["product_data"]
            if isinstance(product_data, list):
                updates["context"] = {
                    **state.get("context", {}),
                    "last_products": product_data,
                    "last_product_names": [p.get("name", "") for p in product_data]
                }
            elif isinstance(product_data, dict):
                updates["context"] = {
                    **state.get("context", {}),
                    "last_product": product_data,
                    "last_product_name": product_data.get("name", "")
                }
    else:
        # 🔥 Store product data in context for future reference
        if state.get("product_data"):
            product_data = state["product_data"]
            if isinstance(product_data, list):
                updates["context"] = {
                    **state.get("context", {}),
                    "last_products": product_data,
                    "last_product_names": [p.get("name", "") for p in product_data]
                }
            elif isinstance(product_data, dict):
                updates["context"] = {
                    **state.get("context", {}),
                    "last_product": product_data,
                    "last_product_name": product_data.get("name", "")
                }

        # -------------------------------
        # SINGLE PRODUCT DISPLAY
        # -------------------------------
        if isinstance(state.get("product_data"), dict):
            p = state["product_data"]
            answer = (
                f"**{p['name']}**\n"
                f"Price: ₹{p['price']}\n"
                f"Status: {'Prescription required' if p.get('requires_prescription') else 'OTC'}\n"
                f"Stock: {'Available' if p.get('stock_qty', 0) > 0 else 'Out of stock'}\n\n"
                "Would you like to add this to your cart?"
            )

        # -------------------------------
        # MULTIPLE PRODUCTS
        # -------------------------------
        elif isinstance(state.get("product_data"), list):
            lines = []
            for p in state["product_data"][:3]:
                rx = "Prescription required" if p.get("requires_prescription") else "OTC"
                stock = "Available" if p.get("stock_qty", 0) > 0 else "Out of stock"
                lines.append(f"- {p['name']} — ₹{p['price']} ({rx}, {stock})")

            answer = (
                "Here are some options:\n"
                + "\n".join(lines)
                + "\n\nTell me the name of the product you want details for, or say 'add [product] to cart'."
            )

        # -------------------------------
        # CART FLOW
        # -------------------------------
        elif state.get("cart_action") or state.get("cart_items"):
            cart = state.get("cart_items", [])
            if not cart:
                answer = "Your cart is empty."
            else:
                lines = [f"- {i['name']} x{i['qty']} = ₹{i.get('price', 0) * i['qty']}" for i in cart]
                total = sum(i.get('price', 0) * i['qty'] for i in cart)
                answer = "🛒 Your Cart:\n" + "\n".join(lines) + f"\n\n**Total: ₹{total}**"

        # -------------------------------
        # PRESCRIPTION FLOW
        # -------------------------------
        elif state.get("requires_prescription"):
            answer = "This medicine requires a prescription. Please upload it to continue."

        # -------------------------------
        # FAQ
        # -------------------------------
        elif state.get("faq_result"):
            answer = state["faq_result"]

        # -------------------------------
        # DRUG INTERACTION
        # -------------------------------
        elif state.get("drug_interaction_result"):
            answer = (
                state["drug_interaction_result"]
                + "\n\n⚠️ This is general information. Please consult a doctor or pharmacist."
            )

        # -------------------------------
        # FALLBACK
        # -------------------------------
        else:
            answer = "How can I help you today?"

    # Prepare return dict
    result = {
        "final_answer": answer,
        "messages": [{"role": "assistant", "content": answer}],
    }
    
    # Add any updates
    result.update(updates)
    
    return result