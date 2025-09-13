FROM python:3.11-slim

WORKDIR /app

# Копируем backend код
COPY backend/ .

# Устанавливаем зависимости
RUN pip install --no-cache-dir fastapi motor uvicorn pydantic

# Сначала заполняем БД начальными автомобилями, затем запускаем API
CMD ["sh", "-c", "python seed.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
