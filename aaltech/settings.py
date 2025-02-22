"""
Django settings for aaltech project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import smtplib
from email.mime.text import MIMEText


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pad!t616fjfzfd36de9d&@!6=f16=e=ej(ij!rt1+(w_73%bmg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contact',
    'accounts',
    'faq',
    'checkout',
    'widget_tweaks',
    'payment',
    'admin_interface',
    'colorfield',
    'career',
    'oilgas',
    'news',
    'image_gallery',
    'transport',
    'product_special_offer',
    'recent_product',
    'help',
    'newsletter',
    'construction',
    'events',
    'product',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aaltech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'aaltech.wsgi.application'

AUTH_USER_MODEL = 'accounts.CustomUser'

SITE_ID = 2





# Admins Configuration
ADMINS = [('Admin', 'slygee46@gmail.com')]  # Admin email for notifications

# Mailtrap SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 2525  # Use port 2525 for Mailtrap
EMAIL_USE_TLS = True  # Use TLS encryption for Mailtrap
EMAIL_HOST_USER = '6a2b0e226b1a21'  # Replace with your Mailtrap username
EMAIL_HOST_PASSWORD = 'a47f1803341e2c'  # Replace with your Mailtrap password
DEFAULT_FROM_EMAIL = 'slygee46@gmail.com'  # Set this to your preferred from email address



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

STATIC_URL = 'static/'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Use a secure session cookie (only for HTTPS connections)
SESSION_COOKIE_SECURE = True

# Prevent JavaScript from accessing the session cookie
SESSION_COOKIE_HTTPONLY = True

# Use the 'Strict' policy for the session cookie, preventing sending it with cross-site requests
SESSION_COOKIE_SAMESITE = 'Strict'

# Use secure CSRF cookie
CSRF_COOKIE_SECURE = True

# Set the CSRF cookie to be HTTP-only
CSRF_COOKIE_HTTPONLY = False

# Set the CSRF cookie SameSite attribute
CSRF_COOKIE_SAMESITE = 'Strict'

SESSION_COOKIE_AGE = 1209600  # Two weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


CSRF_COOKIE_NAME = 'csrftoken'  # The name of the CSRF cookie


# settings.py

PAYSTACK_SECRET_KEY = 'pk_test_678dbd0531c9c40890a4ce0ba18ab41270132c02'


# settings.py

# settings.py
AUTHENTICATION_BACKENDS = [
    # 'staff.backends.StaffModelBackend',  # Add your custom backend here
    'django.contrib.auth.backends.ModelBackend',  # Keep the default backend as well
]
