"""
Django settings for miniprogram project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""


import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6l96=e*-y!^4w+3dg&*liclqe!2tc_c$w2f#x)*(&p_m7&aao9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

USE_MYSQL = False

# TODO: Add host name
ALLOWED_HOSTS = ['localhost', 'backend.sandbox.bbrecycle.cn']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'simple_history',

    'base',
    'usersys',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'miniprogram.urls'

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

WSGI_APPLICATION = 'miniprogram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Change database
if USE_MYSQL:
    SILENCED_SYSTEM_CHECKS = ['mysql.E001']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '/Users/hydra/Documents/coding/github/wali/backend/walibackend/client'
            },
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# User model

AUTH_USER_MODEL = 'usersys.UserBase'

# Add LOG
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'stream': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'debug_stream': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(pathname)s'
                      ' %(lineno)d %(message)s',
        },
        'request_stream': {
            '()': 'base.util.log.RequestDetailFormatter',
            'format':  '%(asctime)s %(name)-12s %(levelname)-8s'
                       ' %(request_method)s %(request_uri)s %(request_body)s'
                       ' %(message)s',
        },
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'stream',
        },
        'debug_stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'debug_stream',
            'filters': ['require_debug_true'],
        },
        'request_stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'request_stream',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['debug_stream'],
            'level': 'DEBUG',
        },
        '': {
            'level': 'WARNING',
            'handlers': ['stream', ],
        },
        'base': {
            'level': 'WARNING',
            'handlers': ['request_stream', ],
            'propagate': False,
        },
    },
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
        'KEY_PREFIX': 'DEFAULT'
    },
    'sessions': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
        'KEY_PREFIX': 'SESSION'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


# Upload location
# FIXME: this path shall be changed
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

UPLOAD_APPEARANCE_BANNER = 'upload/base/banner/%Y/%m/%d/'
UPLOAD_ORDER_PHOTO = 'upload/order/receipt/%Y/%m/%d/'
UPLOAD_VALIDATE_PHOTO = 'upload/user/validate/%Y/%m/%d/'
UPLOAD_DEMAND_PHOTO = 'upload/demand/origin/%Y/%m/%d/'
UPLOAD_INVITE_PHOTO = 'upload/invite/origin/%Y/%m/%d/'
UPLOAD_DEMAND_PHOTO_SNAPSHOT = 'upload/demand/snapshot/%Y/%m/%d/'
UPLOAD_CHECK_PHOTO = 'upload/appraisal/check_photos/%Y/%m/%d/'
CONTRACTS_GENERATE = 'contract/%Y/%m/%d/'
CONTRACTS_TEMPLATE = 'contract_template/'


# File Storage
DEFAULT_FILE_STORAGE = 'base.util.WLFileStorage.UUIDFileStorage'

# Phone Validator

PHONE_VALIDATOR = "base.util.phone_validator.validator.DummyPhoneValidator"

# String Validators

STRING_VALIDATORS = [
    {
        "NAME": "phone number",
        "CLASS": "base.util.misc_validators.PNValidator",
        "ARGS": {

        }
    },
    {
        "NAME": "user password",
        "CLASS": "base.util.misc_validators.DummyValidator",
    },
    {
        "NAME": "reason",
        "CLASS": "base.util.misc_validators.DummyValidator",
    }
]

# User_Sid duration
SID_DURATION = datetime.timedelta(days=10)

# Pusher
PUSHER = {
    "clz": "pushsys.funcs.pusher.jpusher.jpusher.JPusher",
    "kwargs": {}
}

# CORS Staffs

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# history
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True

# WCMiniProgram

MINIPROGRAM = {
    "AppID": 'wxfbbd60114365d79f',
    "AppSecret": '77dacbf01a0bedbf663a932a2e0de4a7',
}
