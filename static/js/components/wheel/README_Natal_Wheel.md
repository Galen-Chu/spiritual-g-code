# Natal Wheel Documentation

## Overview

The natal wheel is an interactive D3.js-powered visualization of a user's astrological birth chart, displaying planets, houses, and aspects in a circular zodiac format.

**Component:**
- `d3-wheel-renderer.js` - D3.js circular wheel renderer

---

## Features

- **Interactive** wheel with drag/zoom
- **Planetary** positions with glyphs
- **House** cusps and boundaries
- **Aspect** lines between planets
- **Zodiac** signs with colors
- **Responsive** to window size
- **Export** to PNG/SVG

---

## D3WheelRenderer Class

### Constructor

```javascript
const renderer = new D3WheelRenderer(containerId, options);
```

**Parameters:**
- `containerId` (string) - DOM element ID for the wheel
- `options` (object) - Configuration options

**Options:**
```javascript
{
    width: 800,
    height: 800,
    innerRadius: 100,
    outerRadius: 350,
    zoomEnabled: true,
    animationDuration: 1000
}
```

---

## Methods

### `render(data)`
Renders the natal wheel with provided data.

**Data Structure:**
```javascript
{
    planets: [
        {
            name: 'Sun',
            sign: 'Leo',
            degree: 135.5,
            house: 5,
            color: '#F4D03F'
        },
        // ... all 10 planets
    ],
    houses: [
        {
            number: 1,
            cusp: 215.5,
            sign: 'Scorpio'
        },
        // ... all 12 houses
    ],
    aspects: [
        {
            from: 'sun',
            to: 'moon',
            type: 'trine',
            degree: 120,
            color: '#00FF41'
        },
        // ... all aspects
    ],
    ascendant: {
        sign: 'Scorpio',
        degree: 215.5
    }
}
```

### `update(newData)`
Updates the wheel with new data.

**Usage:**
```javascript
renderer.update(newNatalData);
```

### `export(format)`
Exports the wheel to image format.

**Parameters:**
- `format` (string) - 'png' or 'svg'

**Usage:**
```javascript
renderer.export('png');
renderer.export('svg');
```

### `destroy()`
Removes the wheel and cleans up D3 elements.

**Usage:**
```javascript
renderer.destroy();
```

---

## Visual Structure

### Layers (bottom to top)

1. **Background Circle** - Dark background
2. **Zodiac Ring** - 12 signs with colors
3. **House Divisions** - 12 house cusps
4. **Aspect Lines** - Lines connecting planets
5. **Planets** - Planet glyphs and symbols
6. **Labels** - Sign and planet labels
7. **Overlay** - Hover effects and tooltips

---

## Zodiac Colors

Each zodiac sign has a unique color:

```javascript
const ZODIAC_COLORS = {
    aries: '#FF6B6B',      // Fire Red
    taurus: '#4ECDC4',     // Earth Teal
    gemini: '#95E1D3',     // Air Light Blue
    cancer: '#45B7D1',     // Water Blue
    leo: '#F4D03F',        // Fire Yellow
    virgo: '#52B788',      // Earth Green
    libra: '#A8DADC',      // Air Pale Blue
    scorpio: '#8B0000',    // Water Dark Red
    sagittarius: '#FFA500', // Fire Orange
    capricorn: '#6B7280',  // Earth Gray
    aquarius: '#40E0D0',   // Air Cyan
    pisces: '#9370DB'      // Water Purple
};
```

---

## Aspect Line Styles

Different aspect types have different line styles:

```javascript
const ASPECT_STYLES = {
    conjunction: {   // 0°
        strokeDasharray: '0',
        strokeWidth: 3,
        color: '#FF6B6B'
    },
    opposition: {    // 180°
        strokeDasharray: '5,5',
        strokeWidth: 2,
        color: '#FF5A5F'
    },
    trine: {         // 120°
        strokeDasharray: '0',
        strokeWidth: 2,
        color: '#00FF41'
    },
    square: {        // 90°
        strokeDasharray: '0',
        strokeWidth: 2,
        color: '#F4D03F'
    },
    sextile: {       // 60°
        strokeDasharray: '3,3',
        strokeWidth: 1.5,
        color: '#58A6FF'
    }
};
```

---

## Usage Example

```javascript
document.addEventListener('DOMContentLoaded', async function() {
    // Initialize renderer
    const renderer = new D3WheelRenderer('natal-wheel-container', {
        width: 800,
        height: 800,
        zoomEnabled: true
    });

    // Fetch natal wheel data
    const wheelData = await apiRequest('/api/natal/wheel/');

    // Render wheel
    renderer.render(wheelData);

    // Export button
    document.getElementById('export-wheel-btn').addEventListener('click', () => {
        renderer.export('png');
    });

    // Update wheel (e.g., from different user)
    document.getElementById('change-user-select').addEventListener('change', async (e) => {
        const userId = e.target.value;
        const newWheelData = await apiRequest(`/api/natal/wheel/?user=${userId}`);
        renderer.update(newWheelData);
    });

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        renderer.destroy();
    });
});
```

---

## Interactions

### Hover

Hovering over a planet displays tooltip with details:
- Planet name
- Sign and degree
- House position
- Any aspects

### Drag

Drag to pan the wheel (if zoom enabled).

### Zoom

Mouse wheel to zoom in/out (if zoom enabled).

---

## Accessibility

### ARIA Labels

The wheel includes ARIA labels for screen readers:

```html
<svg role="img" aria-label="Natal chart wheel showing planetary positions">
    <circle role="img" aria-label="Sun in Leo at 15 degrees">
        ...
    </circle>
</svg>
```

### Keyboard Navigation

- Tab to focus wheel
- Arrow keys to pan
- +/- keys to zoom

---

## Performance Considerations

### Optimize Rendering

For large datasets:

1. **Limit Aspects:** Show only major aspects (conjunction, opposition, trine, square, sextile)
2. **Debounce Updates:** Use debounce for resize/zoom events
3. **Simplify Paths:** Reduce path complexity for aspect lines

### Memory Management

```javascript
// Always destroy when done
window.addEventListener('beforeunload', () => {
    renderer.destroy();
});
```

---

## Browser Compatibility

**Supported:**
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

**Required:**
- D3.js 7.x
- SVG support
- ES6+ (Promises, arrow functions, classes)

---

## Related Documentation

- [Frontend JavaScript](../README_Frontend_JS.md) - Overall JS architecture
- [Chart Components](../charts/README_Chart_Components.md) - Other visualizations
- [API Application](../../../../api/README_API_Application.md) - Data endpoints

---

**Last Updated:** 2026-01-15
