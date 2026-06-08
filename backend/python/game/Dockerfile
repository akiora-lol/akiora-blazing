FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY game/ ./game/
COPY proto-build/src/proto_build/ ./game/
COPY stubs/ ./game/stubs/
COPY shared/src/shared/ ./game/shared/
# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# Запуск приложения
WORKDIR /app/game
CMD ["python", "main.py"]
