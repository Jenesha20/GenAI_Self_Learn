from .store import CART_DB

def update_cart(user_id: str, product_id: str, new_quantity: int):
    if new_quantity <= 0:
        return {
            "status": "invalid",
            "data": None,
            "message": "Quantity must be > 0"
        }

    user_cart = CART_DB.get(user_id, [])
    for item in user_cart:
        if item["product_id"] == product_id:
            item["quantity"] = new_quantity
            break

    return {
        "status": "success",
        "data": {"cart_items": user_cart},
        "message": "Cart updated"
    }
