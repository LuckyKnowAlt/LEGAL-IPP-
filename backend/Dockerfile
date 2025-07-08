# Dockerfile
FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y git libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry-like зависимостей
WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Копируем весь бэкенд
COPY backend /app

# Создание тома под модельные файлы
VOLUME ["/app/models"]

# Открываем порт
EXPOSE 8000

# Запускаем FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
