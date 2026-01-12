from fastapi import APIRouter
from app.supabase_client import add_to_cart, get_cart, update_cart_item, delete_cart_item

router = APIRouter(tags=["Cart"])
SESSION_ID = "demo-session"

@router.post("/cart/")
def add_item(product_id: int, quantity: int):
    try:
        item = add_to_cart(SESSION_ID, product_id, quantity)
        return {"status": "success", "item": item}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/cart/")
def list_cart():
    items = get_cart(SESSION_ID)

    total = 0
    for i in items:
        total += i["quantity"] * i["products"]["price"]

    return {
        "items": items,
        "total_price": total
    }

@router.put("/cart/{item_id}/")
def update_item(item_id: int, quantity: int):
    return update_cart_item(item_id, quantity)

@router.delete("/cart/{item_id}/")
def delete_item(item_id: int):
    return delete_cart_item(item_id)