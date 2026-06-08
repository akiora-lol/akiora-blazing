FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY messenger/ ./messenger/
COPY proto-build/src/proto_build/ ./messenger/
COPY shared/src/shared/ ./messenger/shared/
# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# Запуск приложения
WORKDIR /app/messenger
CMD ["python", "main.py"]
