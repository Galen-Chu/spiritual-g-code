# API Application Documentation

## Overview

The `api/` directory contains the Django REST Framework application that handles all backend business logic, data models, API endpoints, and real-time communication for the Spiritual G-Code platform.

**Technology Stack:**
- Django REST Framework 3.14.0
- Django Channels 4.0.0 (WebSocket support)
- PostgreSQL (production) / SQLite (development)

---

## Directory Structure

```
api/
├── __init__.py
├── admin.py              # Django admin configuration
├── apps.py               # API app configuration
├── annotation.py         # ChartAnnotation model definition
├── filters.py            # QuerySet filters for views
├── models.py             # Database models (8 models)
├── permissions.py        # Custom permission classes
├── serializers.py        # DRF serializers
├── signals.py            # Django signal handlers
├── urls.py               # API URL routing
├── views.py              # API viewsets and views
├── views_html.py         # HTML view controllers
├── consumers/            # WebSocket consumers
│   ├── __init__.py
│   └── dashboard_consumer.py
└── migrations/           # Database migrations
```

---

## Database Models

### Core Models (`models.py`)

#### 1. GCodeUser
Extends Django's AbstractUser with birth data and preferences.

**Key Fields:**
- `uuid` - UUID identifier
- `birth_date`, `birth_time` - Birth datetime
- `birth_location` - Birth place name
- `birth_latitude`, `birth_longitude` - Coordinates
- `birth_timezone` - Timezone string
- `bio` - User biography
- `avatar_url` - Profile picture URL
- `email_notifications` - Notification preference
- `daily_gcode_enabled` - Daily calculation opt-in
- `preferred_tone` - Content tone preference

**Relations:**
- One-to-one with `NatalChart`
- Many-to-many with `DailyTransit`
- Many-to-many with `GeneratedContent`

#### 2. NatalChart
Stores complete astrological birth chart data.

**Key Fields:**
- `user` - One-to-one relation to GCodeUser
- `chart_data` - JSONB with complete planetary positions
- `sun_sign`, `moon_sign`, `ascendant` - Key placements
- `dominant_elements` - JSONB element distribution
- `key_aspects` - JSONB major aspects
- `calculated_at` - Calculation timestamp

#### 3. DailyTransit
Daily transit calculations and interpretations.

**Key Fields:**
- `user` - ForeignKey to GCodeUser
- `transit_date` - Date of transit
- `transit_data` - JSONB transit positions
- `aspects_to_natal` - JSONB aspect calculations
- `g_code_score` - Integer (1-100)
- `themes` - JSONB array of themes
- `intensity_level` - Choice: low/medium/high/intense
- `ai_interpretation` - AI-generated text
- `updated_at` - Last update timestamp

#### 4. GeneratedContent
AI-generated content for social media.

**Key Fields:**
- `user` - ForeignKey to GCodeUser
- `content_type` - Choice: patch_note, insight, horoscope, etc.
- `platform` - Choice: twitter, instagram, linkedin, etc.
- `status` - Choice: draft, posted, scheduled, failed
- `title`, `body` - Content fields
- `hashtags` - JSONB array
- `scheduled_for` - Scheduled posting time
- `posted_at` - Actual posting time

#### 5. GCodeTemplate
AI prompt templates for content generation.

**Key Fields:**
- `name` - Template name
- `category` - Template category
- `prompt_template` - String with variable placeholders
- `variables` - JSONB array of variable names
- `is_active` - Boolean
- `created_by` - ForeignKey to GCodeUser

#### 6. UserActivity
Analytics and activity tracking.

**Key Fields:**
- `user` - ForeignKey to GCodeUser
- `action_type` - Choice: login, chart_calculated, content_generated, etc.
- `metadata` - JSONB additional data
- `timestamp` - Activity timestamp

#### 7. SystemLog
Application-level logging.

**Key Fields:**
- `level` - Choice: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `source` - Log source identifier
- `message` - Log message
- `metadata` - JSONB additional data
- `timestamp` - Log timestamp

#### 8. ChartAnnotation
User annotations on chart data points.

**Location:** `annotation.py`

**Key Fields:**
- `user` - ForeignKey to GCodeUser
- `chart_type` - Choice: daily, natal, transit
- `date` - Associated date
- `g_code_score` - Associated score
- `intensity` - Associated intensity
- `note` - User's note text
- `created_at`, `updated_at` - Timestamps

---

## API Views and ViewSets

### Authentication Views (`views.py`)

#### RegisterView
- **Endpoint:** `POST /api/auth/register/`
- **Purpose:** User registration with birth data
- **Serializer:** `UserRegistrationSerializer`
- **Response:** JWT tokens + user profile

#### UserProfileView
- **Endpoint:** `GET /api/auth/profile/`, `PUT /api/auth/profile/`
- **Purpose:** Retrieve/update current user profile
- **Permission:** IsAuthenticated
- **Serializer:** `UserSerializer`

### Data ViewSets

#### NatalChartViewSet
- **Endpoints:** Standard CRUD
- **Permission:** IsAuthenticated + IsOwner
- **Filters:** By user
- **Actions:**
  - `calculate` - POST to calculate natal chart
  - `retrieve` - GET single chart
  - `update` - PUT full update
  - `partial_update` - PATCH partial update

#### DailyTransitViewSet
- **Endpoints:** Standard CRUD
- **Permission:** IsAuthenticated + IsOwner
- **Filters:** By user, date range
- **Pagination:** PageNumberPagination (page_size=20)
- **Actions:**
  - `calculate` - POST to calculate transit
  - `latest` - GET latest transit for user
  - `range` - GET date range

#### GeneratedContentViewSet
- **Endpoints:** Standard CRUD
- **Permission:** IsAuthenticated + IsOwner
- **Filters:** By user, content_type, status, platform
- **Actions:**
  - `generate` - POST to generate content
  - `batch_generate` - POST for multiple pieces

#### GCodeTemplateViewSet
- **Endpoints:** Standard CRUD
- **Permission:** IsAuthenticated + IsOwnerOrReadOnly
- **Filters:** By category, is_active

#### ChartAnnotationViewSet
- **Endpoints:** Standard CRUD
- **Permission:** IsAuthenticated + IsOwner
- **Filters:** By user, chart_type, date range

### Special Views

#### DashboardOverviewView
- **Endpoint:** `GET /api/dashboard/overview/`
- **Purpose:** Aggregate dashboard data
- **Response:**
  - Latest G-Code score
  - Current intensity
  - Recent themes
  - Quick stats

#### DashboardChartsView
- **Endpoint:** `GET /api/dashboard/charts/`
- **Purpose:** Data for all dashboard charts
- **Response:** Chart-specific datasets

#### NatalWheelView
- **Endpoint:** `GET /api/natal/wheel/`
- **Purpose:** D3.js wheel rendering data
- **Response:** Complete wheel JSON structure

#### HealthCheckView
- **Endpoint:** `GET /api/health/`
- **Purpose:** System health check
- **Response:** Status, database status, version

---

## Serializers

### User Serializers
- `UserSerializer` - Basic user data
- `UserRegistrationSerializer` - Registration with birth data

### Data Serializers
- `NatalChartSerializer` - Natal chart data
- `DailyTransitSerializer` - Transit data
- `NatalWheelSerializer` - D3.js wheel format

### Content Serializers
- `GeneratedContentSerializer` - Full content data
- `GenerateContentSerializer` - Content generation input

### System Serializers
- `GCodeTemplateSerializer` - Template data
- `UserActivitySerializer` - Activity logging
- `DashboardOverviewSerializer` - Dashboard aggregation
- `ChartAnnotationSerializer` - Annotation CRUD

---

## Permissions

### Custom Permissions (`permissions.py`)

#### IsOwner
User can only access their own data.

#### IsOwnerOrReadOnly
Owners have full access, others read-only.

---

## WebSocket Consumers

### DashboardConsumer (`consumers/dashboard_consumer.py`)

**Purpose:** Real-time dashboard updates via WebSocket.

**Features:**
- User-specific channel subscription
- Auto-reconnection with exponential backoff
- Ping/pong keep-alive
- Broadcast events:
  - `gcode_updated` - New daily G-Code
  - `annotation_added` - New annotation
  - `content_generated` - New content

**Usage:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/dashboard/');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle updates
};
```

---

## URL Routing

### Main URL Configuration (`urls.py`)

```python
urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('natal/', NatalChartViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('natal/<int:pk>/', NatalChartViewSet.as_view({'get': 'retrieve'})),
    path('natal/wheel/', NatalWheelView.as_view(), name='natal-wheel'),
    path('gcode/', DailyTransitViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('gcode/<int:pk>/', DailyTransitViewSet.as_view({'get': 'retrieve'})),
    path('content/', GeneratedContentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('content/<int:pk>/', GeneratedContentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('annotations/', ChartAnnotationViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('annotations/<int:pk>/', ChartAnnotationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('dashboard/overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('dashboard/charts/', DashboardChartsView.as_view(), name='dashboard-charts'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
```

### WebSocket Routing (`core/routing.py`)

```python
websocket_urlpatterns = [
    re_path(r'ws/dashboard/$', DashboardConsumer.as_asgi()),
]
```

---

## Signals

### Signal Handlers (`signals.py`)

#### post_save_user
Automatically creates NatalChart when new GCodeUser is registered.

#### log_user_activity
Logs user actions to UserActivity model.

---

## Filters

### QuerySet Filters (`filters.py`)

#### DailyTransitFilter
- `user` - Filter by user ID
- `date__gte`, `date__lte` - Date range
- `intensity_level` - Filter by intensity

#### GeneratedContentFilter
- `user` - Filter by user ID
- `content_type` - Filter by content type
- `status` - Filter by status
- `platform` - Filter by platform

---

## HTML Views

### View Controllers (`views_html.py`)

Django views that render HTML templates (not REST API).

- `dashboard_view` - Main dashboard page
- `natal_chart_view` - Natal chart page
- `content_generation_view` - Content creation page
- `settings_view` - Settings page

---

## API Endpoints Summary

### Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Obtain JWT token |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |
| GET | `/api/auth/profile/` | Get user profile |
| PUT | `/api/auth/profile/` | Update profile |

### Natal Charts
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/natal/` | List natal charts |
| POST | `/api/natal/` | Calculate natal chart |
| GET | `/api/natal/{id}/` | Get natal chart |
| GET | `/api/natal/wheel/` | Get wheel data |

### Daily G-Code
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/gcode/` | List daily transits |
| POST | `/api/gcode/` | Calculate transit |
| GET | `/api/gcode/{id}/` | Get transit |
| GET | `/api/gcode/?user={id}&date={date}` | Filter by user/date |

### Content Generation
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/content/` | List content |
| POST | `/api/content/` | Generate content |
| GET | `/api/content/{id}/` | Get content |
| PUT | `/api/content/{id}/` | Update content |
| DELETE | `/api/content/{id}/` | Delete content |

### Annotations
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/annotations/` | List annotations |
| POST | `/api/annotations/` | Create annotation |
| GET | `/api/annotations/{id}/` | Get annotation |
| PUT | `/api/annotations/{id}/` | Update annotation |
| DELETE | `/api/annotations/{id}/` | Delete annotation |

### Dashboard
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/dashboard/overview/` | Dashboard overview |
| GET | `/api/dashboard/charts/` | Chart data |

### System
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health/` | Health check |

---

## Dependencies

### Python Packages
- `djangorestframework` >= 3.14.0
- `djangorestframework-simplejwt` >= 5.3.0
- `channels` >= 4.0.0
- `djoser` >= 2.2.0
- `django-filter` >= 23.5
- `psycopg2-binary` >= 2.9.0 (production)

---

## Testing

API tests are located in `tests/test_api.py`.

```bash
# Run API tests
pytest tests/test_api.py -v

# Run with coverage
pytest tests/test_api.py --cov=api --cov-report=html
```

---

## Related Documentation

- [Technical Architecture](../docs/TECHNICAL_ARCHITECTURE.md) - Complete system architecture
- [AI Engine](../ai_engine/README_AI_Engine.md) - Calculation and AI services
- [Django Core](../core/README_Django_Core.md) - Django project configuration
- [Testing](../tests/README_Testing.md) - Testing guide

---

**Last Updated:** 2026-01-15
