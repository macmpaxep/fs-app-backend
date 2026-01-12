from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import products, cart

app = FastAPI(title="FS Catalog API")

origins = [
    "http://localhost:3000",       # фронтенд на локальном хосте
    "https://your-frontend-domain.com"  # или фронтенд на Render/Netlify/Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # кто может делать запросы
    allow_credentials=True,
    allow_methods=["*"],         # разрешаем GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# Подключаем роутеры с префиксом /api
app.include_router(products.router, prefix="/api")
app.include_router(cart.router, prefix="/api")

