FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY search/ ./search/
COPY proto-build/src/proto_build/ ./search/
COPY shared/ ./shared/
# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# Запуск приложения
WORKDIR /app/search
CMD ["python", "main.py"]
