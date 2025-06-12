# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Render will use
EXPOSE 8000

# Default command: run migrations, create superuser, start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python create_superuser.py && gunicorn onlinejudge.wsgi:application --bind 0.0.0.0:$PORT"]
