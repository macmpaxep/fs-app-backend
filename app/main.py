from fastapi import FastAPI
from .database import Base, engine
from .models import Product, Cart, CartItem
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from . import crud, schemas, models
from typing import List, Optional

# Создаем таблицы в базе
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Product Catalog API")

@app.get("/")
def root():
    return {"status": "ok"}


# --- Products ---
@app.get("/api/products/", response_model=List[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 10,
                  search: Optional[str] = None,
                  category: Optional[str] = None,
                  sort_by: str = "name",
                  order: str = "asc",
                  db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit,
                             search=search, category=category,
                             sort_by=sort_by, order=order)

@app.get("/api/products/{product_id}/", response_model=schemas.ProductDetail)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# --- Cart ---
@app.get("/api/cart/", response_model=List[schemas.CartItemOut])
def view_cart(session_id: str, db: Session = Depends(get_db)):
    cart = crud.get_cart(db, session_id)
    return cart.items

@app.post("/api/cart/", response_model=schemas.CartItemOut)
def add_cart_item(item: schemas.CartItemCreate, session_id: str, db: Session = Depends(get_db)):
    return crud.add_to_cart(db, session_id, item.product_id, item.quantity)

@app.put("/api/cart/{item_id}/", response_model=schemas.CartItemOut)
def update_cart(item_id: int, quantity: int, db: Session = Depends(get_db)):
    updated_item = crud.update_cart_item(db, item_id, quantity)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/api/cart/{item_id}/")
def delete_cart(item_id: int, db: Session = Depends(get_db)):
    removed_item = crud.remove_cart_item(db, item_id)
    if not removed_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item removed"}