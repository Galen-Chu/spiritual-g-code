# 🔧 Spiritual G-Code - Troubleshooting Guide

This guide covers common issues and solutions when setting up and developing the Spiritual G-Code project, especially on Windows.

---

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Database Migration Issues](#database-migration-issues)
3. [Missing Dependencies](#missing-dependencies)
4. [Windows-Specific Issues](#windows-specific-issues)
5. [Configuration Problems](#configuration-problems)
6. [Code Import Errors](#code-import-errors)
7. [Quick Fix Commands](#quick-fix-commands)

---

## Development Environment Setup

### Issue: PostgreSQL Installation Fails on Windows

**Error:**
```
Error: pg_config executable not found.
pg_config is required to build psycopg2 from source.
```

**Solution:** Use SQLite for local development instead of PostgreSQL.

**Steps:**
1. Edit `core/settings/development.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

2. Comment out PostgreSQL configuration in `core/settings/base.py`

3. Use `requirements-test.txt` which excludes PostgreSQL dependencies:

```txt
# Core Django
Django==5.0.1
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-filter==24.3

# Authentication
djangorestframework-simplejwt==5.5.1
PyJWT==2.8.0

# API Documentation
drf-spectacular==0.29.0

# Testing
pytest==7.4.4
pytest-django==4.7.0

# AI/Utilities
google-generativeai==0.3.2
python-dotenv==1.0.0
Pillow==12.1.0
whitenoise==6.11.0
django-crontab==0.7.1
```

---

## Database Migration Issues

### Issue: Inconsistent Migration History

**Error:**
```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency api.0001_initial
```

**Solution:** Reset the database and migration history.

**Steps:**

**Windows (PowerShell):**
```powershell
# Delete database
Remove-Item -Path ".\db.sqlite3" -Force -ErrorAction SilentlyContinue

# Delete migration files
Remove-Item -Path ".\api\migrations\*.py" -Exclude "__init__.py" -Force -ErrorAction SilentlyContinue

# Recreate migrations
python manage.py makemigrations api

# Run all migrations
python manage.py migrate
```

**Windows (CMD):**
```cmd
del db.sqlite3
del api\migrations\0*.py
python manage.py makemigrations api
python manage.py migrate
```

**Linux/macOS:**
```bash
rm db.sqlite3
rm api/migrations/0*.py
python manage.py makemigrations api
python manage.py migrate
```

---

### Issue: Migration Creates Incorrect Dependencies

**Symptom:** Built-in Django migrations (admin, auth) run before custom app migrations.

**Solution:** Always create migrations for all apps before running migrate:

```bash
# Create migrations for all apps first
python manage.py makemigrations

# Then apply them
python manage.py migrate
```

---

## Missing Dependencies

### Issue: ModuleNotFoundError for Various Packages

**Common missing packages:**
```
ModuleNotFoundError: No module named 'rest_framework_simplejwt'
ModuleNotFoundError: No module named 'drf_spectacular'
ModuleNotFoundError: No module named 'whitenoise'
ModuleNotFoundError: No module named 'django_filters'
ModuleNotFoundError: No module named 'Pillow'
```

**Solution:** Install missing packages:

```bash
# Install all missing packages at once
pip install djangorestframework-simplejwt drf-spectacular whitenoise django-filter Pillow django-crontab
```

### Issue: PyEphem Installation Fails on Windows

**Error:**
```
Building wheel for ephem did not run successfully.
Microsoft Visual C++ 14.0 or greater is required.
```

**Solution:** Temporarily disable `ai_engine` app for testing.

**Steps:**
1. Edit `core/settings/base.py`:
   ```python
   LOCAL_APPS = [
       'api.apps.ApiConfig',
       # 'ai_engine.apps.AiEngineConfig',  # Temporarily disabled - requires PyEphem
   ]
   ```

2. For production, either:
   - Install Visual Studio Build Tools
   - Use Docker/Linux environment for ai_engine features

---

## Windows-Specific Issues

### Issue: Logging Path Does Not Exist

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\var\\log\\gcode\\django.log'
```

**Solution:** Use project-relative paths with automatic directory creation.

**Edit `core/settings/base.py`:**
```python
# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Use logs directory in project root for cross-platform compatibility
LOG_DIR = os.path.join(BASE_DIR.parent, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'django.log')

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
            'filename': LOG_FILE,  # Use the cross-platform path
            'formatter': 'verbose',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    # ... rest of logging config
}
```

### Issue: Redis Cache Backend Not Available

**Error:**
```
django.core.cache.backends.base.InvalidCacheBackendError: Could not find backend 'django_redis.cache.RedisCache': No module named 'django_redis'
```

**Solution:** Use local memory cache for development.

**Edit `core/settings/development.py`:**
```python
# Cache - Use local memory cache for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

---

## Configuration Problems

### Issue: development.py Overrides Base Settings

**Symptom:** Changes in `base.py` don't take effect when using development settings.

**Cause:** `development.py` imports from `base.py` using `from .base import *`, then overrides specific settings.

**Solution:** Check both files when modifying settings:
- `core/settings/base.py` - Base settings for all environments
- `core/settings/development.py` - Development-specific overrides

**Common overrides in development.py:**
- DATABASES
- CACHES
- ALLOWED_HOSTS
- CORS settings
- DEBUG flag

---

## Code Import Errors

### Issue: JWT URL Import Path Incorrect

**Error:**
```
ModuleNotFoundError: No module named 'rest_framework_simplejwt.urls'
```

**Solution:** Import views directly instead of using include().

**Edit `core/urls.py`:**
```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # API - JWT Authentication
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # ... other patterns
]
```

### Issue: DjangoFilterBackend Import Error

**Error:**
```
AttributeError: module 'rest_framework.filters' has no attribute 'DjangoFilterBackend'
```

**Solution:** Import from `django_filters` instead of `rest_framework`.

**Edit `api/views.py`:**
```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters

class DailyTransitViewSet(viewsets.ModelViewSet):
    # ...
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # ...
```

### Issue: Filter Choices Not Defined

**Error:**
```
AttributeError: type object 'DailyTransit' has no attribute 'INTENSITY_LEVEL_CHOICES'
```

**Solution:** Define choice constants in `filters.py` instead of referencing model attributes.

**Edit `api/filters.py`:**
```python
# Choice constants (matching model field definitions)
INTENSITY_LEVEL_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('intense', 'Intense'),
]

class DailyTransitFilter(filters.FilterSet):
    intensity_level = filters.ChoiceFilter(choices=INTENSITY_LEVEL_CHOICES)
    # ...
```

---

## Quick Fix Commands

### Reset Everything (Nuclear Option)

**Windows:**
```cmd
# Delete database and migrations
del db.sqlite3
del api\migrations\0*.py

# Clear Python cache
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
del /s /q *.pyc

# Reinstall dependencies
venv\Scripts\pip install -r requirements-test.txt

# Recreate migrations and database
venv\Scripts\python manage.py makemigrations api
venv\Scripts\python manage.py migrate
```

**Linux/macOS:**
```bash
# Delete database and migrations
rm db.sqlite3
find . -path "*/api/migrations/0*.py" -not -name "__init__.py" -delete

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# Reinstall dependencies
pip install -r requirements-test.txt

# Recreate migrations and database
python manage.py makemigrations api
python manage.py migrate
```

### Check What's Installed

```bash
# List all installed packages
pip list

# Check for specific packages
pip show django djangorestframework django-filter drf-spectacular
```

### Verify Django Settings

```bash
# Check current settings
python manage.py diffsettings

# Check for issues
python manage.py check

# Show migration status
python manage.py showmigrations
```

---

## Pre-commit Checklist

Before committing or pushing code, verify:

1. **Environment is clean:**
   ```bash
   python manage.py check
   python manage.py makemigrations --check --dry-run
   ```

2. **Tests pass:**
   ```bash
   pytest
   ```

3. **No migration conflicts:**
   ```bash
   python manage.py migrate --plan
   ```

4. **Static files collected:**
   ```bash
   python manage.py collectstatic --noinput --dry-run
   ```

---

## Getting Help

If you encounter issues not covered here:

1. Check the main [README.md](../README.md) for setup instructions
2. Review [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) for system details
3. Search existing [GitHub Issues](https://github.com/Galen-Chu/spiritual-g-code/issues)
4. Create a new issue with:
   - Error message (full traceback)
   - Operating system and Python version
   - Steps to reproduce
   - What you've already tried

---

## Prevention Tips

1. **Use Virtual Environment:** Always use a venv to avoid dependency conflicts
2. **Pin Dependencies:** Use exact version numbers in requirements.txt
3. **Test on Clean Environment:** Test setup on a fresh machine/VM occasionally
4. **Document Changes:** Update this guide when you encounter new issues
5. **Use Docker:** For production or complex setups, use Docker to avoid environment issues

---

**Last Updated:** 2025-01-08
**Maintained By:** @Galen-Chu
