import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hh*&v45txhnhu68@i$shi*qalo=l=)w4*b%8$1akw(e+!n#+ju'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Change to False when deploying to production

ALLOWED_HOSTS = ['novajudge.onrender.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://novajudge.onrender.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'accounts',
    'problems',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onlinejudge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'onlinejudge.wsgi.application'


# Database configuration
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For collectstatic

# Optional: if you have a 'static' folder in root
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Enable WhiteNoise static file handling
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Custom User model
AUTH_USER_MODEL = 'accounts.User'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# OpenAI API Key (optional use)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

from django.urls import reverse_lazy
LOGIN_REDIRECT_URL = 'problems:problem_list'  # After login, go to problem list
LOGOUT_REDIRECT_URL = 'home'  # After logout, go to main home (not problems:home)
