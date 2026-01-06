from typing import Dict
from .store import CART_DB

def add_to_cart(user_id: str, product: Dict, quantity: int) -> Dict:
    if quantity <= 0:
        return {
            "status": "invalid",
            "data": None,
            "message": "Quantity must be greater than zero"
        }

    user_cart = CART_DB.setdefault(user_id, [])

    # check if exists
    for item in user_cart:
        if item["product_id"] == product["product_id"]:
            item["quantity"] += quantity
            break
    else:
        user_cart.append({
            "product_id": product["product_id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity,
            "requires_prescription": product["requires_prescription"]
        })

    return {
        "status": "success",
        "data": {
            "cart_items": user_cart,
            "requires_prescription": product["requires_prescription"]
        },
        "message": "Item added to cart"
    }
