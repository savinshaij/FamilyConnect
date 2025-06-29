"""
Django settings for familyconnect project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""
# admin username :admin
# admin email:admin@gmail.con
# admin password :Savin@2004


import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=g=x-!(gjsa8rry(kuk*g!2dj7hh0pkki7pc0n+73om@^r69a('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ["*"]  # Add your production host/domain here, e.g. ['yourdomain.com']

LOGIN_URL = '/auth/login/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'apps.core',
    'apps.users', 
    'apps.groups',
    'apps.posts',
    'apps.events',
    'apps.finance',
    'apps.memories',
    'apps.documents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Handles sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth sessions
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevent clickjacking
]

ROOT_URLCONF = 'familyconnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Use project-level 'templates' folder (optional)
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,  # Look inside app templates folders
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Needed for auth in templates
                'django.contrib.auth.context_processors.auth',  # Adds user, perms to templates
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'familyconnect.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Uncomment and set for production static collection
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_cdn')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Security and session settings for production ---

# Use HTTPS redirection (set True in production)
SECURE_SSL_REDIRECT = False  # Change to True on production with HTTPS setup

# Secure cookies - set True in production with HTTPS
SESSION_COOKIE_SECURE = False  # True in production
CSRF_COOKIE_SECURE = False     # True in production

# HTTPOnly flags for cookies to prevent JS access
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Session expiration settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600  # Two weeks, in seconds

# Prevent clickjacking via X-Frame-Options header
X_FRAME_OPTIONS = 'DENY'

# HTTP Strict Transport Security settings (only effective if SECURE_SSL_REDIRECT=True)
SECURE_HSTS_SECONDS = 31536000  # One year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

AUTH_USER_MODEL = 'users.CustomUser'


# vxiv gpxp vxhs qsgz

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'               # Gmail SMTP server
EMAIL_PORT = 587                            # Port for TLS
EMAIL_USE_TLS = True                        # Use TLS (secure)
EMAIL_HOST_USER = 'dev.savinshaij@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'dpca yuiq oyvz umdd'     # App password, not your main Gmail password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
