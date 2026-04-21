FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY gateway/ ./gateway/
COPY stubs/ ./gateway/stubs/
COPY shared/src/shared/ ./gateway/shared/
COPY proto-build/src/proto_build/ ./gateway/

# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# Запуск приложения
WORKDIR /app/gateway
CMD ["python", "main.py"]
