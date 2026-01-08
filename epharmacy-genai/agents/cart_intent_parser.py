import re

def extract_cart_intent(user_msg: str) -> dict:
    """Parse cart-related intents from user message"""
    msg = user_msg.lower().strip()
    
    # Default intent
    result = {
        "action": "unknown",
        "quantity": None,
        "confirmation": None,
        "product_name": None
    }
    
    print(f"🛒 CART PARSER: Parsing message: '{msg}'")
    
    # 🔥 FIRST: Check if this is a bot message (starts with emoji or has verification)
    if msg.startswith("✅") or "verified successfully" in msg or "how many units" in msg:
        print(f"  → Action: ignore (bot message)")
        result["action"] = "ignore"
        return result
    
    # View cart
    view_patterns = ["view cart", "show cart", "what's in my cart", "cart items", "see cart", "my cart"]
    if any(pattern in msg for pattern in view_patterns):
        result["action"] = "view"
        print(f"  → Action: view")
        return result
    
    # Clear cart
    clear_patterns = ["clear cart", "empty cart", "remove all", "delete cart"]
    if any(pattern in msg for pattern in clear_patterns):
        result["action"] = "clear"
        print(f"  → Action: clear")
        return result
    
    # Remove item
    remove_pattern = r"remove\s+(.+?)\s+(?:from|in)\s+cart"
    if re.search(remove_pattern, msg):
        result["action"] = "remove"
        match = re.search(remove_pattern, msg)
        if match:
            result["product_name"] = match.group(1).strip()
        print(f"  → Action: remove, product: {result['product_name']}")
        return result
    
    # 🔥 FIXED: Add to cart with product name - avoid matching numbers in product names
    # Pattern 1: "add [product name] to cart"
    add_pattern1 = r"add\s+(.+?)\s+(?:to|in)\s+cart"
    # Pattern 2: "add [product name]" (end of message)
    add_pattern2 = r"add\s+(.+)$"
    # Pattern 3: "buy [product name]"
    buy_pattern = r"buy\s+(.+)$"
    # Pattern 4: "purchase [product name]"
    purchase_pattern = r"purchase\s+(.+)$"
    
    patterns = [
        (add_pattern1, "add"),
        (add_pattern2, "add"),
        (buy_pattern, "add"),
        (purchase_pattern, "add"),
    ]
    
    for pattern, action in patterns:
        match = re.search(pattern, msg)
        if match:
            result["action"] = action
            product_name = match.group(1).strip()
            
            # 🔥 FIX: Don't extract quantity from product name
            # Remove any quantity patterns that might be part of product name
            quantity_pattern = r'\b(\d+)\s*(?:units?|pieces?|tablets?|capsules?)\b'
            
            # Check if there's a quantity at the end of the message
            quantity_match = re.search(r'(\d+)$', msg)
            if quantity_match and quantity_match.group(1) in product_name:
                # This is likely part of the product name (e.g., "250mg")
                result["product_name"] = product_name
            else:
                # Check for separate quantity
                q_match = re.search(quantity_pattern, msg)
                if q_match:
                    result["quantity"] = int(q_match.group(1))
                    # Remove quantity from product name
                    result["product_name"] = re.sub(quantity_pattern, '', product_name).strip()
                else:
                    result["product_name"] = product_name
            
            print(f"  → Action: {action}, product: {result['product_name']}, quantity: {result['quantity']}")
            return result
    
    # Simple add patterns (without product name)
    simple_add_patterns = [
        r"^add(?: to)? cart$",
        r"^buy (?:this|it|that)$",
        r"^purchase (?:this|it|that)$",
        r"^add (?:to|in) cart$",
    ]
    
    for pattern in simple_add_patterns:
        if re.search(pattern, msg):
            result["action"] = "add"
            print(f"  → Action: add (simple)")
            
            # Extract quantity if mentioned
            quantity_match = re.search(r'(\d+)\s*(?:units?|pieces?|tablets?|capsules?)?', msg)
            if quantity_match:
                result["quantity"] = int(quantity_match.group(1))
            
            return result
    
    # Checkout
    checkout_patterns = ["checkout", "place order", "proceed to payment", "buy now", "order now"]
    if any(pattern in msg for pattern in checkout_patterns):
        result["action"] = "checkout"
        print(f"  → Action: checkout")
        return result
    
    # Yes/No confirmations
    yes_patterns = ["yes", "yeah", "yep", "sure", "okay", "ok", "alright", "correct"]
    no_patterns = ["no", "nope", "nah", "not now", "later", "cancel"]
    
    if any(pattern == msg for pattern in yes_patterns):
        result["action"] = "confirm"
        result["confirmation"] = "yes"
        print(f"  → Action: confirm (yes)")
        return result
    
    if any(pattern == msg for pattern in no_patterns):
        result["action"] = "confirm"
        result["confirmation"] = "no"
        print(f"  → Action: confirm (no)")
        return result
    
    # Numeric input
    if msg.isdigit():
        result["action"] = "quantity"
        result["quantity"] = int(msg)
        print(f"  → Action: quantity ({msg})")
        return result
    
    print(f"  → Action: unknown")
    return result