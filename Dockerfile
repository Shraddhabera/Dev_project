# # Use official Python image
# FROM python:3.10-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     g++ \
#     python3-dev \
#     libpq-dev \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Upgrade pip to latest version (good practice)
# RUN pip install --upgrade pip

# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project files
# COPY . .

# # Expose port (optional, but helps in some docker setups)
# EXPOSE 8000

# # Run migrations and start server (dev setup)
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Default command
CMD ["sh", "-c", "python manage.py migrate && gunicorn onlinejudge.wsgi:application --bind 0.0.0.0:$PORT"]
