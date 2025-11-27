# Dockerfile

FROM python:3.13-slim

# Non-interactive mode
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies (asyncpg, psycopg, argon2, etc. are required)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establishing dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the code
COPY . .

# Render sets the PORT variable itself
ENV PORT=8000

# For production, we launch via gunicorn + uvicorn worker
CMD ["/bin/sh", "-c", "gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT} --workers 3"]