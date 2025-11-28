FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-docker.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements-docker.txt

# Copy project files
COPY . .

# Create static files directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8001

# Run makemigrations, migrate, and start server with gunicorn
CMD python manage.py makemigrations products && \
    python manage.py migrate && \
    gunicorn product_service.wsgi:application --bind 0.0.0.0:8001 --workers 2 --timeout 10
