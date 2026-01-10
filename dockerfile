# Берём готовый Python 3.14 образ
FROM python:3.14-slim

# Устанавливаем рабочую папку внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Команда запуска FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
