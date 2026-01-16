# Static Assets Documentation

## Overview

The `static/` directory contains all static assets for the Spiritual G-Code platform, including CSS, JavaScript, images, and fonts.

**Organization:**
- `css/` - Custom stylesheets
- `js/` - JavaScript files (documented separately)
- `images/` - Images and icons
- `fonts/` - Custom fonts (if any)

---

## Directory Structure

```
static/
├── css/
│   └── annotations.css      # Annotation system styles
├── js/
│   ├── main.js              # Core utilities
│   └── components/          # JavaScript components
└── images/                  # Logos, icons, etc.
```

---

## CSS Stylesheets

### `css/annotations.css`

Custom styles for the annotation system.

**Features:**
- Annotation tooltip styles
- Modal styles
- Highlight styles
- Context menu styles

**Key Classes:**

#### Annotation Tooltip
```css
.annotation-tooltip {
    position: absolute;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 12px;
    color: #c9d1d9;
    font-size: 14px;
    z-index: 1000;
}
```

#### Annotation Highlight
```css
.annotation-highlight {
    background: rgba(0, 255, 65, 0.1);
    border: 1px solid #00FF41;
    border-radius: 4px;
}
```

#### Annotation Modal
```css
.annotation-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
}
```

---

## Terminal Theme Colors

### CSS Variables

The application uses CSS custom properties for theme colors:

```css
:root {
    /* Background Colors */
    --gcode-bg: #0D1117;
    --gcode-dark: #010409;
    --gcode-card: #161b22;

    /* Accent Colors */
    --gcode-green: #00FF41;
    --gcode-accent: #58A6FF;
    --gcode-purple: #A371F7;

    /* Status Colors */
    --gcode-red: #FF5A5F;
    --gcode-yellow: #F4D03F;

    /* Border and Text */
    --gcode-border: #30363d;
    --gcode-text: #c9d1d9;
    --gcode-text-dim: #8b949e;
}
```

### Usage in CSS

```css
.button {
    background: var(--gcode-green);
    color: var(--gcode-dark);
    border: 1px solid var(--gcode-green);
}

.card {
    background: var(--gcode-card);
    border: 1px solid var(--gcode-border);
}
```

---

## Tailwind CSS Configuration

### CDN Configuration

Tailwind is loaded via CDN with custom configuration:

```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    gcode: {
                        bg: '#0D1117',
                        dark: '#010409',
                        card: '#161b22',
                        green: '#00FF41',
                        accent: '#58A6FF',
                        purple: '#A371F7',
                        red: '#FF5A5F',
                        yellow: '#F4D03F',
                        border: '#30363d',
                    }
                },
                fontFamily: {
                    mono: ['"JetBrains Mono"', 'monospace'],
                }
            }
        }
    }
</script>
```

### Custom Classes

```html
<!-- Button -->
<button class="bg-gcode-green hover:bg-gcode-green-dim text-gcode-dark font-mono py-2 px-4 rounded">
    Calculate G-Code
</button>

<!-- Card -->
<div class="bg-gcode-card border border-gcode-border rounded-lg p-6">
    <h2 class="text-gcode-text font-mono">Dashboard</h2>
</div>
```

---

## Images

### Logo

**Location:** `static/images/logo.png`

**Usage:**
```html
<img src="{% static 'images/logo.png' %}" alt="Spiritual G-Code Logo">
```

### Icons

The application uses Lucide Icons (via CDN):

```html
<script src="https://unpkg.com/lucide@latest"></script>
<script>
    lucide.createIcons();
</script>
```

**Usage:**
```html
<i data-lucide="home"></i>
<i data-lucide="user"></i>
<i data-lucide="settings"></i>
```

---

## Fonts

### Google Fonts

**Font:** JetBrains Mono (monospace)

**Usage:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**CSS:**
```css
body {
    font-family: 'JetBrains Mono', monospace;
}

.code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
}
```

---

## Static Files Management

### Development

In development, Django serves static files automatically:

```python
# core/settings/base.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Production

In production, use WhiteNoise or collect static files:

```python
# core/settings/production.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Collect Static Files:**
```bash
python manage.py collectstatic
```

---

## Loading Static Files

### In Templates

```html
{% load static %}

<!-- CSS -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- JavaScript -->
<script src="{% static 'js/main.js' %}"></script>

<!-- Images -->
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

### In JavaScript

```javascript
// Get static file URL
const staticUrl = '{% static "" %}';
const logoUrl = staticUrl + 'images/logo.png';

// Or use data attributes
<img src="{{ logo_url }}" data-static-path="{% static 'images/logo.png' %}">
```

---

## Optimizing Static Assets

### CSS Minification

Use a tool like `cssmin` or online minifier:

```bash
pip install cssmin
cssmin static/css/style.css > static/css/style.min.css
```

### JavaScript Minification

Use `terser` or `uglify-js`:

```bash
npm install -g terser
terser static/js/main.js -o static/js/main.min.js
```

### Image Optimization

Use tools like `optipng` and `jpegoptim`:

```bash
# Optimize PNG
optipng static/images/logo.png

# Optimize JPEG
jpegoptim static/images/photo.jpg
```

---

## Browser Caching

### Cache Control

Configure cache headers in production:

```python
# core/settings/production.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```

**Nginx Configuration:**
```nginx
location /static/ {
    alias /path/to/staticfiles/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## CDN Options

For production, consider using a CDN:

### AWS CloudFront

```html
<!-- Use CDN URL in production -->
{% if production %}
    <link href="https://cdn.example.com/css/style.css" rel="stylesheet">
{% else %}
    {% load static %}
    <link href="{% static 'css/style.css' %}" rel="stylesheet">
{% endif %}
```

### Cloudflare

Automatically caches static files with proper headers.

---

## Related Documentation

- [Frontend JavaScript](js/README_Frontend_JS.md) - JavaScript components
- [Templates](../templates/README_Templates.md) - HTML templates
- [Django Core](../core/README_Django_Core.md) - Django settings

---

**Last Updated:** 2026-01-15
