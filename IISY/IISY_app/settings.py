"""
Django settings for IISY_app project.
Generated by 'django-admin startproject' using Django 2.2.6.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import django_heroku
import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+m-kqg!bx%wq(t9lq2co5uc9(eo%c-28)ifc%94hqw84ckfi--'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# '10.0.1.6', '127.0.0.1:8000'
ALLOWED_HOSTS = ['iisy.herokuapp.com', 'newdomain.live']


# Application definition
# Shared apps are apps that all tenants can interact with and if they modify it gets modified for everyone
SHARED_APPS = [
    'django_tenants',
    'Customer',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # allows setting cors headers for requests to API
    'rest_framework',  # enable rest framework
]
# Tenant apps are the ones where each tenant get their own instance of an app
TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'iisy_landing',

]

INSTALLED_APPS = list(set(SHARED_APPS + TENANT_APPS))


MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

# Need to study this further
PUBLIC_SCHEMA_URLCONF = 'IISY_app.public_urls'
ROOT_URLCONF = 'IISY_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), '..',
                         'templates').replace('\\', '/'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # ~ 'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # List of callables that know how to import templates from various sources.
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                # insert your TEMPLATE_LOADERS here
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    # ...
)

WSGI_APPLICATION = 'IISY_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# Install postgresql and then enter your servers name, username and password to test

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT'],
        # ..
    }
}
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

# Need to study this further
TENANT_MODEL = "Customer.Client"
TENANT_DOMAIN_MODEL = "Customer.Domain"

STATICFILES_DIRS = (os.path.join('static'), )

# TODO: figure out how to allow certain domains to request API with CORS
# For now allow requests from all domains
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1',
#     'localhost'
# )
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
config = locals()
django_heroku.settings(config, databases=False)
# Manual configuration of database
conn_max_age = config.get('CONN_MAX_AGE', 600)  # Used in django-heroku
config['DATABASES'] = {
    'default': dj_database_url.parse(
        os.environ['DATABASE_URL'],
        engine='django_tenants.postgresql_backend',
        conn_max_age=conn_max_age,
        ssl_require=True
    )
}
# for sending emails
#SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Override production variables if DJANGO_DEVELOPMENT env variable is set
if os.environ.get('DJANGO_DEVELOPMENT') is not None:
    from settings_dev import *