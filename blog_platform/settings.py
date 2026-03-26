from pathlib import Path
from os import getenv
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------ SECURITY ------------------
SECRET_KEY = getenv('SECRET_KEY', 'unsafe-secret-key')

DEBUG = getenv('IS_DEVELOPMENT', 'False') == 'True'

ALLOWED_HOSTS = ['.onrender.com']


# ------------------ APPS ------------------
INSTALLED_APPS = [
    'blog',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # cloudinary
    'cloudinary',
    'cloudinary_storage',
]


# ------------------ MIDDLEWARE ------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'blog_platform.urls'


# ------------------ TEMPLATES ------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'blog_platform.wsgi.application'


# ------------------ DATABASE ------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ------------------ STATIC ------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ------------------ CLOUDINARY ------------------

# If you are using CLOUDINARY_URL, this config is optional
cloudinary.config(
    cloud_name=getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=getenv('CLOUDINARY_API_KEY'),
    api_secret=getenv('CLOUDINARY_API_SECRET'),
)


# ❌ REMOVE THESE (very important)
# MEDIA_ROOT = BASE_DIR/'uploads'
# MEDIA_URL = '/files/'


# ------------------ OTHER ------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
