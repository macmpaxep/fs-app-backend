from app.database import SessionLocal
from app.models import Product

# --- Открываем сессию ---
db = SessionLocal()

# --- Тестовые товары ---
products = [
    {"name": "Товар 1", "description": "Описание 1", "price": 1000, "image": "http://example.com/1.png", "category": "Электроника"},
    {"name": "Товар 2", "description": "Описание 2", "price": 500, "image": "http://example.com/2.png", "category": "Книги"},
    {"name": "Товар 3", "description": "Описание 3", "price": 200, "image": "http://example.com/3.png", "category": "Игрушки"},
    {"name": "Товар 4", "description": "Описание 4", "price": 1500, "image": "http://example.com/4.png", "category": "Электроника"},
    {"name": "Товар 5", "description": "Описание 5", "price": 300, "image": "http://example.com/5.png", "category": "Книги"},
]

# --- Добавляем в базу ---
for p in products:
    product = Product(**p)
    db.add(product)

db.commit()
db.close()

print("Тестовые товары успешно добавлены!")
