from fastapi import FastAPI
from app.routers import products, cart

app = FastAPI(title="FS Catalog API")

# Подключаем роутеры с префиксом /api
app.include_router(products.router, prefix="/api")
app.include_router(cart.router, prefix="/api")

