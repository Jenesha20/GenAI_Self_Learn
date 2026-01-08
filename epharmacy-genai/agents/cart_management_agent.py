from graph.state import GraphState
from agents.cart_intent_parser import extract_cart_intent

def find_product_by_name(product_name: str, product_list):
    """Find product by name in product list"""
    if not product_name or not product_list:
        return None
    
    product_name_lower = product_name.lower()
    
    # If product_list is a dict (single product)
    if isinstance(product_list, dict):
        if product_name_lower in product_list.get("name", "").lower():
            return product_list
    
    # If product_list is a list
    elif isinstance(product_list, list):
        # Exact match
        for product in product_list:
            if product_name_lower == product.get("name", "").lower():
                return product
        
        # Partial match (product name contains search term)
        for product in product_list:
            if product_name_lower in product.get("name", "").lower():
                return product
        
        # Check if search term contains any word from product name
        name_words = product_name_lower.split()
        for product in product_list:
            product_name = product.get("name", "").lower()
            if any(word in product_name for word in name_words if len(word) > 2):
                return product
    
    return None

def cart_management_node(state: GraphState) -> dict:
    user_msg = state["messages"][-1]["content"]
    cart = state.get("cart_items", [])
    ctx = state.get("context", {}) or {}
    
    print(f"🛒 CART NODE: Processing message: '{user_msg}'")
    
    # 🔥 Check if this is a bot message (should be ignored)
    if user_msg.startswith("✅") or "verified successfully" in user_msg.lower():
        print(f"🛒 CART NODE: Ignoring bot message")
        return {
            "final_answer": "Please enter a quantity for the product.",
            "messages": [{"role": "assistant", "content": "Please enter a quantity for the product."}],
            "awaiting_quantity": True
        }
    
    # Get user intent
    intent = extract_cart_intent(user_msg)
    
    # If intent is "ignore", it's a bot message
    if intent["action"] == "ignore":
        print(f"🛒 CART NODE: Ignoring message (bot message)")
        return {
            "final_answer": "Please provide a quantity for the product.",
            "messages": [{"role": "assistant", "content": "Please provide a quantity for the product."}],
            "awaiting_quantity": True
        }
    
    # 🔥 Get available products from multiple sources
    available_products = None
    if state.get("product_data"):
        available_products = state["product_data"]
    elif ctx.get("last_products"):
        available_products = ctx.get("last_products")
    elif state.get("context", {}).get("last_products"):
        available_products = state["context"].get("last_products")
    
    print(f"🛒 CART NODE: Available products: {available_products}")
    
    # 🔥 Find the product user is referring to
    product = None
    
    # Priority 1: Current product in state (from prescription flow)
    if state.get("current_product"):
        product = state["current_product"]
        print(f"🛒 CART NODE: Using current_product from state: {product.get('name')}")
    
    # Priority 2: Product mentioned in intent
    if not product and intent.get("product_name") and available_products:
        product = find_product_by_name(intent["product_name"], available_products)
        print(f"🛒 CART NODE: Found product by name '{intent['product_name']}': {product.get('name') if product else 'None'}")
    
    # Priority 3: Single product from product_data
    if not product and isinstance(available_products, dict):
        product = available_products
    
    # Priority 4: First product from list
    if not product and isinstance(available_products, list) and len(available_products) > 0:
        product = available_products[0]
    
    print(f"🛒 CART NODE: Selected product: {product.get('name') if product else 'None'}")
    
    # 🔥 Handle quantity response (numeric input)
    if user_msg.strip().isdigit() and (state.get("awaiting_quantity") or ctx.get("awaiting_quantity")):
        qty = int(user_msg.strip())
        current_product = product or state.get("current_product")
        
        if current_product:
            # Add to cart
            cart_item = {
                "name": current_product.get("name", "Unknown Product"),
                "qty": qty,
                "price": current_product.get("price", 0),
                "requires_prescription": current_product.get("requires_prescription", False)
            }
            
            # Check if item already in cart
            existing_idx = -1
            for i, item in enumerate(cart):
                if item["name"].lower() == cart_item["name"].lower():
                    existing_idx = i
                    break
            
            if existing_idx >= 0:
                cart[existing_idx]["qty"] += qty
            else:
                cart.append(cart_item)
            
            final_answer = f"✅ Added {qty} units of {current_product['name']} to your cart."
            
            return {
                "cart_items": cart,
                "current_product": None,
                "awaiting_quantity": False,
                "requires_prescription": False,
                "final_answer": final_answer,
                "messages": [{"role": "assistant", "content": final_answer}],
                "context": {}
            }
        else:
            final_answer = "I'm not sure which product you're referring to. Please try again."
            return {
                "final_answer": final_answer,
                "messages": [{"role": "assistant", "content": final_answer}]
            }
    
    # Handle intents
    if intent["action"] == "view":
        if not cart:
            final_answer = "🛒 Your cart is empty."
        else:
            lines = []
            total = 0
            for item in cart:
                line = f"- {item['name']} × {item['qty']} = ₹{item.get('price', 0) * item['qty']}"
                if item.get("requires_prescription"):
                    line += " (Prescription required)"
                lines.append(line)
                total += item.get('price', 0) * item['qty']
            
            final_answer = "🛒 Your Cart:\n" + "\n".join(lines) + f"\n\n**Total: ₹{total}**"
        
        return {
            "final_answer": final_answer,
            "messages": [{"role": "assistant", "content": final_answer}]
        }
    
    elif intent["action"] == "clear":
        final_answer = "🗑️ Your cart has been cleared."
        return {
            "cart_items": [],
            "final_answer": final_answer,
            "messages": [{"role": "assistant", "content": final_answer}],
            "context": {}
        }
    
    elif intent["action"] == "remove":
        if not product:
            final_answer = "Which product do you want to remove from your cart?"
        else:
            new_cart = [item for item in cart 
                       if item["name"].lower() != product["name"].lower()]
            
            removed = len(cart) - len(new_cart)
            final_answer = f"Removed {product['name']} from your cart." if removed > 0 else "Item not found in cart."
            
            return {
                "cart_items": new_cart,
                "final_answer": final_answer,
                "messages": [{"role": "assistant", "content": final_answer}]
            }
    
    # 🔥 ADD ITEM
    elif intent["action"] == "add":
        if not product:
            if available_products:
                # List available products for user to choose
                if isinstance(available_products, list):
                    names = [p.get("name", "Unknown") for p in available_products[:3]]
                    final_answer = f"I found these products: {', '.join(names)}. Which one would you like to add to cart?"
                else:
                    final_answer = "Please specify which product you want to add to cart."
            else:
                final_answer = "Which product would you like to add to your cart?"
            
            return {
                "final_answer": final_answer,
                "messages": [{"role": "assistant", "content": final_answer}]
            }
        
        # Check if product requires prescription
        requires_rx = product.get("requires_prescription", False)
        
        if requires_rx:
            # Go to prescription flow
            return {
                "current_product": product,
                "requires_prescription": True,
                "prescription_status": "pending",
                "final_answer": f"⚠️ {product['name']} requires a prescription. Please upload your prescription to continue.",
                "messages": [{"role": "assistant", "content": f"⚠️ {product['name']} requires a prescription. Please upload your prescription to continue."}],
                "context": {**ctx, "last_product": product}
            }
        else:
            # Check if quantity was provided
            qty = intent.get("quantity")
            
            if qty:
                # Direct add with quantity
                cart_item = {
                    "name": product.get("name", "Unknown Product"),
                    "qty": qty,
                    "price": product.get("price", 0),
                    "requires_prescription": product.get("requires_prescription", False)
                }
                
                cart.append(cart_item)
                final_answer = f"✅ Added {qty} units of {product['name']} to your cart."
                
                return {
                    "cart_items": cart,
                    "current_product": None,
                    "requires_prescription": False,
                    "final_answer": final_answer,
                    "messages": [{"role": "assistant", "content": final_answer}],
                    "context": {}
                }
            else:
                # Ask for quantity
                final_answer = f"How many units of {product['name']} would you like to add?"
                
                return {
                    "current_product": product,
                    "awaiting_quantity": True,
                    "requires_prescription": False,
                    "final_answer": final_answer,
                    "messages": [{"role": "assistant", "content": final_answer}],
                    "context": {"awaiting_quantity": True, "last_product": product}
                }
    
    # Checkout
    elif intent["action"] == "checkout":
        if not cart:
            final_answer = "Your cart is empty. Add items before checkout."
        else:
            # Check if any items require prescription
            rx_items = [item for item in cart if item.get("requires_prescription")]
            if rx_items:
                final_answer = "Some items require prescription verification before checkout."
            else:
                total = sum(item.get('price', 0) * item['qty'] for item in cart)
                final_answer = f"Proceeding to checkout... Total: ₹{total}. (This would integrate with payment system)"
        
        return {
            "final_answer": final_answer,
            "messages": [{"role": "assistant", "content": final_answer}]
        }
    
    # Quantity input
    elif intent["action"] == "quantity":
        qty = intent.get("quantity")
        current_product = product or state.get("current_product")
        
        if current_product and qty:
            cart_item = {
                "name": current_product.get("name", "Unknown Product"),
                "qty": qty,
                "price": current_product.get("price", 0),
                "requires_prescription": current_product.get("requires_prescription", False)
            }
            
            cart.append(cart_item)
            final_answer = f"✅ Added {qty} units of {current_product['name']} to your cart."
            
            return {
                "cart_items": cart,
                "current_product": None,
                "awaiting_quantity": False,
                "final_answer": final_answer,
                "messages": [{"role": "assistant", "content": final_answer}],
                "context": {}
            }
    
    # Confirmations
    elif intent["action"] == "confirm":
        if intent.get("confirmation") == "yes":
            final_answer = "Great! What would you like to do next?"
        else:
            final_answer = "Alright. Let me know if you need anything else."
        
        return {
            "final_answer": final_answer,
            "messages": [{"role": "assistant", "content": final_answer}]
        }
    
    # FALLBACK
    final_answer = "What would you like to do with your cart? You can view, add, remove, or clear items."
    
    return {
        "final_answer": final_answer,
        "messages": [{"role": "assistant", "content": final_answer}]
    }