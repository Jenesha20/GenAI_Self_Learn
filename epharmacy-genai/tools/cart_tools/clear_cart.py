from .store import CART_DB

def clear_cart(user_id: str):
    CART_DB[user_id] = []
    return {
        "status": "success",
        "data": {"cart_items": []},
        "message": "Cart cleared"
    }
