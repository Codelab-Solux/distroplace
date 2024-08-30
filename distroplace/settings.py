# from decouple import config
import json
from dotenv import load_dotenv
from firebase_admin import credentials
import firebase_admin
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@u0f6%r&_-_#znj87l$xc3yl6bzuf%dfosqnctm9)vkrz0z&)j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False


ALLOWED_HOSTS = [
    'distroplace.com',
    'www.distroplace.com',
    'localhost',
    '127.0.0.1'
]

CORS_ALLOWED_ORIGINS = [
    "https://distroplace.com",
    "https://www.distroplace.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://distroplace.com",
    "https://www.distroplace.com",
]


# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

HASHIDS_SALT = 'VERITASCHRISTOETECCLESIAE'

SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # ---------third party apps-----------
    # 'decouple',
    'corsheaders',
    'django_ckeditor_5',
    # allauth stuff-------
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # firebase stuff-------
    # "django_firebase_auth",
    # ---------project apps-----------
    'base.apps.BaseConfig',
    'store.apps.StoreConfig',
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Place WhiteNoise here
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


ROOT_URLCONF = 'distroplace.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'distroplace.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'NAME': '/data/db/distroplace.sqlite3', #production db
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# if DEBUG:
#     # Local storage settings
#     MEDIA_URL = '/media/'
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# else:
#     # Google Cloud Storage settings
#     DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
#     GS_BUCKET_NAME = 'your-gcs-bucket-name'
#     GS_CREDENTIALS = 'path/to/your/credentials.json'
#     MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = (
    'distroplace.backends.FirebaseBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"}
    },
    "facebook": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"}
    }
}

# email config -----------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Replace with your email provider's SMTP server
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587  # Common port for TLS
# EMAIL_USE_TLS = True  # Use TLS
# EMAIL_HOST_USER = 'codelabsolux@gmail.com'  # Your email address
# EMAIL_HOST_PASSWORD = 'password'  # Your email password
# # DEFAULT_FROM_EMAIL = 'noreply@distroplace.com'

# django-allauth config -----------------------------------------------------
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False  # new
ACCOUNT_USERNAME_REQUIRED = False  # new
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # new
ACCOUNT_EMAIL_REQUIRED = True  # new
ACCOUNT_UNIQUE_EMAIL = True  # new

# app crash logs -----------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'app.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


# Firebase frontend settings -----------------------------------------------------
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
FIREBASE_AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN')
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')
FIREBASE_MESSAGING_SENDER_ID = os.getenv('FIREBASE_MESSAGING_SENDER_ID')
FIREBASE_APP_ID = os.getenv('FIREBASE_APP_ID')

# # Firebase backend settings
# FIREBASE_ADMIN_CREDENTIALS = os.path.join(
#     BASE_DIR, 'firebase_admin.json')
# cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIALS)
# firebase_admin.initialize_app(cred, name='distroplace')

# FIREBASE_CREDENTIALS_FILE = os.path.join(
#     BASE_DIR, 'firebase_admin.json')

# CKEditor config -----------------------------------------------------
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote',
            'imageUpload', 'insertTable', 'mediaEmbed', 'undo', 'redo'
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative', 'imageStyle:full', 'imageStyle:side'
            ]
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells']
        },
        'mediaEmbed': {
            'previewsInData': True
        },
    }
}


# login/logout redirects -----------------------------------------------------
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT = "/" #allauth redirect overrides the default redirect
# LOGOUT_REDIRECT_URL = "/"
# very important for overiding the default user model!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
AUTH_USER_MODEL = "accounts.CustomUser"
