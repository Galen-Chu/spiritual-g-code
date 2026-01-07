"""
Testing settings for Spiritual G-Code.
"""

from .base import *

# Debug Mode
DEBUG = True

# Database - Use SQLite for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Password Validation - Disable for faster tests
AUTH_PASSWORD_VALIDATORS = []

# Email Backend - Use memory backend for tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Celery - Always eager for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable Logging for tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

# Disable CRSF for API testing
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
)

# Faster password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Media files - Use temp directory
MEDIA_ROOT = '/tmp/spiritual_gcode_media/'
