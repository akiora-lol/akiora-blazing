FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY auth/ ./auth/
COPY proto-build/src/proto_build/ ./auth/

COPY shared/src/shared/ ./auth/shared/
COPY stubs/ ./auth/stubs/
# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# Запуск приложения
WORKDIR /app/auth
CMD ["python", "main.py"]
