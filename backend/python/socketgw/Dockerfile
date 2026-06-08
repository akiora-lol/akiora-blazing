FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY socketgw/ ./socketgw/
COPY shared/src/shared/ ./socketgw/shared/

ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV PYTHONPATH=/app

WORKDIR /app/socketgw
CMD ["python", "main.py"]
