FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY community/ ./community/
COPY proto-build/src/proto_build/ ./community/
COPY shared/src/shared/ ./community/shared/
# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# Запуск приложения
WORKDIR /app/community
CMD ["python", "main.py"]
