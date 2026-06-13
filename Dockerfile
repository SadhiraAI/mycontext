FROM python:3.12-slim

WORKDIR /app

# Install system deps for asyncpg (PostgreSQL C client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps first (cached layer if requirements don't change)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY pyproject.toml /app/
COPY README.md /app/
COPY src/ /app/src/
COPY app/ /app/app/
COPY alembic.ini /app/

# Install the mycontext SDK (all cognitive patterns are open source and ship by default)
RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
