from .store import CART_DB

def view_cart(user_id: str):
    cart = CART_DB.get(user_id, [])
    total = sum(i["price"] * i["quantity"] for i in cart)

    return {
        "status": "success",
        "data": {
            "cart_items": cart,
            "total_price": total
        },
        "message": "Cart fetched"
    }
