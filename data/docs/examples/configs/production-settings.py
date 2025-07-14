"""
Context7 ERP - Production Settings Configuration
Version: v2.2.0-glassmorphism-enhanced
Source: Çeşitli deployment docs
Purpose: Production ayarları - configuration örnekleri
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================
# 1. SECURITY SETTINGS
# =============================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='your-production-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts for production
ALLOWED_HOSTS = [
    '31.97.44.248',  # VPS IP
    'context7.com',  # Domain
    'www.context7.com',
    'localhost',
    '127.0.0.1',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://context7.com",
    "https://www.context7.com",
    "http://31.97.44.248:8000",
]

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL/HTTPS settings (uncomment when SSL is ready)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# =============================
# 2. DATABASE CONFIGURATION
# =============================

# PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='context7_erp'),
        'USER': config('DB_USER', default='context7'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 60

# =============================
# 3. CACHE CONFIGURATION
# =============================

# Redis cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# =============================
# 4. EMAIL CONFIGURATION
# =============================

# SMTP configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@context7.com')

# =============================
# 5. STATIC & MEDIA FILES
# =============================

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================
# 6. LOGGING CONFIGURATION
# =============================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_error.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'erp': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# =============================
# 7. CELERY CONFIGURATION
# =============================

# Celery broker settings
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379/0')

# Celery task settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Istanbul'

# Celery beat schedule
CELERY_BEAT_SCHEDULE = {
    'send-low-stock-alerts': {
        'task': 'erp.tasks.send_low_stock_alert',
        'schedule': 3600.0,  # Her saat
    },
    'cleanup-old-logs': {
        'task': 'core.tasks.cleanup_old_logs',
        'schedule': 86400.0,  # Her gün
    },
}

# =============================
# 8. API CONFIGURATION
# =============================

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# JWT settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# =============================
# 9. MIDDLEWARE CONFIGURATION
# =============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.security_middleware.AdvancedRateLimitMiddleware',
    'core.middleware.security_middleware.SecurityHeadersMiddleware',
]

# =============================
# 10. APPLICATION SETTINGS
# =============================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_extensions',
    'debug_toolbar',  # Only for development
]

LOCAL_APPS = [
    'core',
    'dashboard',
    'erp',
    'users',
    'inventory',
    'production',
    'reports',
    'ai_forms',
    'labels',
    'work_orders',
    'settings_app',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# =============================
# 11. INTERNATIONALIZATION
# =============================

LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# =============================
# 12. FILE UPLOAD SETTINGS
# =============================

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Allowed file types
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']

# =============================
# 13. BACKUP CONFIGURATION
# =============================

# Backup settings
BACKUP_ROOT = os.path.join(BASE_DIR, 'backups')
BACKUP_RETENTION_DAYS = 30

# Database backup settings
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BACKUP_ROOT, 'database')}

# Media backup settings
MEDIABACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIABACKUP_STORAGE_OPTIONS = {'location': os.path.join(BACKUP_ROOT, 'media')}

# =============================
# 14. MONITORING SETTINGS
# =============================

# Application monitoring
MONITORING_ENABLED = True
MONITORING_ALERT_EMAIL = ['admin@context7.com']

# Performance monitoring
PERFORMANCE_MONITORING = {
    'SLOW_QUERY_THRESHOLD': 1.0,  # seconds
    'MEMORY_THRESHOLD': 80,  # percentage
    'CPU_THRESHOLD': 80,  # percentage
}

# Health check endpoints
HEALTH_CHECK_URLS = [
    '/health/',
    '/health/database/',
    '/health/cache/',
]

# =============================
# 15. DEFAULT PRIMARY KEY
# =============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================
# 16. CUSTOM SETTINGS
# =============================

# Context7 specific settings
CONTEXT7_VERSION = '2.2.0-glassmorphism-enhanced'
CONTEXT7_DEPLOYMENT_DATE = '2025-01-09'
CONTEXT7_ENVIRONMENT = 'production'

# ERP specific settings
ERP_COMPANY_NAME = 'Context7 ERP Sistemi'
ERP_COMPANY_CODE = 'C7'
ERP_CURRENCY = 'TRY'
ERP_DECIMAL_PLACES = 2

# Notification settings
NOTIFICATIONS_ENABLED = True
EMAIL_NOTIFICATIONS = True
SMS_NOTIFICATIONS = False

# Report settings
REPORT_CACHE_TIMEOUT = 3600  # 1 hour
EXPORT_FORMATS = ['pdf', 'excel', 'csv']

# Audit settings
AUDIT_ENABLED = True
AUDIT_RETENTION_DAYS = 365 