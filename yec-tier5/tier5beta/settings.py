"""
Django settings for Tier5 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
SECRET_KEY = '5*3n0a!+aa4d8=0r!t(_rlgg6@23w3j(5t#+ik9j#-^d*bb#84'

CELERY_TASK_SERIALIZER='json'
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_RESULT_SERIALIZER='json'
CELERY_RESULT_BACKEND = 'amqp'
BROKER_CONNECTION_TIMEOUT = 30
BROKER_POOL_LIMIT = 1 # Will decrease connection usage
CELERY_TIMEZONE='US/Eastern'
CELERY_ENABLE_UTC=True
CELERY_IMPORTS=("legion.modules", "dashboard.modules", "dashboard.experiments")
CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'
CELERY_SEND_EVENTS = False
CELERY_EVENT_QUEUE_EXPIRE = 60
CELERY_EVENT_QUEUE_TTL = 10
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates/',
    BASE_DIR + 'dashboard/templates/'
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Sinan', 'sinan@tier5.co'))
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']


AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = 'AKIAIKM6CUVGB6BQ34CA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tier5'
MEDIA_URL = 'http://%s.s3.amazonaws.com/tier5beta/media/' % AWS_STORAGE_BUCKET_NAME


STATICFILES_DIRS = ( os.path.join(BASE_DIR,'static/'),)
#STATICFILES_DIRS = ( '/static/',)
MEDIA_ROOT = 'http://%s.s3.amazonaws.com/tier5beta/media/' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"

if False:  
    STATIC_URL = '/static/'
    STATIC_ROOT = '/static/'
    pass
else:
    STATIC_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
    STATIC_ROOT = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'legion',
    'south',
    'storages',
    'djcelery',
    'qsstats',
    'kombu.transport.django', 
    'corsheaders',
    'dashboard',
    'endless_pagination',
)

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'sinan.u.ozdemir'
EMAIL_HOST_PASSWORD = 'tier5beta'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
STRIPE_SECRET = "sk_live_Vl3d20R5NvvLUo3I7G55nDcg"
ENDLESS_PAGINATION_PER_PAGE = 9

AUTHENTICATION_BACKENDS = (
    'dashboard.backend.DashBoardBackend', 
    'legion.backend.MyCustomBackend', 
)
LOGIN_URL = '/legion/login/'
LOGIN_ERROR_URL = '/error/'
LOGIN_REDIRECT_URL = '/complete/'

TEMPLATE_CONTEXT_PROCESSORS = (
'django.core.context_processors.request',
'django.contrib.auth.context_processors.auth',
    )

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dashboard.middleware.ImpersonateMiddleware',
    'dashboard.middleware.SettingsMiddleWare',
)

ROOT_URLCONF = 'tier5beta.urls'
WSGI_APPLICATION = 'tier5beta.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'd3l8gvl393k4u7',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'u82shdigc2q2ci',
            'PASSWORD': 'p9061tvp0fc8fkantf0bic9846c',
            'HOST': 'ec2-54-83-207-160.compute-1.amazonaws.com',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '6442',                      # Set to empty string for default.
        }
}

CONN_MAX_AGE = 60
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ( 'GET', 'POST', 'PUT', 'PATCH', 'OPTIONS' )
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True





