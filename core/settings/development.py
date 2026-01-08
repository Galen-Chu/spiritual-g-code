"""
Development settings for Spiritual G-Code.
"""

from .base import *

# Debug Mode
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database - Use SQLite for development/testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL configuration (commented out for local testing)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'spiritual_gcode_dev'),
#         'USER': os.getenv('DB_USER', 'gcode_user'),
#         'PASSWORD': os.getenv('DB_PASSWORD', 'dev_password'),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }

# Email Backend (Console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache - Use local memory cache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Static Files
STATICFILES_DIRS = [BASE_DIR / 'static']

# Logging - More verbose for development
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['api']['level'] = 'DEBUG'
LOGGING['loggers']['ai_engine']['level'] = 'DEBUG'

# Debug Toolbar
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1', 'localhost']
    except ImportError:
        pass
