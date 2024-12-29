import os
import environ
from pathlib import Path
from datetime import timedelta
from core.middlewares.request_id import RequestIDFilter

env = environ.Env(
    DEBUG=(bool, False),
    USE_SMTP=(int, 0),
    AXES_FAILURE_LIMIT=(int, 5),
    DB_POOL_MIN_SIZE=(int, 5),
    DB_POOL_MAX_SIZE=(int, 20),
    DB_POOL_TIMEOUT=(int, 30),
    LOG_MAX_BYTES=(int, 5242880),
    LOG_DISABLE_EXISTING=(bool, False),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True)
)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# App Settings - Add environment-specific defaults
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000'])
WEBSITE_NAME = env.str('WEBSITE_NAME', default='ABC Website')
WEBSITE_URL = env.str('WEBSITE_URL', default='www.abc.com')
ENVIRONMENT = env.str('ENVIRONMENT', default='PROD')  # Add environment setting (PROD / DEV)
USE_SMTP = env.int('USE_SMTP', default=0)  # Options: 0 - will use console, 1 - will use SMTP

# Application Config Settings
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# Core Settings
SECRET_KEY = env.str('SECRET_KEY', default='')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth Model
# AUTH_USER_MODEL = 'user.User'

# Locale Settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Installed Applications
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#3rd Party Applications
THIRD_PARTY_APPS = [
    'ninja',
    'ninja_extra',
    'ninja_jwt',
    'axes',
    'corsheaders'
]

#Local Applications
LOCAL_APPS = [

    'core',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Security Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'core.middlewares.request_id.RequestIDMiddleware'
]

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'max_similarity': 0.5,  # Reduced similarity threshold
            'user_attributes': ('username', 'first_name', 'last_name', 'email'),
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # NIST recommends at least 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'core.validators.password_validator.PasswordComplexityValidator',
    }
]

# Password Hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Template Settings
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
            ],
        },
    },
]

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME', default='postgres'),
        'USER': env.str('DB_USER', default='postgres'),
        'PASSWORD': env.str('DB_PASSWORD', default=''),
        'HOST': env.str('DB_HOST', default='localhost'),
        'PORT': env.str('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'pool': {  # Psycopg3's native pooling
                'min_size': env.int('DB_POOL_MIN_SIZE', default=5),  # Minimum connections in the pool
                'max_size': env.int('DB_POOL_MAX_SIZE', default=20),  # Maximum connections in the pool
                'timeout': env.int('DB_POOL_TIMEOUT', default=30),  # Time to wait for a connection
            },
            'application_name': WEBSITE_NAME,
            'options': '-c statement_timeout=5000',  # Set timeout for individual queries
        },
    }
}

# Redis Configuration
CACHE_LOCATION_URL = env.str('CACHE_LOCATION_URL', default='redis://127.0.0.1:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CACHE_LOCATION_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'RETRY_ON_TIMEOUT': True,
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,  # Define max connections here only
            },
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',  # Add compression
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',  # Use JSON serializer
        },
        'KEY_PREFIX': f"{WEBSITE_NAME}_{ENVIRONMENT}",  # Environment-specific prefix
    }
}


# RSA Key Handling
PRIVATE_KEY_PATH = env('PRIVATE_KEY_PATH', default='rsa_private.pem')
PUBLIC_KEY_PATH = env('PUBLIC_KEY_PATH', default='rsa_public.pem')
 
SIGNING_KEY = 'abcd'
VERIFYING_KEY = 'abcd'

if os.path.exists(PRIVATE_KEY_PATH):
    with open(PRIVATE_KEY_PATH, 'r') as private_key_file:
        SIGNING_KEY = private_key_file.read()

if os.path.exists(PUBLIC_KEY_PATH):
    with open(PUBLIC_KEY_PATH, 'r') as public_key_file:
        VERIFYING_KEY = public_key_file.read()

# JWT Settings
NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1440),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'RS256',
    'SIGNING_KEY': SIGNING_KEY,
    'VERIFYING_KEY': VERIFYING_KEY,
    'AUDIENCE': env('JWT_AUDIENCE', default='https://api.example.com'),
    'ISSUER': env('JWT_ISSUER', default='https://auth.example.com'),
    'AUTH_HEADER_TYPES': ('JWT',),
}

# Static and Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Session Configuration - Use Redis for sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Security Settings - Enhanced
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'

# Improved Axes Configuration
AXES_LOCK_OUT_AT_FAILURE = True
AXES_COOLOFF_TIME = timedelta(minutes=60)
# AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_LOCKOUT_CALLABLE = "core.services.lockout.lockout"
AXES_FAILURE_LIMIT = env.int('AXES_FAILURE_LIMIT', default=5)
AXES_IPWARE_META_PRECEDENCE_ORDER = [
    'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'
]
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend', 'django.contrib.auth.backends.ModelBackend'
]

# File Storage - Add S3 configuration
if not DEBUG:
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# Logging Configuration
LOG_LEVEL = env("LOG_LEVEL", default="DEBUG")
LOG_DIR_NAME = env("LOG_DIR_NAME", default="logs")
LOG_FILE_NAME = env("LOG_FILE_NAME", default="application.log")
LOG_MAX_BYTES = env.int("LOG_MAX_BYTES", default=5242880)  # Default to 5 MB
LOG_DISABLE_EXISTING = env.bool("LOG_DISABLE_EXISTING", default=False)  # Options: Bool

# Construct the full path for the log file
LOG_FILE_PATH = os.path.join(LOG_DIR_NAME, LOG_FILE_NAME)

# Check if the directory exists, if not, create it
if not os.path.exists(LOG_DIR_NAME):
    os.makedirs(LOG_DIR_NAME)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': LOG_DISABLE_EXISTING,
    'filters': {
        'request_id': {
            '()': RequestIDFilter,
        },
    },
    'handlers': {
        'handle_success_filelog': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'file_log_success',
            'maxBytes': LOG_MAX_BYTES,
            'backupCount': 5,
            'filters': ['request_id'],
        },
        'handle_error_filelog': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'file_log_error',
            'maxBytes': LOG_MAX_BYTES,
            'backupCount': 5,
            'filters': ['request_id'],
        },
    },
    'loggers': {
        'restapi.log.success.file': {
            'handlers': ['handle_success_filelog'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'restapi.log.error.file': {
            'handlers': ['handle_error_filelog'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
    'formatters': {
        'file_log_success': {
            'format': '[{levelname}] [{asctime}] [{process:d}] [{thread:d}] <{request_id}> {msg}',
            'style': '{',
        },
        'file_log_error': {
            'format': '[{levelname}] [{asctime}] [{process:d}] [{thread:d}] <{request_id}> {msg} {params}',
            'style': '{',
        }
    }
}

# Celery Configuration
CELERY_SETTINGS = {
    'broker_url': env.str("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/1"),
    'result_backend': env.str("CELERY_RESULT_BACKEND", default="redis://127.0.0.1:6379/1"),
    'task_track_started': True,
    'task_time_limit': 30 * 60,  # 30 minutes
    'worker_send_task_events': True,
    'worker_prefetch_multiplier': 1,
    'worker_max_tasks_per_child': 50,
    'worker_concurrency': os.cpu_count(),
    'beat_scheduler': 'django_celery_beat.schedulers:DatabaseScheduler',
    'task_compression': 'gzip',
    'task_protocol': 2,
    'worker_pool': 'solo',  # solo pool for Windows
    'task_acks_late': True,
    'task_reject_on_worker_lost': True,
    'task_retry_policy': {
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    },
    'broker_connection_retry_on_startup': True,
    'worker_hijack_root_logger': False,
    'worker_log_format': '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    'worker_task_log_format': '[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s',
    'task_default_queue': 'default',
    'task_queues': {
        'default': {
            'exchange': 'default',
            'routing_key': 'default',
        },
        'periodic': {
            'exchange': 'periodic',
            'routing_key': 'periodic',
        },
    },
    'result_expires': 60 * 60 * 24,  # 24 hours
    'result_extended': True,
    'result_compression': 'gzip',
}

# Email Configuration with environment-specific backends
if USE_SMTP:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.mailtrap.io')
    EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default=f'no-reply@{WEBSITE_NAME}.com')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
