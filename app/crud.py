from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from . import models, schemas

def get_products(db: Session, skip: int = 0, limit: int = 10,
                 search: str = None, category: str = None,
                 sort_by: str = "name", order: str = "asc"):
    query = db.query(models.Product)

    if search:
        query = query.filter(models.Product.name.contains(search) |
                             models.Product.description.contains(search))
    if category:
        query = query.filter(models.Product.category == category)

    if sort_by == "price":
        query = query.order_by(asc(models.Product.price) if order=="asc" else desc(models.Product.price))
    else:
        query = query.order_by(asc(models.Product.name) if order=="asc" else desc(models.Product.name))

    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_cart_item(db: Session, cart_id: int, item: schemas.CartItemCreate):
    cart_item = models.CartItem(cart_id=cart_id, product_id=item.product_id, quantity=item.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

# -------- Корзина --------
def get_cart(db: Session, session_id: str):
    cart = db.query(models.Cart).filter(models.Cart.session_id==session_id).first()
    if not cart:
        cart = models.Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_to_cart(db: Session, session_id: str, product_id: int, quantity: int):
    cart = get_cart(db, session_id)
    item = db.query(models.CartItem).filter(models.CartItem.cart_id==cart.id,
                                            models.CartItem.product_id==product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = models.CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(item)
    db.commit()
    db.refresh(item)
    return item

def update_cart_item(db: Session, item_id: int, quantity: int):
    item = db.query(models.CartItem).filter(models.CartItem.id==item_id).first()
    if item:
        item.quantity = quantity
        db.commit()
        db.refresh(item)
    return item

def remove_cart_item(db: Session, item_id: int):
    item = db.query(models.CartItem).filter(models.CartItem.id==item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

def get_products(db: Session, skip: int = 0, limit: int = 10,
                 search: str = None, category: str = None,
                 min_price: float = None, max_price: float = None,
                 sort_by: str = "name", order: str = "asc"):
    query = db.query(models.Product)

    # Поиск по названию и описанию
    if search:
        query = query.filter(
            models.Product.name.contains(search) |
            models.Product.description.contains(search)
        )

    # Фильтрация по категории
    if category:
        query = query.filter(models.Product.category == category)

    # Фильтрация по цене
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    # Сортировка
    if sort_by == "price":
        query = query.order_by(asc(models.Product.price) if order=="asc" else desc(models.Product.price))
    else:
        query = query.order_by(asc(models.Product.name) if order=="asc" else desc(models.Product.name))

    # Пагинация
    return query.offset(skip).limit(limit).all()
