FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    httpx \
    asyncpg \
    psycopg2-binary \
    python-dotenv \
    alembic \
    requests

EXPOSE 8000 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
