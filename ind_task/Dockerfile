FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install fastapi motor uvicorn

# Запускаем seed.py перед запуском сервера
CMD ["sh", "-c", "python seed.py && uvicorn main:app --host 0.0.0.0 --port 8000"]