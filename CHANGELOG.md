# Changelog

All notable changes to the Spiritual G-Code project will be documented in this file.

## [Unreleased]

### Future Enhancements (Planned)
- PDF Reports - Generate downloadable PDF reports
- CSV Export - Export raw data as CSV
- Mobile app - React Native or PWA
- Multi-language support - Chinese, Spanish, etc.
- Community features - Share, Comment, Like
- Premium subscriptions - Stripe integration
- AI-powered recommendations
- Wearable device integration
- Global G-Code network
- Research partnerships
- Enterprise features

## [0.6.5] - 2026-01-26

### Bug Fixes
- Fixed Planetary Chart Legend - Corrected generateLabels function to return proper Chart.js legend objects instead of strings
- Fixed Cytoscape Selectors - Changed from invalid `node:hover` to `node.hover` with event handlers
- Fixed Dashboard Loading State - Added ID to cosmic status element and updated text after dashboard loads
- Fixed Natal Chart Authentication - Updated to use JWT authentication with Authorization header
- Fixed Dashboard Natal Chart Display - Added natal_chart field to DashboardOverviewSerializer and updateNatalChartSigns() function
- Fixed Auto-complete Attributes - Added proper autocomplete attributes to login form inputs

### Resolved Issues
- JavaScript error: `Cannot create property 'textAlign' on string` - RESOLVED
- Cytoscape error: `The selector 'node:hover' is invalid` - RESOLVED
- Dashboard stuck on "Loading cosmic data..." - RESOLVED
- Natal chart calculation returning 401 Unauthorized - RESOLVED
- Natal chart signs not displaying on dashboard - RESOLVED

## [0.6.0] - 2026-01-14

### Phase 6: Advanced Features

#### MVP.1: WebSocket Infrastructure (2026-01-13)
- Django Channels 4.0.0 installed
- ASGI application configured
- WebSocket consumer created
- Dashboard WebSocket client (JavaScript)
- Connection status indicator
- Auto-reconnect mechanism

#### MVP.2: Chart Annotations (2026-01-14)
- ChartAnnotation data model
- RESTful API endpoints (CRUD)
- Frontend annotation manager
- Annotation UI (modal, tooltips, context menu)
- Visual markers on charts
- Cache mechanism

#### MVP.3: Date Range Comparison (2026-01-14)
- Side-by-side chart comparison
- Statistics panel (avg, min, max, diff %)
- Custom date range inputs
- Comparison mode toggle
- API date range support
- Terminal-Chic styling

#### MVP.4: Natal Wheel with D3.js (2026-01-14)
- D3.js circular zodiac wheel (12 signs, color-coded by element)
- Placidus house calculation (simplified algorithm)
- Planet positioning by longitude (10 planets with symbols)
- Aspect lines (5 types: conjunction, sextile, square, trine, opposition)
- Interactive tooltips (hover for planet/sign/degree)
- Export functionality (PNG/SVG)
- Terminal-Chic dark theme integration
- Dedicated wheel page (/natal/wheel/)

## [0.5.0] - 2026-01-13

### Phase 5: Chart Enhancements
- Chart Export - PNG/SVG download buttons for all charts
- Export Utilities - ChartExportUtils class with export methods
- Bulk Export - Export all charts at once (PNGs or SVGs)
- Refresh Button - Individual and global chart refresh buttons
- Auto-Refresh - Configurable timer (1, 5, 10, 15, 30 min intervals)
- Auto-Refresh Toggle - Enable/disable with visual feedback
- Custom Date Range - HTML5 date picker for historical data
- Chart Toggle - Show/hide individual charts with checkboxes
- Mobile Optimization - Touch-friendly buttons (40px min), responsive layout
- Touch Device Support - Special CSS for devices without hover
- iOS Safari Fixes - 16px font to prevent zoom, 44px min touch targets

### Key Achievements
- ~870 lines of new/modified code (JavaScript, HTML, CSS)
- 23 new UI components (buttons, inputs, checkboxes)
- ChartExportUtils class with 5 export methods
- Auto-refresh timer with 5 configurable intervals
- Mobile-responsive customization controls
- All features fully functional across desktop and mobile

## [0.4.0] - 2026-01-12

### Phase 4: Aspects Network Chart
- Cytoscape.js Integration - Network visualization library
- Aspects Network Chart - Interactive planetary aspect relationship graph
- Force-Directed Layout - COSE algorithm for automatic node positioning
- Color-Coded Nodes - Personal/Social/Outer planet groups
- Aspect-Based Edge Styling - Different colors for conjunction/opposition/trine/square/sextile
- Interactive Features - Drag nodes, zoom, hover highlights, tap to focus
- Terminal-Chic Theme - Consistent dark theme styling
- API Enhancement - Mock data fallback for users without natal charts

### Key Achievements
- ~370 lines of new JavaScript code
- Cytoscape.js 3.28.1 integrated
- 10 planet nodes + 12 aspect links
- Full interactivity (drag, zoom, hover, click)
- Beautiful force-directed layout

## [0.3.0] - 2026-01-12

### Phase 3: Chart.js Integration
- Chart.js Component Architecture - Modular chart system
- G-Code 7-Day Trend Chart - Line chart with gradient fill and intensity color-coding
- Planetary Positions Chart - Polar area chart showing 10 planets in zodiac positions
- Element Distribution Chart - Horizontal bar chart displaying Fire/Earth/Air/Water balance
- Weekly Forecast Chart - Line chart with star points for 7-day predictions
- Terminal-Chic Theme - Consistent dark theme with neon green accents
- Responsive 2x2 Grid Layout - Desktop dual-column, mobile single-column
- DashboardChartsManager - Centralized chart initialization and management
- API Data Endpoints - 5 new chart data endpoints in backend

### Key Achievements
- ~918 lines of new JavaScript code
- 6 chart component modules created
- Backend API extended with 5 chart data endpoints
- All charts successfully render with mock data fallbacks
- Interactive tooltips and hover effects
- Gradient fills and custom point styles

## [0.2.1] - 2026-01-09

### Phase 2b: AI Engine & Functional Testing
- MockGCodeCalculator - Deterministic astronomical calculations without PyEphem
- MockGeminiGCodeClient - AI-powered content generation (no API key required)
- DailyGCodeService - Complete orchestration layer
- User Registration Flow - Tested and working
- Login/Logout Functionality - JWT + Session-based auth
- Dashboard Display - Confirmed accessible after login
- All bug fixes (SSL redirect, session backend, URL routing)
- Git Commit - All AI engine code committed and pushed

### Key Achievements
- 35 tests passed (100% pass rate)
- 19 bugs resolved
- ~1500+ lines of new code
- Full integration without external dependencies

## [0.2.0] - 2025-12-XX

### Phase 2: MVP
- User authentication (JWT)
- Daily G-Code calculation (Backend + Frontend)
- Content generation system (Backend + Frontend)
- REST API (Complete)
- Spiritual Dashboard UI (Terminal-Chic Design)
- Auth Pages (Login/Register with Birth Data)
- Natal Chart Calculator UI
- Content Generation Interface
- Settings & Profile Management
- Docker deployment configuration
- Mobile responsiveness (Basic)
- API Integration (JavaScript Client)

## [0.1.0] - 2025-12-XX

### Phase 1: Foundation
- Brand identity & architecture
- Technical design documentation
- Django project setup
- Core models & API endpoints
- Gemini AI integration
- Automation scripts (Crontab)
- Testing suite

---

## Version Convention

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

---

## Links

- [GitHub Repository](https://github.com/Galen-Chu/spiritual-g-code)
- [Issue Tracker](https://github.com/Galen-Chu/spiritual-g-code/issues)
- [Documentation](./docs/README.md)
