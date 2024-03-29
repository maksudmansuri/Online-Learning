"""
Django settings for OC3 project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
import dj_database_url
# from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tchv)$j0)3m9_xcro$jr1kvqp5^^2rrd&r5d3s&9hsepz-8)^$'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

#only for training/testing 
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['aptechlearning.herokuapp.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'front.apps.FrontConfig',
    'student_lms.apps.StudentLmsConfig',
    'instructor_lms.apps.InstructorLmsConfig',
    'counsellor.apps.CounsellorConfig',
    'crispy_forms',
    'ckeditor',
    'ckeditor_uploader',
    'accounts',
    'simple_email_confirmation',
    'moviepy',
    'django.contrib.humanize',
    # 'channels',
    'chat',
    'rest_framework',
    'rest_framework.authtoken',
  

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.LoginCheckMiddleWare.LoginCheckMiddleWare',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'OC3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': ['templates'],
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                
            ],
        },
    },
]

SITE_ID = 1

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
 
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
 
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly'
        'rest_framework.permissions.IsAuthenticated'
        #  'rest_framework.permissions.IsAdminUser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'accounts.EmailBackEnd.EmailBackEnd',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10,
   
}
CORS_ORIGIN_WHITELIST = (
    'localhost:1234',
)



# AUTH_USER_MODEL='account.Account'
AUTH_USER_MODEL="accounts.CustomUser"

AUTHENTICATION_BACKENDS=(
    'accounts.EmailBackEnd.EmailBackEnd',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'OC3.wsgi.application'

ASGI_APPLICATION = 'OC3.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

LOGIN_URL="/accounts/student_singup"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE':'django.db.backends.mysql',
        'NAME':'octoecommrce',
        'USER':'root',
        'PASSWORD':'Aot567@lk',
        'HOST':'localhost',
        'PORT':'3306'
    }
}
db_frome_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_frome_env)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'

# Manualy Added
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_TEMPLATE_PACK="bootstrap4"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL =  '/media/'
TEMP = os.path.join(BASE_DIR, "temp")

from datetime import timedelta

EMAIL_CONFIRMATION_PERIOD_DAYS = 1
SIMPLE_EMAIL_CONFIRMATION_PERIOD = timedelta(days=EMAIL_CONFIRMATION_PERIOD_DAYS)

# SIMPLE_EMAIL_CONFIRMATION_EMAIL_ADDRESS_MODEL = 'accounts.EmailAddress'

#Email Sending
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'intellecttec@gmail.com'
EMAIL_HOST_PASSWORD = 'Aot567@lk'
EMAIL_PORT = 587

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())

#Payu Setup
PAYU_MERCHANT_KEY = "hACIXuc1",
PAYU_MERCHANT_SALT = "9yduiHrY25",
# Change the PAYU_MODE to 'LIVE' for production.
PAYU_MODE = "TEST"