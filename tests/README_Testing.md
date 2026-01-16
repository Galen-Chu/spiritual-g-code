# Testing Documentation

## Overview

The `tests/` directory contains pytest-based test suites for the Spiritual G-Code platform. Tests cover API endpoints, calculator logic, and integration workflows.

**Technology:**
- pytest 7.4+
- pytest-django
- pytest-cov (coverage)
- pytest-mock (mocking)

---

## Directory Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_api.py              # API endpoint tests
└── test_calculator.py       # Calculator logic tests
```

---

## Pytest Configuration

### `pytest.ini`

```ini
[pytest]
DJANGO_SETTINGS_MODULE = core.settings.testing
python_files = test_*.py
testpaths = tests
addopts =
    -v
    --tb=short
    --cov=api
    --cov=ai_engine
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    django_db: Tests requiring database
```

---

## Fixtures (`conftest.py`)

### Available Fixtures

#### `db`
Setup test database.

**Usage:**
```python
@pytest.mark.django_db
def test_something(db):
    # Test with database
    pass
```

#### `user`
Create test user.

**Usage:**
```python
def test_with_user(user):
    # user is a GCodeUser instance
    assert user.username == 'testuser'
```

#### `natal_chart`
Create test natal chart.

**Usage:**
```python
def test_with_natal_chart(natal_chart):
    assert natal_chart.sun_sign == 'Leo'
```

#### `api_client`
API client for testing endpoints.

**Usage:**
```python
def test_api_endpoint(api_client):
    response = api_client.get('/api/gcode/')
    assert response.status_code == 200
```

---

## Test Files

### `test_api.py`

Tests for REST API endpoints.

**Test Categories:**

#### Authentication Tests
```python
def test_user_registration(api_client):
    response = api_client.post('/api/auth/register/', {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'birth_date': '2000-01-01',
        'birth_time': '12:00',
        'birth_location': 'New York, NY'
    })
    assert response.status_code == 201
```

#### Natal Chart Tests
```python
@pytest.mark.django_db
def test_create_natal_chart(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/natal/', {
        'birth_date': '2000-01-01',
        'birth_time': '12:00',
        'birth_location': 'New York, NY'
    })
    assert response.status_code == 201
    assert response.data['sun_sign'] is not None
```

#### Daily Transit Tests
```python
@pytest.mark.django_db
def test_calculate_daily_transit(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.post('/api/gcode/', {
        'date': '2026-01-15'
    })
    assert response.status_code == 201
    assert 'g_code_score' in response.data
```

#### Dashboard Tests
```python
@pytest.mark.django_db
def test_dashboard_overview(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/dashboard/overview/')
    assert response.status_code == 200
    assert 'latest_gcode' in response.data
```

---

### `test_calculator.py`

Tests for calculator logic.

**Test Categories:**

#### Natal Chart Calculation
```python
def test_calculate_natal_chart():
    calculator = MockGCodeCalculator()
    result = calculator.calculate_natal_chart({
        'date': '2000-01-01',
        'time': '12:00',
        'latitude': 40.7128,
        'longitude': -74.0060
    })
    assert 'planets' in result
    assert 'houses' in result
    assert result['sun_sign'] == 'Capricorn'
```

#### Transit Calculation
```python
def test_calculate_transits():
    calculator = MockGCodeCalculator()
    natal_chart = calculator.calculate_natal_chart({...})
    transits = calculator.calculate_transits(natal_chart, '2026-01-15')
    assert 'transits' in transits
    assert 'aspects_to_natal' in transits
```

#### Intensity Scoring
```python
def test_calculate_intensity():
    calculator = MockGCodeCalculator()
    result = calculator.calculate_g_code_intensity({
        'aspects': [...],
        'moon_phase': 'full'
    })
    assert 1 <= result['score'] <= 100
    assert result['intensity_level'] in ['low', 'medium', 'high', 'intense']
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_api.py
```

### Run Specific Test

```bash
pytest tests/test_api.py::test_user_registration
```

### Run with Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run tests requiring database
pytest -m django_db
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=api --cov=ai_engine --cov-report=html

# Open coverage report
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### Run in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest -n 4
```

---

## Test Organization

### Structure

```python
# tests/test_api.py

import pytest
from rest_framework.test import APIClient

class TestAuthentication:
    """Test authentication endpoints."""

    @pytest.mark.django_db
    def test_user_registration(self, api_client):
        pass

    @pytest.mark.django_db
    def test_user_login(self, api_client, user):
        pass

class TestNatalCharts:
    """Test natal chart endpoints."""

    @pytest.mark.django_db
    def test_create_natal_chart(self, api_client, user):
        pass
```

---

## Best Practices

### 1. Use Fixtures

```python
# Good
def test_with_fixture(user):
    assert user.is_active

# Bad
def test_without_fixture():
    user = GCodeUser.objects.create(username='test')
    assert user.is_active
```

### 2. Mark Tests

```python
@pytest.mark.django_db
def test_database_operation():
    pass

@pytest.mark.unit
def test_unit_test():
    pass

@pytest.mark.integration
def test_integration_test():
    pass
```

### 3. Use Descriptive Names

```python
# Good
def test_user_registration_with_valid_data_succeeds():
    pass

# Bad
def test_user():
    pass
```

### 4. Test One Thing

```python
# Good
def test_registration_returns_201():
    pass

def test_registration_creates_user_in_db():
    pass

# Bad
def test_registration():
    # Tests multiple things
    pass
```

---

## Mocking

### Mock External Services

```python
from unittest.mock import patch, Mock

@patch('ai_engine.gemini_client.GeminiGCodeClient')
def test_with_mocked_ai(mock_client_class):
    mock_client = Mock()
    mock_client.generate_daily_gcode.return_value = {
        'interpretation': 'Test interpretation',
        'themes': ['test']
    }
    mock_client_class.return_value = mock_client

    # Test with mocked client
    result = mock_client.generate_daily_gcode(...)
    assert result['interpretation'] == 'Test interpretation'
```

---

## Continuous Integration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements-test.txt
      - run: pytest --cov=api --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## Test Data Management

### Factory Boy (Optional)

Use Factory Boy for creating test data:

```python
import factory
from api.models import GCodeUser

class GCodeUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GCodeUser

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    birth_date = factory.Faker('date_of_birth')
```

---

## Related Documentation

- [API Application](../api/README_API_Application.md) - API endpoints
- [AI Engine](../ai_engine/README_AI_Engine.md) - Calculator logic
- [Django Core](../core/README_Django_Core.md) - Django settings

---

**Last Updated:** 2026-01-15
