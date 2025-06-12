import os
from django.contrib.auth import get_user_model
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlinejudge.settings")
django.setup()

def run():
    User = get_user_model()
    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superuser created")
    else:
        print("ℹ️ Superuser already exists")

if __name__ == "__main__":
    run()
