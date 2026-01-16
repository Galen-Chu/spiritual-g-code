# Frontend JavaScript Documentation

## Overview

The `static/js/` directory contains all client-side JavaScript for the Spiritual G-Code platform. The application uses vanilla JavaScript (ES6+) with a modular component-based architecture.

**Technology Stack:**
- Vanilla JavaScript (ES6+)
- Chart.js 4.4.0 (Data visualization)
- Cytoscape.js 3.28.1 (Network graphs)
- D3.js (Natal wheel visualization)
- No frontend framework (intentional for simplicity)

---

## Directory Structure

```
static/js/
├── main.js                 # Core utilities and API client
└── components/             # Modular JavaScript components
    ├── charts/             # Chart.js components (8 files)
    ├── annotations/        # Annotation system (2 files)
    ├── comparison/         # Date range comparison (2 files)
    ├── websocket/          # WebSocket client (1 file)
    └── wheel/              # Natal wheel renderer (1 file)
```

---

## Core JavaScript (`main.js`)

The main JavaScript file provides common utilities and helper functions used across the application.

### API Client

#### `apiRequest(endpoint, options)`
Makes authenticated API requests with automatic token refresh.

**Parameters:**
- `endpoint` (string) - API endpoint path (e.g., `/gcode/`)
- `options` (object) - Fetch API options (method, body, etc.)

**Returns:** Promise with JSON response

**Features:**
- Automatic JWT token injection
- Token refresh on 401 errors
- Error handling and logging

**Usage:**
```javascript
// GET request
const data = await apiRequest('/gcode/');

// POST request
const result = await apiRequest('/natal/', {
    method: 'POST',
    body: JSON.stringify({ birth_date: '2000-01-01' })
});
```

#### `refreshAccessToken()`
Refreshes JWT access token using refresh token.

**Process:**
1. Gets refresh token from localStorage
2. Calls `/api/auth/refresh/` endpoint
3. Updates access token in localStorage
4. Redirects to login if refresh fails

**Usage:** Automatic (called by `apiRequest()` on 401 errors)

### UI Utilities

#### `showToast(message, type)`
Displays toast notification to user.

**Parameters:**
- `message` (string) - Notification message
- `type` (string) - Notification type: `success`, `error`, `warning`, `info`

**Usage:**
```javascript
showToast('G-Code calculated successfully!', 'success');
showToast('Calculation failed', 'error');
```

#### `showLoading(message)` / `hideLoading()`
Displays/hides loading overlay.

**Parameters:**
- `message` (string) - Loading message (default: "Loading...")

**Usage:**
```javascript
showLoading('Calculating G-Code...');
// ... perform operation
hideLoading();
```

### Date Formatting

#### `formatDate(dateString)`
Formats date string to readable format.

**Returns:** "Jan 15, 2026"

#### `formatDateTime(dateString)`
Formats datetime string to readable format.

**Returns:** "Jan 15, 2026, 10:30 AM"

### Utility Functions

#### `debounce(func, wait)`
Debounces function execution.

**Parameters:**
- `func` (function) - Function to debounce
- `wait` (number) - Delay in milliseconds

**Usage:**
```javascript
const debouncedSearch = debounce(searchUsers, 300);
input.addEventListener('input', debouncedSearch);
```

#### `initializeCharts()`
Initializes Chart.js global configuration.

**Sets:**
- Default color: `#c9d1d9`
- Default font: "JetBrains Mono"
- Default border color: `#30363d`

---

## Component Architecture

### Design Principles

1. **Modularity:** Each component is a separate file with a single responsibility
2. **No Framework:** Pure vanilla JavaScript (no React, Vue, etc.)
3. **Reusability:** Components are designed to be reused across pages
4. **Isolation:** Components don't depend on each other (except utilities)
5. **Initialization:** Components have explicit initialization functions

### Component Structure

Each component file follows this pattern:

```javascript
/**
 * Component Name
 * Description of what this component does
 */

class ComponentName {
    constructor(elementId, options = {}) {
        this.element = document.getElementById(elementId);
        this.options = options;
        this.chart = null;
        this.data = null;
    }

    init() {
        // Initialize component
    }

    render() {
        // Render component
    }

    update(newData) {
        // Update component with new data
    }

    destroy() {
        // Clean up
    }
}

// Export for use in other files
window.ComponentName = ComponentName;
```

---

## Component Modules

### Charts (`components/charts/`)
Chart.js components for data visualization.

**Files:**
- `chart-utils.js` - Shared chart utilities
- `trend-chart.js` - G-Code 7-day trend line
- `planetary-chart.js` - Polar area chart (10 planets)
- `element-chart.js` - Horizontal bar chart (elements)
- `forecast-chart.js` - Weekly forecast line chart
- `aspects-network-chart.js` - Cytoscape.js network graph
- `export-utils.js` - Chart export (PNG/SVG)
- `chart-manager.js` - Centralized initialization

**Documentation:** [Chart Components](components/charts/README_Chart_Components.md)

### Annotations (`components/annotations/`)
User annotation system for chart data points.

**Files:**
- `annotation-manager.js` - CRUD operations
- `annotation-ui.js` - Modal, tooltips, context menu

**Documentation:** [Annotation System](components/annotations/README_Annotation_System.md)

### Comparison (`components/comparison/`)
Side-by-side date range comparison.

**Files:**
- `chart-comparator.js` - Comparison logic
- `date-range-picker.js` - Date selection UI

**Documentation:** [Comparison Feature](components/comparison/README_Comparison_Feature.md)

### WebSocket (`components/websocket/`)
Real-time dashboard updates via WebSocket.

**Files:**
- `dashboard-client.js` - WebSocket client with auto-reconnect

**Documentation:** [WebSocket Client](components/websocket/README_WebSocket_Client.md)

### Natal Wheel (`components/wheel/`)
Interactive zodiac wheel visualization.

**Files:**
- `d3-wheel-renderer.js` - D3.js circular wheel

**Documentation:** [Natal Wheel](components/wheel/README_Natal_Wheel.md)

---

## Using Components

### 1. Include Component Script

In your HTML template:

```html
<script src="{% static 'js/main.js' %}"></script>
<script src="{% static 'js/components/charts/trend-chart.js' %}"></script>
```

### 2. Initialize Component

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const trendChart = new TrendChart('trend-chart-canvas', {
        apiUrl: '/api/dashboard/charts/',
        chartType: 'line',
        colors: {
            primary: '#00FF41',
            secondary: '#7B3F00'
        }
    });

    trendChart.init();
});
```

### 3. Update Component

```javascript
// Fetch new data
const newData = await apiRequest('/gcode/?date=2026-01-15');

// Update chart
trendChart.update(newData);
```

---

## Global Variables

### Configuration

```javascript
const API_BASE_URL = '/api';          // API endpoint base URL
let accessToken = null;               // JWT access token (from localStorage)
```

### Local Storage

```javascript
// Authentication
localStorage.getItem('access_token');
localStorage.getItem('refresh_token');

// User preferences (optional)
localStorage.getItem('theme');
localStorage.getItem('chart_preferences');
```

---

## Event Handling

### DOMContentLoaded

All components initialize on page load:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    initializeCharts();

    // Initialize components
    // ... component initialization
});
```

### Custom Events

Components dispatch custom events for communication:

```javascript
// Dispatch event
document.dispatchEvent(new CustomEvent('chart:updated', {
    detail: { chartId: 'trend', data: newData }
}));

// Listen for event
document.addEventListener('chart:updated', (event) => {
    console.log('Chart updated:', event.detail);
});
```

---

## Error Handling

### API Errors

```javascript
try {
    const data = await apiRequest('/gcode/');
} catch (error) {
    console.error('API request failed:', error);
    showToast('Failed to load data', 'error');
}
```

### Chart Rendering Errors

```javascript
try {
    chart.render();
} catch (error) {
    console.error('Chart rendering failed:', error);
    showToast('Failed to render chart', 'error');
}
```

### WebSocket Errors

```javascript
ws.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
    showToast('Connection lost', 'warning');
});
```

---

## Performance Considerations

### Chart Optimization

1. **Debounce Updates:** Use `debounce()` for frequent updates
2. **Limit Data Points:** Show max 30-50 data points per chart
3. **Destroy Old Charts:** Call `chart.destroy()` before re-rendering

### Memory Management

```javascript
// Clean up when leaving page
window.addEventListener('beforeunload', function() {
    if (trendChart) {
        trendChart.destroy();
    }
});
```

### Lazy Loading

Load components only when needed:

```javascript
// Load chart component dynamically
const script = document.createElement('script');
script.src = '/static/js/components/charts/trend-chart.js';
document.head.appendChild(script);
```

---

## Browser Compatibility

**Supported Browsers:**
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

**Required Features:**
- ES6+ (arrow functions, async/await, classes)
- Fetch API
- Canvas API (for charts)
- WebSocket API (for real-time updates)

**Polyfills:** Not used (modern browsers only)

---

## Debugging

### Console Logging

```javascript
// Enable debug mode
localStorage.setItem('debug', 'true');

// Components check debug mode
if (localStorage.getItem('debug') === 'true') {
    console.log('Component initialized:', this);
}
```

### Network Requests

```javascript
// Log all API requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('Fetch:', args);
    return originalFetch.apply(this, args);
};
```

---

## Related Documentation

- [Chart Components](components/charts/README_Chart_Components.md) - Chart.js components
- [Annotation System](components/annotations/README_Annotation_System.md) - Annotation feature
- [Comparison Feature](components/comparison/README_Comparison_Feature.md) - Date comparison
- [WebSocket Client](components/websocket/README_WebSocket_Client.md) - Real-time updates
- [Natal Wheel](components/wheel/README_Natal_Wheel.md) - D3.js wheel
- [Templates](../../templates/README_Templates.md) - HTML templates

---

**Last Updated:** 2026-01-15
