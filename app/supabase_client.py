import requests
import os

# -----------------------------
# Настройки Supabase
# -----------------------------
SUPABASE_URL = "https://maodicpwdcgrmvcfuzdz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hb2RpY3B3ZGNncm12Y2Z1emR6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODA2MjgzNCwiZXhwIjoyMDgzNjM4ODM0fQ.oO5uLO4va2bGW1VLAt6s0JjA86tKt4dkTwILAtCfgDA"  # ⚠️ Service Role Key из Settings → API → Service key
TABLE_PRODUCTS = "products"
TABLE_CARTS = "carts"
TABLE_CART_ITEMS = "cart_items"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ---------------- PRODUCTS ----------------

def get_products(category=None, min_price=None, max_price=None, search=None,
                 limit=10, offset=0, sort_by="name", order="asc"):

    url = f"{SUPABASE_URL}/rest/v1/{TABLE_PRODUCTS}"

    params = {
        "select": "*",
        "limit": limit,
        "offset": offset,
        "order": f"{sort_by}.{order}"
    }

    if category:
        params["category"] = f"eq.{category}"
    if min_price is not None:
        params["price"] = f"gte.{min_price}"
    if max_price is not None:
        params["price"] = f"lte.{max_price}"
    if search:
        params["or"] = f"(name.ilike.*{search}*,description.ilike.*{search}*)"

    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


def get_product_by_id(product_id: int):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_PRODUCTS}?id=eq.{product_id}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


# ---------------- CART ----------------

def get_or_create_cart(session_id: str):
    # проверить есть ли корзина
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_CARTS}?session_id=eq.{session_id}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()

    if data:
        return data[0]

    # создать
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/{TABLE_CARTS}",
        headers=HEADERS,
        json={"session_id": session_id}
    )
    r.raise_for_status()
    return r.json()[0]


def add_to_cart(session_id: str, product_id: int, quantity: int):
    cart = get_or_create_cart(session_id)

    # проверить есть ли уже товар
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_CART_ITEMS}"
    params = {
        "select": "*",
        "cart_id": f"eq.{cart['id']}",
        "product_id": f"eq.{product_id}"
    }

    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    data = r.json()

    if data:
        item = data[0]
        return update_cart_item(item["id"], item["quantity"] + quantity)

    # иначе вставляем новый
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/{TABLE_CART_ITEMS}",
        headers=HEADERS,
        json={
            "cart_id": cart["id"],
            "product_id": product_id,
            "quantity": quantity
        }
    )
    r.raise_for_status()
    return r.json()[0]


def get_cart(session_id: str):
    cart = get_or_create_cart(session_id)

    url = f"{SUPABASE_URL}/rest/v1/{TABLE_CART_ITEMS}"
    params = {
        "select": "id,quantity,products(id,name,price)",
        "cart_id": f"eq.{cart['id']}"
    }

    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


def update_cart_item(item_id: int, quantity: int):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_CART_ITEMS}?id=eq.{item_id}"
    r = requests.patch(url, headers=HEADERS, json={"quantity": quantity})
    r.raise_for_status()
    return r.json()[0]


def delete_cart_item(item_id: int):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_CART_ITEMS}?id=eq.{item_id}"
    r = requests.delete(url, headers=HEADERS)
    r.raise_for_status()
    return {"status": "deleted"}