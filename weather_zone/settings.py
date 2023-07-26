"""
Django settings for weather_zone project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import environ

from django.utils.translation import gettext_lazy as _

from .constants import (
    BASE_APP_NAME, FORECAST_APP_NAME, MET_EIREANN_APP_NAME
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# name of main app
MAIN_APP = Path(__file__).resolve().parent.name

# required environment variables are keys of 'scheme' plus REQUIRED_ENV_VARS
scheme = {
    # set casting, default value
    'DEBUG': (bool, False),
    'DEVELOPMENT': (bool, False),
    'TEST': (bool, False),
}

# Take environment variables from .env file
env = environ.Env(**scheme)
os.environ.setdefault('ENV_FILE', '.env')
environ.Env.read_env(
    os.path.join(BASE_DIR, env('ENV_FILE'))
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
DEVELOPMENT = env('DEVELOPMENT')
TEST = env('TEST')

ALLOWED_HOSTS = []


# Application definition
# Set to 'cloudinary' or 's3' for cloud storage
STORAGE_PROVIDER = 'default' if DEVELOPMENT else \
    env('STORAGE_PROVIDER', default='default').lower()
STATIC_PROVIDERS = {
    'default': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    'cloudinary': 'cloudinary_storage.storage.StaticHashedCloudinaryStorage',
    's3': f'{MAIN_APP}.s3_storage.StaticStorage'
}
DEFAULT_STORAGE = {
    'default': 'django.core.files.storage.FileSystemStorage',
    'cloudinary': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    's3': f'{MAIN_APP}.s3_storage.PublicMediaStorage'
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# forecast provider apps
FORECAST_APPS = [
    MET_EIREANN_APP_NAME,
]
# weather_zone apps
WZ_APPS = FORECAST_APPS.copy()
WZ_APPS.extend([
    # forecast app must be registered after provider apps
    FORECAST_APP_NAME,
    BASE_APP_NAME,
])
INSTALLED_APPS.extend(WZ_APPS)

INSTALLED_APPS.extend([
    'django_countries',
])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# https://docs.djangoproject.com/en/4.2/ref/settings/#root-urlconf
ROOT_URLCONF = f'{MAIN_APP}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # app-specific context processors
                f'{MAIN_APP}.context_processors.app_context',
                f'{BASE_APP_NAME}.context_processors.base_context',
                f'{FORECAST_APP_NAME}.context_processors.forecast_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'weather_zone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db(),
}
if not TEST:
    # only need default database in test mode
    DATABASES.update({
        # read os.environ['REMOTE_DATABASE_URL']
        'remote': env.db_url(
            'REMOTE_DATABASE_URL',
            default=f'sqlite:'
                    f'///{os.path.join(BASE_DIR, "temp-remote.sqlite3")}'
        ),
    })


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-IE'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ("en", _("English")),
    ("de", _("German")),
    ("fr", _("French")),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# !!
# https://github.com/klis87/django-cloudinary-storage
# Please note that you must set DEBUG to False to fetch static files from
# Cloudinary.
# With DEBUG equal to True, Django staticfiles app will use your local files
# for easier and faster development
# (unless you use cloudinary_static template tag).
# !!

if STORAGE_PROVIDER == 's3':
    # s3-related settings
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    # aws settings
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    # ACL default is None which means the file will be private per Amazon’s
    # default
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
else:
    # URL to use when referring to static files located in STATIC_ROOT
    STATIC_URL = 'static/'
    MEDIA_URL = 'media/'

# https://docs.djangoproject.com/en/4.2/ref/settings/#storages
STORAGES = {
    "default": {
        "BACKEND": DEFAULT_STORAGE[STORAGE_PROVIDER],
    },
    "staticfiles": {
        "BACKEND": STATIC_PROVIDERS[STORAGE_PROVIDER],
    },
}

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STATICFILES_DIRS
# Additional locations the staticfiles app will traverse for collectstatic
STATICFILES_DIRS = [
    # directories that will be found by staticfiles’s finders are by default,
    # are 'static/' app sub-directories and any directories included in
    # STATICFILES_DIRS
    os.path.join(BASE_DIR, 'static')
]
# absolute path to the directory where static files are collected for
# deployment
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STATIC_ROOT
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-MEDIA_ROOT
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# read in forecast provider settings
# providers should provide provider-specific settings via following variable:
# - <PROVIDER APP NAME>_SETTINGS : dict of settings
#   e.g. 'url=http://example.com;username=foo;password=bar'
FORECAST_APPS_SETTINGS = {}
for provider in FORECAST_APPS:
    # https://django-environ.readthedocs.io/en/latest/tips.html#complex-dict-format
    FORECAST_APPS_SETTINGS[provider] = env.dict(
        provider.upper() + '_SETTINGS',
        cast={'value': str},
        default={}
    )

# Google site verification
# https://support.google.com/webmasters/answer/9008080#meta_tag_verification&zippy=%2Chtml-tag
GOOGLE_SITE_VERIFICATION = env('GOOGLE_SITE_VERIFICATION', default='')

# Fontawesome kit url
# https://fontawesome.com/docs/web/setup/use-kit
FONTAWESOME_URL = env('FONTAWESOME_URL', default='')

# Google API key for geocoding
# https://developers.google.com/maps/documentation/geocoding/start
GOOGLE_API_KEY = env('GOOGLE_API_KEY', default='')

# Requests timeout
REQUEST_TIMEOUT = env('REQUEST_TIMEOUT', default=10)


# Development mode settings
CACHED_GEOCODE_RESULT = env('CACHED_GEOCODE_RESULT', default='') \
    if DEVELOPMENT else ''
