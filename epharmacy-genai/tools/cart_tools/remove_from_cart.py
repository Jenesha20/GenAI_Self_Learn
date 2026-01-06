from .store import CART_DB

def remove_from_cart(user_id: str, product_id: str):
    user_cart = CART_DB.get(user_id, [])

    new_cart = [i for i in user_cart if i["product_id"] != product_id]
    CART_DB[user_id] = new_cart

    return {
        "status": "success",
        "data": {"cart_items": new_cart},
        "message": "Item removed"
    }
