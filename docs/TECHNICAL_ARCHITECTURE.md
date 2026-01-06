# Spiritual G-Code: Technical Architecture

## 🏗️ System Overview

The Spiritual G-Code platform is a **full-stack web application** that combines Django REST Framework for the backend, a modern frontend for the dashboard, and Google Gemini AI for intelligent content generation.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Web Dashboard│  │  Mobile App  │  │  API Clients │      │
│  │  (Tailwind)  │  │  (Future)    │  │  (External)  │      │
│  └──────┬───────┘  └──────┬───���───┘  └──────┬───────┘      │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                    ┌───────▼────────┐
                    │  API Gateway   │
                    │  (Django DRF)  │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌──────▼─────────┐
│  Core Service  │  │  AI Engine     │  │  Scheduler     │
│  - User Mgmt   │  │  - Gemini AI   │  │  - Crontab     │
│  - Natal Data  │  │  - Prompts     │  │  - Daily Calc  │
│  - Transits    │  │  - Templates   │  │  - Patch Notes │
└───────┬────────┘  └───────┬────────┘  └──────┬─────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌──────▼─────────┐
│  PostgreSQL   │  │  Redis Cache  │  │  File Storage  │
│  - User Data  │  │  - Sessions   │  │  - Images      │
│  - Charts     │  │  - API Cache  │  │  - Exports     │
└───────────────┘  └────────────────┘  └────────────────┘
```

---

## 🛠️ Technology Stack

### Backend Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11+ | Core backend logic |
| **Framework** | Django 5.0 | Web framework & ORM |
| **API** | Django REST Framework | RESTful API endpoints |
| **Task Queue** | Celery + Redis | Asynchronous task processing |
| **Scheduler** | Django-Crontab | Periodic jobs (Daily G-Code) |
| **Database** | PostgreSQL 15+ | Primary data storage |
| **Cache** | Redis | Session & API caching |

### AI/ML Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Model** | Google Gemini API | Content generation & insights |
| **Prompt Engine** | Custom Python SDK | G-Code template management |
| **Text Processing** | spaCy / NLTK | NLP for spiritual content |

### Frontend Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Vanilla JS / HTMX | Lightweight interactivity |
| **Styling** | Tailwind CSS | Terminal-chic aesthetic |
| **Charts** | Chart.js / D3.js | Data visualizations |
| **Icons** | Lucide Icons | Geometric icon set |

### DevOps Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Containerization** | Docker | Environment consistency |
| **Orchestration** | Docker Compose | Local development |
| **CI/CD** | GitHub Actions | Automated testing & deployment |
| **Hosting** | (TBD: AWS/GCP/DigitalOcean) | Production deployment |

---

## 📊 Database Schema

### Core Tables

#### 1. Users Table
```sql
CREATE TABLE gcode_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    birth_date DATE NOT NULL,           -- For Natal Chart calculations
    birth_time TIME,                     -- Optional but recommended
    birth_location VARCHAR(100),         -- City, Country or Lat/Long
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 2. Natal Charts Table
```sql
CREATE TABLE natal_charts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES gcode_users(id),
    chart_data JSONB NOT NULL,           -- Complete natal chart
    sun_sign VARCHAR(20),
    moon_sign VARCHAR(20),
    ascendant VARCHAR(20),
    dominant_elements JSONB,             -- Element distribution
    key_aspects JSONB,                   -- Major planetary aspects
    calculated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3. Daily Transits Table
```sql
CREATE TABLE daily_transits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES gcode_users(id),
    transit_date DATE NOT NULL,
    transit_data JSONB NOT NULL,         -- Planetary positions
    aspects_to_natal JSONB,              -- Aspects to natal chart
    g_code_score INTEGER,                -- Daily G-Code (1-100)
    themes TEXT[],                       -- Key themes for the day
    intensity_level VARCHAR(20),         -- Low / Medium / High
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, transit_date)
);
```

#### 4. Generated Content Table
```sql
CREATE TABLE generated_content (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES gcode_users(id),
    content_type VARCHAR(50),            -- 'patch_note', 'insight', etc.
    title VARCHAR(200),
    body TEXT NOT NULL,
    hashtags TEXT[],
    platform VARCHAR(50),                -- 'twitter', 'instagram', etc.
    status VARCHAR(20) DEFAULT 'draft',  -- 'draft', 'posted', 'scheduled'
    generated_at TIMESTAMP DEFAULT NOW(),
    posted_at TIMESTAMP
);
```

#### 5. G-Code Templates Table
```sql
CREATE TABLE gcode_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),                -- 'daily', 'weekly', 'retrograde'
    prompt_template TEXT NOT NULL,
    variables JSONB,                     -- Placeholder variables
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔌 API Endpoints

### Authentication Endpoints

```
POST   /api/auth/register/           # User registration
POST   /api/auth/login/              # User login
POST   /api/auth/logout/             # User logout
POST   /api/auth/refresh/            # Refresh JWT token
```

### User Management

```
GET    /api/users/me/                # Current user profile
PATCH  /api/users/me/                # Update profile
GET    /api/users/{id}/natal/        # Get natal chart
```

### G-Code Calculation

```
POST   /api/gcode/natal/calculate/   # Calculate natal chart
GET    /api/gcode/daily/{date}/      # Get daily transits
GET    /api/gcode/weekly/            # Get weekly forecast
GET    /api/gcode/current/           # Get today's G-Code
```

### Content Generation

```
POST   /api/content/generate/        # Generate content
GET    /api/content/history/         # Get generated content
PATCH  /api/content/{id}/            # Update content
DELETE /api/content/{id}/            # Delete content
```

### Dashboard Data

```
GET    /api/dashboard/overview/      # Dashboard overview
GET    /api/dashboard/charts/        # Chart data for visualizations
GET    /api/dashboard/stats/         # User statistics
```

---

## 🤖 AI Engine Architecture

### Gemini Integration

```python
# ai_engine/gemini_client.py

import google.generativeai as genai
from typing import Dict, List, Optional

class GeminiGCodeClient:
    """Custom Gemini client for G-Code generation"""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_daily_gcode(
        self,
        natal_data: Dict,
        transit_data: Dict,
        user_preferences: Optional[Dict] = None
    ) -> Dict:
        """Generate Daily G-Code interpretation"""

        prompt = self._build_daily_prompt(
            natal_data,
            transit_data,
            user_preferences
        )

        response = self.model.generate_content(prompt)

        return {
            'interpretation': response.text,
            'themes': self._extract_themes(response.text),
            'affirmations': self._extract_affirmations(response.text),
            'score': self._calculate_gcode_score(transit_data)
        }

    def generate_spiritual_patch_note(
        self,
        daily_gcode: Dict,
        platform: str = 'twitter'
    ) -> str:
        """Generate social media content"""

        template = self._load_template(f'patch_note_{platform}')

        prompt = template.format(
            themes=', '.join(daily_gcode['themes']),
            score=daily_gcode['score'],
            key_insight=daily_gcode['interpretation'][:200]
        )

        response = self.model.generate_content(prompt)

        return response.text

    def _build_daily_prompt(
        self,
        natal_data: Dict,
        transit_data: Dict,
        preferences: Optional[Dict]
    ) -> str:
        """Build structured prompt for daily G-Code"""

        # Load base template
        base_template = self._load_template('daily_gcode_base')

        # Inject data
        prompt = base_template.format(
            sun_sign=natal_data['sun_sign'],
            moon_sign=natal_data['moon_sign'],
            ascendant=natal_data['ascendant'],
            major_transits=self._format_transits(transit_data),
            user_tone=preferences.get('tone', 'inspiring') if preferences else 'inspiring'
        )

        return prompt
```

### Prompt Templates

```python
# ai_engine/prompts/daily_gcode_base.txt

You are the Spiritual G-Code interpreter—a bridge between cosmic data and human understanding.

## Natal Configuration
- Sun Sign: {sun_sign}
- Moon Sign: {moon_sign}
- Ascendant: {ascendant}

## Current Transits
{major_transits}

## Your Task
Provide a Daily G-Code interpretation that:

1. **Highlights the key theme** of the day (1 sentence)
2. **Explains the cosmic weather** in accessible terms (2-3 sentences)
3. **Offers practical guidance** on how to navigate the day (2-3 sentences)
4. **Identifies 3 key themes** as hashtags
5. **Calculates a G-Code intensity score** (1-100, where 100 = most transformative)

## Tone
{user_tone}, precise, poetic, and practical. Blend scientific accuracy with spiritual wisdom.

## Output Format
```json
{{
  "theme": "Theme of the day",
  "interpretation": "Full interpretation",
  "themes": ["#theme1", "#theme2", "#theme3"],
  "affirmation": "Daily affirmation",
  "practical_guidance": ["tip1", "tip2", "tip3"],
  "score": 75
}}
```
```

---

## ⏰ Scheduler & Automation

### Daily G-Code Calculation (Crontab)

```python
# scripts/calculate_daily_gcode.py

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User, DailyTransit
from ai_engine.calculator import GCodeCalculator
from ai_engine.gemini_client import GeminiGCodeClient

def calculate_all_daily_gcodes():
    """Calculate G-Code for all users at 4:00 AM"""

    calculator = GCodeCalculator()
    ai_client = GeminiGCodeClient(api_key=os.getenv('GEMINI_API_KEY'))

    # Get tomorrow's date
    tomorrow = date.today() + timedelta(days=1)

    # Calculate for all active users
    for user in User.objects.filter(is_active=True):
        try:
            # 1. Calculate planetary transits
            transit_data = calculator.calculate_transits(
                user.birth_date,
                user.birth_location,
                tomorrow
            )

            # 2. Get natal chart
            natal_chart = user.natal_charts.first()

            # 3. Generate AI interpretation
            gcode_interpretation = ai_client.generate_daily_gcode(
                natal_data=natal_chart.chart_data,
                transit_data=transit_data
            )

            # 4. Save to database
            DailyTransit.objects.update_or_create(
                user=user,
                transit_date=tomorrow,
                defaults={
                    'transit_data': transit_data,
                    'aspects_to_natal': gcode_interpretation['aspects'],
                    'g_code_score': gcode_interpretation['score'],
                    'themes': gcode_interpretation['themes'],
                    'intensity_level': _get_intensity(gcode_interpretation['score'])
                }
            )

            print(f"✅ G-Code calculated for {user.username}")

        except Exception as e:
            print(f"❌ Error calculating for {user.username}: {str(e)}")

if __name__ == '__main__':
    calculate_all_daily_gcodes()
```

### Crontab Configuration

```python
# core/crontab.py

from django_crontab import CrontabCommand

CRONJOBS = [
    # Calculate Daily G-Code at 4:00 AM every day
    ('0 4 * * *', 'scripts.calculate_daily_gcode.calculate_all_daily_gcodes', '>> /tmp/gcode_calc.log'),

    # Generate Spiritual Patch Notes at 5:00 AM every day
    ('0 5 * * *', 'scripts.generate_patch_notes.generate_all', '>> /tmp/patch_notes.log'),

    # Clean up old transits (keep only 90 days)
    ('0 3 * * 0', 'scripts.cleanup_old_transits.cleanup', '>> /tmp/cleanup.log'),
]
```

---

## 🎨 Frontend Architecture

### Dashboard Components

```html
<!-- templates/dashboard/index.html -->

<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spiritual G-Code | Dashboard</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- Custom Config -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        gcode: {
                            green: '#00FF41',      /* Terminal green */
                            dark: '#0D1117',        /* GitHub dark */
                            accent: '#58A6FF'       /* Accent blue */
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gcode-dark text-green-400 font-mono">

    <!-- Navigation -->
    <nav class="border-b border-green-900 p-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold">SPIRITUAL<span class="text-white">G-</span>CODE</h1>
            <div class="flex gap-4">
                <a href="/dashboard/" class="hover:text-white">Dashboard</a>
                <a href="/natal/" class="hover:text-white">Natal Chart</a>
                <a href="/content/" class="hover:text-white">Content</a>
                <a href="/settings/" class="hover:text-white">Settings</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto p-6">

        <!-- Today's G-Code Card -->
        <div class="bg-gcode-dark border border-green-900 rounded-lg p-6 mb-6">
            <h2 class="text-xl font-bold mb-4">Today's G-Code</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- Score -->
                <div class="text-center">
                    <div class="text-6xl font-bold" id="gcode-score">--</div>
                    <div class="text-sm mt-2">G-Code Intensity</div>
                </div>
                <!-- Theme -->
                <div class="text-center">
                    <div class="text-2xl font-bold" id="gcode-theme">Loading...</div>
                    <div class="text-sm mt-2">Today's Theme</div>
                </div>
                <!-- Affirmation -->
                <div class="text-center">
                    <div class="text-lg italic" id="gcode-affirmation">Loading...</div>
                    <div class="text-sm mt-2">Daily Affirmation</div>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Natal Geometry Chart -->
            <div class="bg-gcode-dark border border-green-900 rounded-lg p-6">
                <h3 class="text-lg font-bold mb-4">Natal Geometry</h3>
                <canvas id="natalChart"></canvas>
            </div>

            <!-- Current Transits Chart -->
            <div class="bg-gcode-dark border border-green-900 rounded-lg p-6">
                <h3 class="text-lg font-bold mb-4">Current Transits</h3>
                <canvas id="transitChart"></canvas>
            </div>
        </div>

    </main>

    <!-- JavaScript -->
    <script>
        // Fetch today's G-Code
        fetch('/api/gcode/current/')
            .then(res => res.json())
            .then(data => {
                document.getElementById('gcode-score').textContent = data.score;
                document.getElementById('gcode-theme').textContent = data.theme;
                document.getElementById('gcode-affirmation').textContent = data.affirmation;
            });

        // Initialize Charts (using Chart.js)
        // ... chart initialization code
    </script>

</body>
</html>
```

---

## 🐳 Docker Configuration

### Dockerfile

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: spiritual_gcode
      POSTGRES_USER: gcode_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://gcode_user:${DB_PASSWORD}@db:5432/spiritual_gcode
      - REDIS_URL=redis://redis:6379/0
      - GEMINI_API_KEY=${GEMINI_API_KEY}

  celery:
    build: .
    command: celery -A core worker -l info
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://gcode_user:${DB_PASSWORD}@db:5432/spiritual_gcode
      - REDIS_URL=redis://redis:6379/0
      - GEMINI_API_KEY=${GEMINI_API_KEY}

volumes:
  postgres_data:
```

---

## 🚀 Deployment Strategy

### Phase 1: Development (Current)
- Local development with Docker Compose
- GitHub for version control
- Manual testing

### Phase 2: Staging (Months 1-3)
- Deploy to DigitalOcean Droplet / AWS EC2
- Automated testing with GitHub Actions
- Beta testing with selected users

### Phase 3: Production (Months 3-6)
- Load balancer + multiple web servers
- Redis cluster for caching
- PostgreSQL replication
- CDN for static assets
- Monitoring with Sentry / New Relic

---

## 📈 Monitoring & Analytics

### Key Metrics to Track
- Daily Active Users (DAU)
- G-Code calculations per day
- Content generation success rate
- API response times
- Error rates by endpoint

### Logging Strategy
```python
# core/settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/gcode/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'gcode': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

---

## 🔒 Security Considerations

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- API rate limiting
- CORS configuration

### Data Protection
- Encryption at rest (PostgreSQL)
- Encryption in transit (HTTPS/TLS)
- PII hashing for sensitive data
- Regular security audits

### API Security
- Input validation & sanitization
- SQL injection prevention (ORM)
- XSS protection
- CSRF tokens

---

## 📚 API Documentation

### Interactive API Docs
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

### Generated by drf-spectacular
```python
# core/settings.py

INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/test_calculator.py

import pytest
from ai_engine.calculator import GCodeCalculator

class TestGCodeCalculator:
    def test_calculate_transits(self):
        calculator = GCodeCalculator()
        result = calculator.calculate_transits(
            birth_date='1990-06-15',
            location='Taipei, Taiwan',
            target_date='2025-01-06'
        )
        assert 'sun' in result
        assert 'moon' in result
        assert 'aspects' in result
```

### Integration Tests
```python
# tests/test_api.py

from rest_framework.test import APITestCase

class TestGCodeAPI(APITestCase):
    def test_get_current_gcode(self):
        response = self.client.get('/api/gcode/current/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('score', response.data)
```

---

## 🔄 Development Workflow

### Git Flow
```
main (production)
  ↑
develop (staging)
  ↑
feature/* (branches)
```

### Commit Convention
```
feat: add daily G-Code calculation
fix: resolve transit chart rendering bug
docs: update API documentation
style: format code with black
refactor: simplify calculator logic
test: add unit tests for Gemini client
chore: update Dockerfile
```

---

## 📝 Next Steps

1. ✅ Brand & architecture defined
2. ⏳ Set up Django project structure
3. ⏳ Implement core models & API endpoints
4. ⏳ Integrate Gemini AI
5. ⏳ Build dashboard UI
6. ⏳ Set up automation (Crontab)
7. ⏳ Deploy to staging
8. ⏳ Beta testing & iteration

---

*This architecture is a living document, evolving as the project grows.*
*Last Updated: 2025-01-06*
