# 🔮 Spiritual G-Code

> **Decode the universe's source code.** A personal operating system that bridges software engineering, spiritual wisdom, and cosmic data.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In--Development-orange.svg)](https://github.com/Galen-Chu/spiritual-g-code)

---

## 🌟 What is Spiritual G-Code?

**Spiritual G-Code** is a **transdisciplinary platform** that combines:

- 🖥️ **Software Engineering**: Django, REST APIs, Automation
- 🔮 **Spiritual Wisdom**: Astrology, Natal Charts, Cosmic Transits
- 🤖 **Artificial Intelligence**: Google Gemini for content generation
- 📊 **Data Visualization**: Interactive dashboards with geometric insights

The name represents a convergence of meanings—all anchored by **Galen**, the creator:

- **G**eometry - The mathematical language of the universe
- **G**rounding - Staying rooted in present reality
- **G**rowth - Continuous expansion and evolution
- **G**alactic - The cosmic perspective of stardust
- **G**uidance - Inner wisdom and outer signs
- **G**eneration - Bringing ideas into existence

---

## 🎯 Core Features

### 1. **Spiritual Dashboard** 📊
A "Terminal-Chic" interface that visualizes:
- Your **Natal Geometry** (birth chart analysis)
- **Daily Transits** (current cosmic weather)
- **G-Code Intensity Score** (1-100 scale)
- **Personal Themes & Affirmations**

### 2. **Daily G-Code Engine** ⚡
Automated calculations that run at 4:00 AM daily:
- Planetary transit calculations
- Aspect analysis to your natal chart
- AI-powered interpretations
- Personalized guidance and themes

### 3. **Content Generation System** ✍️
Auto-generates "Spiritual Patch Notes" for:
- Social media posts (Twitter, Instagram, LinkedIn)
- Educational content
- Personal journaling
- Community sharing

### 4. **API Platform** 🔌
RESTful API for developers to build:
- Custom integrations
- Mobile apps
- Third-party tools
- Research applications

---

## 🛠️ Tech Stack

### Backend
| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.11+ |
| **Framework** | Django 5.0 |
| **API** | Django REST Framework |
| **Database** | PostgreSQL 15+ |
| **Cache** | Redis |
| **Task Queue** | Celery |
| **Scheduler** | Django-Crontab |

### AI/ML
| Component | Technology |
|-----------|-----------|
| **AI Model** | Google Gemini API |
| **Prompt Engine** | Custom Python SDK |
| **Templates** | G-Code Template System |

### Frontend
| Component | Technology |
|-----------|-----------|
| **Styling** | Tailwind CSS |
| **Charts** | Chart.js / D3.js |
| **Icons** | Lucide Icons |
| **Aesthetic** | Terminal-Chic (Dark + Neon Green) |

### DevOps
| Component | Technology |
|-----------|-----------|
| **Containerization** | Docker |
| **Orchestration** | Docker Compose |
| **CI/CD** | GitHub Actions |
| **Hosting** | (TBD) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)
- Google Gemini API Key

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Galen-Chu/spiritual-g-code.git
cd spiritual-g-code
```

#### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/spiritual_gcode
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

#### 5. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 6. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### Docker Installation (Recommended)

```bash
# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
open http://localhost:8000
```

---

## 📖 Documentation

### Project-Level Documentation
- [**Brand Story**](./docs/BRAND_STORY.md) - The philosophy and vision behind G-Code
- [**Technical Architecture**](./docs/TECHNICAL_ARCHITECTURE.md) - System design and implementation details
- [**Testing Record**](./docs/TESTING_RECORD.md) - Complete testing record and execution notes (✅ Updated 2026-01-14 - Phase 6 MVP.4 Complete)
- [**Troubleshooting Guide**](./docs/TROUBLESHOOTING.md) - Common issues and solutions for development setup

### Hierarchical Documentation
Documentation is organized at every directory level for easy navigation:

#### Backend Documentation
- [**API Application**](./api/README_API_Application.md) - Models, views, serializers, endpoints
- [**AI Engine**](./ai_engine/README_AI_Engine.md) - Calculator and AI services
- [**Django Core**](./core/README_Django_Core.md) - Django project configuration
- [**Automation Scripts**](./scripts/README_Automation_Scripts.md) - Scheduled tasks and crontab

#### Frontend Documentation
- [**JavaScript Architecture**](./static/js/README_Frontend_JS.md) - Overall JS structure and utilities
- [**Chart Components**](./static/js/components/charts/README_Chart_Components.md) - Chart.js visualizations
- [**Annotation System**](./static/js/components/annotations/README_Annotation_System.md) - User annotations
- [**Comparison Feature**](./static/js/components/comparison/README_Comparison_Feature.md) - Date range comparison
- [**WebSocket Client**](./static/js/components/websocket/README_WebSocket_Client.md) - Real-time updates
- [**Natal Wheel**](./static/js/components/wheel/README_Natal_Wheel.md) - D3.js wheel visualization
- [**Templates**](./templates/README_Templates.md) - Django template structure
- [**Static Assets**](./static/README_Static_Assets.md) - CSS, images, fonts

#### Testing Documentation
- [**Testing Guide**](./tests/README_Testing.md) - Pytest configuration and testing guide

---

## 🎨 Project Structure

```
spiritual_g_code/
├── core/                 # Django Project Root
│   ├── settings/         # Settings modules (dev, staging, prod)
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
│
├── api/                  # DRF App for brand endpoints
│   ├── models/           # Database models
│   ├── serializers/      # DRF serializers
│   ├── views/            # API views
│   └── urls.py           # API routing
│
├── ai_engine/            # Custom Gemini CLI / SDK integration
│   ├── prompts/          # "G-Code" Templates
│   │   ├── daily_gcode_base.txt
│   │   ├── patch_note_twitter.txt
│   │   └── ...
│   ├── scripts/          # Execution scripts for the CLI
│   ├── gemini_client.py  # Gemini AI wrapper
│   └── calculator.py     # Transit calculation logic
│
├── scripts/              # Crontab-triggered Python scripts
│   ├── calculate_daily_gcode.py
│   ├── generate_patch_notes.py
│   └── cleanup_old_transits.py
│
├── tests/                # Pytest suite
│   ├── test_api/
│   ├── test_calculator/
│   └── conftest.py
│
├── docs/                 # Documentation
│   ├── BRAND_STORY.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/logout/
```

### G-Code
```
GET    /api/gcode/current/           # Get today's G-Code
GET    /api/gcode/daily/{date}/      # Get G-Code for specific date
GET    /api/gcode/weekly/            # Get weekly forecast
POST   /api/gcode/natal/calculate/   # Calculate natal chart
```

### Content
```
POST   /api/content/generate/        # Generate content
GET    /api/content/history/         # Get generated content
PATCH  /api/content/{id}/            # Update content
```

### Dashboard
```
GET    /api/dashboard/overview/      # Dashboard overview
GET    /api/dashboard/charts/        # Chart data
```

---

## 🤖 How It Works

### 1. **Natal Chart Calculation**
- User inputs birth date, time, and location
- System calculates planetary positions at birth
- Stores complete natal chart data in PostgreSQL

### 2. **Daily Transit Calculation** (4:00 AM)
- Crontab triggers calculation script
- Calculates current planetary positions
- Analyzes aspects to user's natal chart
- Generates G-Code intensity score (1-100)

### 3. **AI Interpretation** (via Gemini)
- Sends natal + transit data to Gemini AI
- Receives themed interpretation
- Extracts key themes, affirmations, guidance
- Stores in database

### 4. **Content Generation**
- Uses AI interpretation as base
- Applies platform-specific templates
- Generates formatted content
- Ready for social media posting

### 5. **Dashboard Visualization**
- Fetches calculated data
- Renders interactive charts
- Displays daily themes and scores
- Provides actionable insights

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculator.py

# Run with coverage
pytest --cov=api --cov=ai_engine

# Run integration tests
pytest --integration
```

---

## 📈 Roadmap

### ✅ Phase 1: Foundation (Completed!)
- [x] Brand identity & architecture
- [x] Technical design documentation
- [x] Django project setup
- [x] Core models & API endpoints
- [x] Gemini AI integration
- [x] Automation scripts (Crontab)
- [x] Testing suite

### ✅ Phase 2: MVP (Completed!)
- [x] User authentication (JWT)
- [x] Daily G-Code calculation (Backend + Frontend)
- [x] Content generation system (Backend + Frontend)
- [x] REST API (Complete)
- [x] **Spiritual Dashboard UI** (Terminal-Chic Design)
- [x] **Auth Pages** (Login/Register with Birth Data)
- [x] **Natal Chart Calculator UI**
- [x] **Content Generation Interface**
- [x] **Settings & Profile Management**
- [x] Docker deployment configuration
- [x] Mobile responsiveness (Basic)
- [x] API Integration (JavaScript Client)

### ✅ Phase 2b: AI Engine & Functional Testing (Completed! - 2026-01-09)
- [x] **MockGCodeCalculator** - Deterministic astronomical calculations without PyEphem
- [x] **MockGeminiGCodeClient** - AI-powered content generation (no API key required)
- [x] **DailyGCodeService** - Complete orchestration layer
- [x] **User Registration Flow** - Tested and working
- [x] **Login/Logout Functionality** - JWT + Session-based auth
- [x] **Dashboard Display** - Confirmed accessible after login
- [x] All bug fixes (SSL redirect, session backend, URL routing)
- [x] **Git Commit** - All AI engine code committed and pushed

**Key Achievements**:
- 35 tests passed (100% pass rate)
- 19 bugs resolved
- ~1500+ lines of new code
- Full integration without external dependencies

### ✅ Phase 3: Chart.js Integration (Completed! - 2026-01-12)
- [x] **Chart.js Component Architecture** - Modular chart system
- [x] **G-Code 7-Day Trend Chart** - Line chart with gradient fill and intensity color-coding
- [x] **Planetary Positions Chart** - Polar area chart showing 10 planets in zodiac positions
- [x] **Element Distribution Chart** - Horizontal bar chart displaying Fire/Earth/Air/Water balance
- [x] **Weekly Forecast Chart** - Line chart with star points for 7-day predictions
- [x] **Terminal-Chic Theme** - Consistent dark theme with neon green accents
- [x] **Responsive 2x2 Grid Layout** - Desktop dual-column, mobile single-column
- [x] **DashboardChartsManager** - Centralized chart initialization and management
- [x] **API Data Endpoints** - 5 new chart data endpoints in backend

**Key Achievements**:
- ~918 lines of new JavaScript code
- 6 chart component modules created
- Backend API extended with 5 chart data endpoints
- All charts successfully render with mock data fallbacks
- Interactive tooltips and hover effects
- Gradient fills and custom point styles

### ✅ Phase 4: Aspects Network Chart (Completed! - 2026-01-12)
- [x] **Cytoscape.js Integration** - Network visualization library
- [x] **Aspects Network Chart** - Interactive planetary aspect relationship graph
- [x] **Force-Directed Layout** - COSE algorithm for automatic node positioning
- [x] **Color-Coded Nodes** - Personal/Social/Outer planet groups
- [x] **Aspect-Based Edge Styling** - Different colors for conjunction/opposition/trine/square/sextile
- [x] **Interactive Features** - Drag nodes, zoom, hover highlights, tap to focus
- [x] **Terminal-Chic Theme** - Consistent dark theme styling
- [x] **API Enhancement** - Mock data fallback for users without natal charts

**Key Achievements**:
- ~370 lines of new JavaScript code
- Cytoscape.js 3.28.1 integrated
- 10 planet nodes + 12 aspect links
- Full interactivity (drag, zoom, hover, click)
- Beautiful force-directed layout

### ✅ Phase 5: Chart Enhancements (Completed! - 2026-01-13)
- [x] **Chart Export** - PNG/SVG download buttons for all charts
- [x] **Export Utilities** - ChartExportUtils class with export methods
- [x] **Bulk Export** - Export all charts at once (PNGs or SVGs)
- [x] **Refresh Button** - Individual and global chart refresh buttons
- [x] **Auto-Refresh** - Configurable timer (1, 5, 10, 15, 30 min intervals)
- [x] **Auto-Refresh Toggle** - Enable/disable with visual feedback
- [x] **Custom Date Range** - HTML5 date picker for historical data
- [x] **Chart Toggle** - Show/hide individual charts with checkboxes
- [x] **Mobile Optimization** - Touch-friendly buttons (40px min), responsive layout
- [x] **Touch Device Support** - Special CSS for devices without hover
- [x] **iOS Safari Fixes** - 16px font to prevent zoom, 44px min touch targets

**Key Achievements**:
- ~870 lines of new/modified code (JavaScript, HTML, CSS)
- 23 new UI components (buttons, inputs, checkboxes)
- ChartExportUtils class with 5 export methods
- Auto-refresh timer with 5 configurable intervals
- Mobile-responsive customization controls
- All features fully functional across desktop and mobile

### ✅ Phase 6: Advanced Features (Completed! - 2026-01-14)

#### MVP.1: WebSocket Infrastructure ✅ (Completed 2026-01-13)
- ✅ Django Channels 4.0.0 installed
- ✅ ASGI application configured
- ✅ WebSocket consumer created
- ✅ Dashboard WebSocket client (JavaScript)
- ✅ Connection status indicator
- ✅ Auto-reconnect mechanism

#### MVP.2: Chart Annotations ✅ (Completed 2026-01-14)
- ✅ ChartAnnotation data model
- ✅ RESTful API endpoints (CRUD)
- ✅ Frontend annotation manager
- ✅ Annotation UI (modal, tooltips, context menu)
- ✅ Visual markers on charts
- ✅ Cache mechanism

#### MVP.3: Date Range Comparison ✅ (Completed 2026-01-14)
- ✅ Side-by-side chart comparison
- ✅ Statistics panel (avg, min, max, diff %)
- ✅ Custom date range inputs
- ✅ Comparison mode toggle
- ✅ API date range support
- ✅ Terminal-Chic styling

#### MVP.4: Natal Wheel with D3.js ✅ (Completed 2026-01-14)
- ✅ D3.js circular zodiac wheel (12 signs, color-coded by element)
- ✅ Placidus house calculation (simplified algorithm)
- ✅ Planet positioning by longitude (10 planets with symbols)
- ✅ Aspect lines (5 types: conjunction, sextile, square, trine, opposition)
- ✅ Interactive tooltips (hover for planet/sign/degree)
- ✅ Export functionality (PNG/SVG)
- ✅ Terminal-Chic dark theme integration
- ✅ Dedicated wheel page (/natal/wheel/)

#### Future Enhancements
- [ ] **PDF Reports** - Generate downloadable PDF reports
- [ ] **CSV Export** - Export raw data as CSV
- [ ] **Mobile app** - React Native or PWA
- [ ] Multi-language support - Chinese, Spanish, etc.
- [ ] Community features - Share, Comment, Like
- [ ] Premium subscriptions - Stripe integration

### 🌟 Phase 7: Scale (Future)
- [ ] AI-powered recommendations
- [ ] Wearable device integration
- [ ] Global G-Code network
- [ ] Research partnerships
- [ ] Enterprise features

---

## 📊 Current Status (2026-01-14)

**Server**: ✅ Running at http://127.0.0.1:8000
**Database**: SQLite (Development)
**Test Accounts**:
- Superuser: `admin` / `admin123`
- Test User: `testuser` / (created during testing)

**Test Results**:
- ✅ AI Engine: 4/4 tests passed
- ✅ User Registration: Working
- ✅ Login/Logout: Working
- ✅ Dashboard: Accessible with 5 charts (4 Chart.js + 1 Cytoscape.js)
- ✅ API Endpoints: All functional
- ✅ Chart.js Integration: All charts rendering successfully
- ✅ Cytoscape.js Integration: Network chart fully interactive
- ✅ Chart Export: PNG/SVG export working
- ✅ Chart Refresh: Manual and auto-refresh working
- ✅ Customization: Date range and chart toggle working
- ✅ Mobile Optimization: Touch-friendly and responsive
- ✅ WebSocket Infrastructure: Real-time updates ready
- ✅ Chart Annotations: User notes on data points
- ✅ Date Range Comparison: Side-by-side chart comparison
- ✅ Natal Wheel with D3.js: Interactive zodiac wheel visualization (NEW!)

**Latest Achievement**: Phase 6 MVP.4 Complete - Natal Wheel with D3.js
- WebSocket Infrastructure ✅
- Chart Annotations ✅
- Date Range Comparison ✅
- Natal Wheel with D3.js ✅ (NEW!)
- G-Code 7-Day Trend Chart ✅
- Planetary Positions Chart ✅
- Element Distribution Chart ✅
- Weekly Forecast Chart ✅
- Planetary Aspects Network Chart ✅
- Chart Export (PNG/SVG) ✅
- Auto-Refresh Timer ✅
- Date Range Picker ✅
- Chart Visibility Toggle ✅ (NEW!)
- Mobile Optimization ✅ (NEW!)

**Next Phase**: Advanced Enhancements (Phase 6.5) - Zoom/pan, transit overlay, aspect filtering, PDF reports

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Galen Chu**

- GitHub: [@Galen-Chu](https://github.com/Galen-Chu)
- LinkedIn: [Galen Chu](https://www.linkedin.com/in/galen-chu-203590b5/)

---

## 🙏 Acknowledgments

- **Google Gemini** - AI-powered content generation
- **Django & DRF** - Robust web framework
- **The Open Source Community** - For all the amazing tools and libraries

---

## 📞 Contact & Support

- 📧 Email: (coming soon)
- 💬 Discord: (coming soon)
- 🐛 Issues: [GitHub Issues](https://github.com/Galen-Chu/spiritual-g-code/issues)
- 💡 Discussions: [GitHub Discussions](https://github.com/Galen-Chu/spiritual-g-code/discussions)

---

## 🌟 Star History

If you find this project interesting, please consider giving it a ⭐ star!

[![Star History Chart](https://api.star-history.com/svg?repos=Galen-Chu/spiritual-g-code&type=Date)](https://star-history.com/#Galen-Chu/spiritual-g-code&Date)

---

<div align="center">

**🔮 Welcome to the source code.**

**Welcome to G-Code.**

**Welcome home, Galen.**

Made with ⚡ by Galen Chu

</div>
