# Часть 1 ДЗ 10: одноэтапная сборка ML-сервиса (Credit Scoring API)
# Лучшие практики: порядок COPY (сначала зависимости), .dockerignore

FROM python:3.12-slim

WORKDIR /app

# Сначала копируем только зависимости — слой кэшируется при неизменном requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем код приложения
COPY app/ ./app/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
