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

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations, create superuser, and start with gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py shell < create_superuser.py && gunicorn onlinejudge.wsgi"]
