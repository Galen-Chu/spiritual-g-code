# Django Templates Documentation

## Overview

The `templates/` directory contains all HTML templates for the Spiritual G-Code platform. Templates use Django Template Language (DTL) and follow the terminal-chic design aesthetic.

**Technology:**
- Django Template Language (DTL)
- Tailwind CSS (CDN)
- Vanilla JavaScript (ES6+)

---

## Directory Structure

```
templates/
├── base.html               # Base template with navigation
├── auth/
│   ├── login.html         # Login page
│   └── register.html      # Registration page
├── dashboard/
│   └── index.html         # Main dashboard
├── natal/
│   ├── index.html         # Natal chart page
│   └── wheel.html         # Interactive natal wheel
├── content/
│   └── index.html         # Content generation page
└── settings/
    └── index.html         # Settings page
```

---

## Base Template

### `base.html`

The base template provides:
- HTML5 doctype and structure
- Tailwind CSS CDN
- Google Fonts (JetBrains Mono)
- Lucide Icons
- Navigation bar
- Toast notification container
- JavaScript includes
- CSRF token

**Key Sections:**

#### HTML Head
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Spiritual G-Code{% endblock %}</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    {% block extra_css %}{% endblock %}
</head>
```

#### Navigation
```html
<nav class="bg-gcode-dark border-b border-gcode-border">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Navigation links -->
    </div>
</nav>
```

#### Content Blocks
```html
<main class="min-h-screen bg-gcode-bg">
    {% block content %}{% endblock %}
</main>

<div id="toast-container"></div>
```

#### JavaScript
```html
<script src="{% static 'js/main.js' %}"></script>
{% block extra_js %}{% endblock %}
```

---

## Auth Templates

### `auth/login.html`

**Purpose:** User login page.

**Features:**
- Email/username input
- Password input
- Remember me checkbox
- "Forgot password" link
- "Sign up" link
- CSRF protection

**Form:**
```html
<form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
```

### `auth/register.html`

**Purpose:** User registration page with birth data.

**Features:**
- Username, email, password inputs
- Birth date picker
- Birth time picker
- Birth location input
- Latitude/longitude (auto-filled)
- Timezone (auto-detected)
- Password validation

**Form:**
```html
<form method="post" action="{% url 'register' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Account</button>
</form>
```

---

## Dashboard Templates

### `dashboard/index.html`

**Purpose:** Main dashboard with charts and data.

**Features:**
- G-Code score display
- 5 interactive charts:
  - Trend chart
  - Planetary positions
  - Element distribution
  - Weekly forecast
  - Aspects network
- Quick stats
- Recent activity
- Auto-refresh toggle

**Chart Containers:**
```html
<div class="chart-container">
    <canvas id="gcode-trend-chart"></canvas>
</div>
<div class="chart-container">
    <canvas id="planetary-chart"></canvas>
</div>
<!-- ... more charts -->
```

**JavaScript Includes:**
```html
<script src="{% static 'js/components/charts/chart-utils.js' %}"></script>
<script src="{% static 'js/components/charts/trend-chart.js' %}"></script>
<script src="{% static 'js/components/charts/planetary-chart.js' %}"></script>
<script src="{% static 'js/components/charts/chart-manager.js' %}"></script>
```

---

## Natal Templates

### `natal/index.html`

**Purpose:** Display natal chart data.

**Features:**
- Sun, Moon, Ascendant display
- All 10 planetary positions
- House cusps
- Dominant elements
- Key aspects
- Calculate/Recalculate button

### `natal/wheel.html`

**Purpose:** Interactive D3.js natal wheel.

**Features:**
- D3.js circular wheel
- Planet glyphs
- House divisions
- Aspect lines
- Zoom and pan
- Export to PNG/SVG

**Container:**
```html
<div id="natal-wheel-container"></div>
```

**JavaScript:**
```html
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="{% static 'js/components/wheel/d3-wheel-renderer.js' %}"></script>
```

---

## Content Templates

### `content/index.html`

**Purpose:** Generate AI content for social media.

**Features:**
- Platform selector (Twitter, Instagram, LinkedIn)
- Content type selector
- Date picker
- Generate button
- Preview area
- Edit content
- Copy to clipboard
- Post/Schedule buttons

**Form:**
```html
<form id="content-form">
    <select name="platform">
        <option value="twitter">Twitter</option>
        <option value="instagram">Instagram</option>
        <option value="linkedin">LinkedIn</option>
    </select>
    <input type="date" name="date">
    <button type="submit">Generate</button>
</form>
```

---

## Settings Templates

### `settings/index.html`

**Purpose:** User settings and preferences.

**Features:**
- Profile settings
- Birth data edit
- Notification preferences
- Email subscription
- Daily G-Code enable/disable
- Preferred tone selection
- Account deletion

---

## Template Inheritance

### Extending Base Template

All templates extend `base.html`:

```html
{% extends 'base.html' %}

{% block title %}Dashboard - Spiritual G-Code{% endblock %}

{% block content %}
    <h1>Welcome to the Dashboard</h1>
    {% csrf_token %}
{% endblock %}

{% block extra_css %}
    <style>
        /* Custom CSS */
    </style>
{% endblock %}

{% block extra_js %}
    <script>
        // Custom JavaScript
    </script>
{% endblock %}
```

---

## Template Filters and Tags

### Custom Filters

#### `format_date`
Formats date to readable string.

```html
{{ transit_date|format_date }}
<!-- Output: Jan 15, 2026 -->
```

#### `format_intensity`
Formats intensity level with color.

```html
{{ intensity_level|format_intensity }}
<!-- Output: <span class="text-gcode-red">High</span> -->
```

---

## Static Files Reference

### CSS

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

### JavaScript

```html
<script src="{% static 'js/main.js' %}"></script>
```

### Images

```html
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

---

## Context Processors

### Available Context

All templates have access to:

```python
{
    'user': request.user,           # Current user
    'debug': settings.DEBUG,        # Debug mode
    'request': request,             # HTTP request
}
```

---

## CSRF Protection

All POST forms must include CSRF token:

```html
<form method="post">
    {% csrf_token %}
    <!-- Form fields -->
</form>
```

---

## Responsive Design

Templates use Tailwind CSS responsive utilities:

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Responsive grid: 1 col on mobile, 2 on tablet, 3 on desktop -->
</div>
```

---

## Related Documentation

- [Frontend JavaScript](../static/js/README_Frontend_JS.md) - JavaScript components
- [Django Core](../core/README_Django_Core.md) - Django configuration

---

**Last Updated:** 2026-01-15
