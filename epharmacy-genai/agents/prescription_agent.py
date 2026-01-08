from graph.state import GraphState

def prescription_node(state: GraphState) -> dict:
    user_msg = state["messages"][-1]["content"].lower()
    product = state.get("current_product")
    
    print(f"📄 PRESCRIPTION NODE: Processing message: '{user_msg}'")
    print(f"📄 PRESCRIPTION NODE: Current product: {product}")
    
    if not product:
        # Try to get product from context
        ctx = state.get("context", {})
        product = ctx.get("last_product") or ctx.get("pending_product")
        
        if not product:
            return {
                "final_answer": "No product is currently awaiting prescription verification.",
                "prescription_status": None,
                "messages": [{"role": "assistant", "content": "No product is currently awaiting prescription verification."}]
            }
    
    # Handle prescription upload
    upload_keywords = ["upload", "here", "attached", "done", "sent", "submit", "prescription"]
    if any(keyword in user_msg for keyword in upload_keywords) and len(user_msg) < 50:
        # Simulate prescription processing
        return {
            "prescription_status": "verified",
            "requires_prescription": False,
            "current_product": product,  # Keep product for quantity question
            "awaiting_quantity": True,  # Set flag for quantity input
            "final_answer": f"✅ Prescription for {product['name']} verified successfully! How many units would you like to add?",
            "messages": [{"role": "assistant", "content": f"✅ Prescription for {product['name']} verified successfully! How many units would you like to add?"}],
            "context": {"prescription_verified": True, "awaiting_quantity": True}
        }
    
    elif "cancel" in user_msg or "skip" in user_msg or "no" in user_msg:
        return {
            "prescription_status": "rejected",
            "requires_prescription": False,
            "current_product": None,
            "final_answer": f"Prescription requirement for {product['name']} was not fulfilled. Item not added to cart.",
            "messages": [{"role": "assistant", "content": f"Prescription requirement for {product['name']} was not fulfilled. Item not added to cart."}],
            "context": {}
        }
    
    # Default message - ask for prescription
    default_msg = (
        f"**{product['name']}** requires a prescription.\n\n"
        "Please upload a clear image/PDF of your prescription.\n"
        "You can say 'I've uploaded it' or 'Here is my prescription' when done.\n"
        "Or say 'cancel' to skip this product."
    )
    
    return {
        "final_answer": default_msg,
        "prescription_status": "pending",
        "current_product": product,  # Keep product
        "messages": [{"role": "assistant", "content": default_msg}]
    }