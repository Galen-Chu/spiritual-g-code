# Django Core Configuration Documentation

## Overview

The `core/` directory contains the Django project configuration for the Spiritual G-Code platform. This includes settings, URL routing, WSGI/ASGI application entry points, Celery task queue configuration, and WebSocket routing.

**Technology Stack:**
- Django 5.0.1
- Django Channels 4.0.0 (WebSocket support)
- Celery 5.3.4 (Task queue)
- Redis (Cache & message broker)

---

## Directory Structure

```
core/
├── __init__.py
├── asgi.py                 # ASGI application entry point (WebSocket support)
├── wsgi.py                 # WSGI application entry point (HTTP)
├── urls.py                 # Root URL configuration
├── routing.py              # WebSocket URL routing
├── celery.py               # Celery task queue configuration
└── settings/               # Environment-specific settings
    ├── __init__.py
    ├── base.py             # Base settings (303 lines)
    ├── development.py      # Development environment overrides
    ├── testing.py          # Test environment overrides
    └── production.py       # Production environment overrides
```

---

## Settings Configuration

### Base Settings (`settings/base.py`)

The base settings file contains all common configuration shared across environments.

#### Application Structure

**Django Apps:**
```python
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

**Third-Party Apps:**
```python
THIRD_PARTY_APPS = [
    'rest_framework',                # Django REST Framework
    'rest_framework_simplejwt',      # JWT authentication
    'django_crontab',               # Scheduled tasks
    'corsheaders',                  # CORS support
    'drf_spectacular',              # OpenAPI schema
    'channels',                     # WebSocket support
]
```

**Local Apps:**
```python
LOCAL_APPS = [
    'api.apps.ApiConfig',           # API application
]
```

#### Database Configuration

**Development (SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'spiritual_gcode'),
        'USER': os.getenv('DB_USER', 'gcode_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

#### Custom User Model
```python
AUTH_USER_MODEL = 'api.GCodeUser'
```

#### REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}
```

#### JWT Configuration

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

**Token Lifetimes:**
- Access Token: 60 minutes
- Refresh Token: 7 days
- Auto-rotation enabled for security

#### CORS Configuration

```python
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
).split(',')
CORS_ALLOW_CREDENTIALS = True
```

#### Celery Configuration

```python
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
```

#### Cache Configuration (Redis)

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'gcode',
        'TIMEOUT': 300,
    }
}
```

#### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'api': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'ai_engine': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}
```

**Log File Location:** `logs/django.log`

#### Crontab Configuration

```python
CRONJOBS = [
    # Calculate Daily G-Code at 4:00 AM every day
    ('0 4 * * *', 'scripts.calculate_daily_gcode.calculate_all_daily_gcodes', '>> /tmp/gcode_calc.log'),

    # Generate Spiritual Patch Notes at 5:00 AM every day
    ('0 5 * * *', 'scripts.generate_patch_notes.generate_all_patch_notes', '>> /tmp/patch_notes.log'),

    # Clean up old data on Sundays at 3:00 AM
    ('0 3 * * 0', 'scripts.cleanup_old_data.run_all_cleanup', '>> /tmp/cleanup.log'),
]
```

**Scheduled Tasks:**
- Daily G-Code calculation: 4:00 AM daily
- Patch note generation: 5:00 AM daily
- Data cleanup: 3:00 AM on Sundays

#### Channels (WebSocket) Configuration

```python
CHANNEL_LAYERS = {
    'default': {
        # Use in-memory channel layer for development
        # For production, change to 'channels_redis.core.RedisChannelLayer'
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}
```

**Channel Layer Expiration:** 3600 seconds (1 hour)

#### API Documentation (Drf-Spectacular)

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Spiritual G-Code API',
    'DESCRIPTION': 'API for Spiritual G-Code - A personal operating system bridging software engineering, spiritual wisdom, and cosmic data.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api',
    'COMPONENT_SPLIT_REQUEST': True,
}
```

#### Session Configuration

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 604800  # 7 days in seconds
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

#### Security Settings

**Production (DEBUG=False):**
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

**Development (DEBUG=True):**
```python
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

---

### Environment-Specific Settings

#### Development (`settings/development.py`)

Overrides for local development environment:

```python
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Testing (`settings/testing.py`)

Overrides for test environment:

```python
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # In-memory database for fast tests
    }
}
CELERY_TASK_ALWAYS_EAGER = True  # Execute tasks synchronously
```

#### Production (`settings/production.py`)

Overrides for production environment:

```python
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Production database configuration
    }
}
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}
```

---

## URL Configuration

### Root URLs (`urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('djoser.urls.base')),
    path('', include('api.urls_html')),  # HTML views
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**URL Patterns:**
- `/admin/` - Django admin interface
- `/api/` - REST API endpoints
- `/auth/` - Authentication endpoints (login, logout, password reset)
- `/` - HTML views (dashboard, natal chart, etc.)

---

## WebSocket Routing

### WebSocket URLs (`routing.py`)

```python
from django.urls import re_path
from api.consumers import DashboardConsumer

websocket_urlpatterns = [
    re_path(r'^ws/dashboard/$', DashboardConsumer.as_asgi()),
]
```

**WebSocket Endpoints:**
- `ws/dashboard/` - Real-time dashboard updates

---

## Application Entry Points

### WSGI Application (`wsgi.py`)

Entry point for traditional HTTP requests:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

application = get_wsgi_application()
```

**Used by:**
- Gunicorn (production)
- Django development server (development)

### ASGI Application (`asgi.py`)

Entry point for WebSocket connections:

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

application = get_asgi_application()
```

**Used by:**
- Daphne (production ASGI server)
- Django development server (development)

---

## Celery Configuration

### Celery App (`celery.py`)

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

app = Celery('spiritual_gcode')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**Features:**
- Auto-discovers tasks from all installed apps
- Uses Redis as message broker
- Configured from Django settings

---

## Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=spiritual_gcode
DB_USER=gcode_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-pro

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Timezone
TIME_ZONE=UTC

# Logging
LOG_LEVEL=INFO
```

---

## Deployment Considerations

### Production Settings

**Required Changes:**
1. Set `DEBUG=False`
2. Set strong `SECRET_KEY`
3. Configure PostgreSQL database
4. Use Redis channel layer for WebSockets
5. Enable SSL/HTTPS
6. Set secure cookie flags
7. Configure ALLOWED_HOSTS properly
8. Use environment-specific settings module

### Static Files

**Development:** Served by Django
**Production:** Served by WhiteNoise or CDN

```bash
# Collect static files
python manage.py collectstatic
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Celery Worker

```bash
# Start Celery worker
celery -A core worker -l info

# Start Celery beat (scheduled tasks)
celery -A core beat -l info
```

### WebSocket Server

**Development:** Handled by Django dev server
**Production:** Use Daphne

```bash
daphne core.asgi:application -b 0.0.0.0 -p 8000
```

---

## Troubleshooting

### Common Issues

#### 1. WebSocket Connection Fails
- Check ASGI server is running
- Verify `CHANNEL_LAYERS` configuration
- Ensure Redis is running (for production)

#### 2. Celery Tasks Not Running
- Verify Redis is running
- Check Celery worker is started
- Review `CELERY_BROKER_URL` configuration

#### 3. Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` permissions
- Verify `STATIC_URL` configuration

#### 4. Database Connection Errors
- Verify database server is running
- Check database credentials in `.env`
- Ensure database exists and migrations are applied

---

## Related Documentation

- [API Application](../api/README_API_Application.md) - API backend implementation
- [AI Engine](../ai_engine/README_AI_Engine.md) - Calculation and AI services
- [Scripts](../scripts/README_Scripts.md) - Scheduled task scripts
- [Technical Architecture](../docs/TECHNICAL_ARCHITECTURE.md) - Complete system architecture

---

**Last Updated:** 2026-01-15
