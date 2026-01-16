# Chart Components Documentation

## Overview

The `components/charts/` directory contains Chart.js-based data visualization components for the Spiritual G-Code dashboard. These components render various astrological and statistical charts using the terminal-chic theme.

**Technology Stack:**
- Chart.js 4.4.0
- Cytoscape.js 3.28.1 (network graphs)
- Custom terminal theme colors

---

## Directory Structure

```
charts/
├── chart-utils.js           # Shared utilities and theme colors
├── chart-manager.js         # Centralized initialization (262 lines)
├── trend-chart.js           # G-Code 7-day trend line chart
├── planetary-chart.js       # Polar area chart (10 planets)
├── element-chart.js         # Horizontal bar chart (4 elements)
├── forecast-chart.js        # Weekly forecast line chart
├── aspects-network-chart.js # Cytoscape.js network graph (368 lines)
└── export-utils.js          # Chart export utilities (PNG/SVG)
```

---

## Color System (`chart-utils.js`)

### Terminal Theme Colors

```javascript
const GCODE_COLORS = {
    bg: '#0D1117',           // Main background
    dark: '#010409',         // Dark background
    green: '#00FF41',        // Primary accent (G-Code green)
    greenDim: '#00B82D',     // Dimmed green
    greenTransparent: 'rgba(0, 255, 65, 0.1)',
    accent: '#58A6FF',       // Secondary accent
    purple: '#A371F7',       // Purple accent
    red: '#FF5A5F',          // Error/intense
    yellow: '#F4D03F',       // Warning/high
    border: '#30363d',       // Border color
    card: '#161b22',         // Card background
    text: '#c9d1d9',         // Primary text
    textDim: '#8b949e',      // Secondary text
};
```

### Element Colors

```javascript
const ELEMENT_COLORS = {
    fire: '#FF6B6B',      // Red
    earth: '#4ECDC4',     // Teal
    air: '#95E1D3',       // Light Blue
    water: '#45B7D1',     // Blue
};
```

### Planet Colors

```javascript
const PLANET_COLORS = {
    sun: '#F4D03F',       // Yellow
    moon: '#C0C0C0',      // Silver
    mercury: '#A9A9A9',   // Gray
    venus: '#FFC0CB',     // Pink
    mars: '#FF4500',      // Red-Orange
    jupiter: '#FFA500',   // Orange
    saturn: '#DAA520',    // Golden
    uranus: '#40E0D0',    // Cyan
    neptune: '#4169E1',   // Royal Blue
    pluto: '#8B0000',     // Dark Red
};
```

### Intensity Level Colors

```javascript
function getIntensityColor(score) {
    if (score >= 75) return GCODE_COLORS.red;      // Intense
    if (score >= 50) return GCODE_COLORS.yellow;   // High
    if (score >= 25) return GCODE_COLORS.green;    // Medium
    return GCODE_COLORS.accent;                    // Low
}
```

---

## Default Chart Options

All charts share these default options (configured in `chart-utils.js`):

```javascript
const DEFAULT_CHART_OPTIONS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            labels: {
                color: GCODE_COLORS.text,
                font: { family: "'JetBrains Mono', monospace" }
            }
        },
        tooltip: {
            backgroundColor: GCODE_COLORS.card,
            titleColor: GCODE_COLORS.green,
            bodyColor: GCODE_COLORS.text,
            borderColor: GCODE_COLORS.green,
            borderWidth: 1,
            padding: 12,
            displayColors: true,
        }
    },
    scales: {
        x: {
            grid: { color: GCODE_COLORS.border, drawBorder: false },
            ticks: { color: GCODE_COLORS.textDim }
        },
        y: {
            grid: { color: GCODE_COLORS.border, drawBorder: false },
            ticks: { color: GCODE_COLORS.textDim }
        }
    }
};
```

---

## Chart Components

### 1. G-Code Trend Chart (`trend-chart.js`)

**Purpose:** Displays 7-day G-Code score trend as a line chart.

**Chart Type:** Line chart

**Canvas Element:** `#gcode-trend-chart`

**Data Structure:**
```javascript
{
    labels: ['Jan 9', 'Jan 10', 'Jan 11', 'Jan 12', 'Jan 13', 'Jan 14', 'Jan 15'],
    datasets: [{
        label: 'G-Code Score',
        data: [65, 72, 68, 75, 80, 78, 82],
        borderColor: GCODE_COLORS.green,
        backgroundColor: GCODE_COLORS.greenTransparent,
        tension: 0.4,
        fill: true
    }]
}
```

**Features:**
- Smooth curve (tension: 0.4)
- Filled area under line
- Gradient colors based on intensity
- Interactive tooltips

---

### 2. Planetary Positions Chart (`planetary-chart.js`)

**Purpose:** Displays current planetary positions as a polar area chart.

**Chart Type:** Polar area chart

**Canvas Element:** `#planetary-chart`

**Data Structure:**
```javascript
{
    labels: ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'],
    datasets: [{
        label: 'Planetary Strength',
        data: [85, 72, 65, 90, 45, 78, 55, 60, 40, 35],
        backgroundColor: [
            PLANET_COLORS.sun,
            PLANET_COLORS.moon,
            PLANET_COLORS.mercury,
            // ... all 10 planets
        ]
    }]
}
```

**Features:**
- 10 planets displayed radially
- Planet-specific colors
- Size indicates strength/influence
- Hover tooltips with sign info

---

### 3. Element Distribution Chart (`element-chart.js`)

**Purpose:** Displays dominant element distribution (Fire, Earth, Air, Water).

**Chart Type:** Horizontal bar chart

**Canvas Element:** `#element-chart`

**Data Structure:**
```javascript
{
    labels: ['Fire', 'Earth', 'Air', 'Water'],
    datasets: [{
        label: 'Element Dominance',
        data: [35, 25, 20, 30],
        backgroundColor: [
            ELEMENT_COLORS.fire,
            ELEMENT_COLORS.earth,
            ELEMENT_COLORS.air,
            ELEMENT_COLORS.water,
        ],
        borderWidth: 0
    }]
}
```

**Features:**
- 4 elements (Fire, Earth, Air, Water)
- Horizontal bars for easy comparison
- Element-specific colors
- Percentage display

---

### 4. Weekly Forecast Chart (`forecast-chart.js`)

**Purpose:** Displays 7-day forecast with predicted G-Code scores.

**Chart Type:** Line chart (similar to trend chart)

**Canvas Element:** `#forecast-chart`

**Data Structure:**
```javascript
{
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [{
        label: 'Forecast',
        data: [70, 75, 82, 68, 72, 85, 80],
        borderColor: GCODE_COLORS.accent,
        backgroundColor: 'rgba(88, 166, 255, 0.1)',
        tension: 0.4,
        fill: true,
        borderDash: [5, 5]  // Dashed line for forecast
    }]
}
```

**Features:**
- 7-day forecast
- Dashed line (indicates prediction)
- Confidence shading
- Comparison with actual trend

---

### 5. Aspects Network Chart (`aspects-network-chart.js`)

**Purpose:** Displays planetary aspects as an interactive network graph.

**Library:** Cytoscape.js 3.28.1

**Container Element:** `#aspects-network-chart`

**Data Structure:**
```javascript
{
    nodes: [
        { data: { id: 'sun', label: 'Sun', sign: 'Leo' } },
        { data: { id: 'moon', label: 'Moon', sign: 'Pisces' } },
        { data: { id: 'jupiter', label: 'Jupiter', sign: 'Sagittarius' } },
        // ... more planets
    ],
    edges: [
        { data: { source: 'sun', target: 'moon', label: 'Trine' } },
        { data: { source: 'sun', target: 'jupiter', label: 'Conjunction' } },
        // ... more aspects
    ]
}
```

**Features:**
- Interactive node dragging
- Edge labels (aspect types)
- Node colors by planet
- Zoom and pan
- Export to PNG/SVG

**Visual Styling:**
```javascript
const style = [
    {
        selector: 'node',
        style: {
            'background-color': 'data(color)',
            'label': 'data(label)',
            'width': 30,
            'height': 30,
            'font-size': 12,
            'text-valign': 'center',
            'text-halign': 'center',
            'color': '#fff'
        }
    },
    {
        selector: 'edge',
        style: {
            'width': 2,
            'line-color': '#555',
            'target-arrow-color': '#555',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': 10,
            'text-rotation': 'autorotate',
            'text-margin-y': -10
        }
    }
];
```

---

## Chart Manager (`chart-manager.js`)

### DashboardChartsManager Class

Centralized manager for initializing and controlling all dashboard charts.

**Methods:**

#### `initAll()`
Initializes all dashboard charts.

**Usage:**
```javascript
const manager = new DashboardChartsManager();
await manager.initAll();
```

**Charts Initialized:**
1. G-Code Trend Chart
2. Planetary Positions Chart
3. Element Distribution Chart
4. Weekly Forecast Chart
5. Aspects Network Chart

#### `refreshAll()`
Refreshes all charts with latest data.

**Usage:**
```javascript
manager.refreshAll();
```

#### `refreshChart(chartName)`
Refreshes a specific chart.

**Parameters:**
- `chartName` (string) - Chart identifier (`trend`, `planetary`, `element`, `forecast`, `network`)

**Usage:**
```javascript
manager.refreshChart('trend');
```

#### `exportNetwork(format)`
Exports the aspects network chart.

**Parameters:**
- `format` (string) - Export format (`png` or `svg`)

**Usage:**
```javascript
manager.exportNetwork('png');
manager.exportNetwork('svg');
```

---

## Chart Export Utils (`export-utils.js`)

### Chart Export Functions

#### `exportChartAsPNG(chart, filename)`
Exports Chart.js chart as PNG image.

**Parameters:**
- `chart` (Chart instance) - Chart.js instance
- `filename` (string) - Output filename

**Usage:**
```javascript
ChartExportUtils.exportChartAsPNG(trendChart, 'gcode-trend-2026-01-15.png');
```

#### `exportChartAsSVG(chart, filename)`
Exports Chart.js chart as SVG vector image.

**Parameters:**
- `chart` (Chart instance) - Chart.js instance
- `filename` (string) - Output filename

**Usage:**
```javascript
ChartExportUtils.exportChartAsSVG(trendChart, 'gcode-trend-2026-01-15.svg');
```

#### `exportCytoscapeAsPNG(cy, filename)`
Exports Cytoscape.js network as PNG.

**Parameters:**
- `cy` (Cytoscape instance) - Cytoscape instance
- `filename` (string) - Output filename

**Usage:**
```javascript
ChartExportUtils.exportCytoscapeAsPNG(network.cy, 'aspects-network-2026-01-15.png');
```

#### `exportCytoscapeAsSVG(cy, filename)`
Exports Cytoscape.js network as SVG.

**Parameters:**
- `cy` (Cytoscape instance) - Cytoscape instance
- `filename` (string) - Output filename

**Usage:**
```javascript
ChartExportUtils.exportCytoscapeAsSVG(network.cy, 'aspects-network-2026-01-15.svg');
```

---

## Using Chart Components

### 1. Include Scripts

```html
<script src="{% static 'js/main.js' %}"></script>
<script src="{% static 'js/components/charts/chart-utils.js' %}"></script>
<script src="{% static 'js/components/charts/trend-chart.js' %}"></script>
<script src="{% static 'js/components/charts/chart-manager.js' %}"></script>
```

### 2. Add Canvas Element

```html
<div class="chart-container">
    <canvas id="gcode-trend-chart"></canvas>
</div>
```

### 3. Initialize Chart

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const trendChart = new GCodeTrendChart('gcode-trend-chart');
    trendChart.init();
});
```

### 4. Update Chart Data

```javascript
// Fetch new data
const newData = await apiRequest('/api/dashboard/charts/');

// Update chart
trendChart.update(newData.trend);
```

---

## Chart Component Pattern

All chart components follow this structure:

```javascript
class ChartName {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.options = options;
        this.chart = null;
    }

    async init() {
        // Fetch data
        const data = await this.fetchData();

        // Create chart
        this.chart = new Chart(this.canvas, {
            type: 'line',  // or other type
            data: data,
            options: this.getOptions()
        });
    }

    async fetchData() {
        // API call to fetch data
    }

    getOptions() {
        // Return chart options
    }

    update(newData) {
        // Update chart with new data
        this.chart.data = newData;
        this.chart.update();
    }

    destroy() {
        // Clean up
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

// Export
window.ChartName = ChartName;
```

---

## Responsive Design

Charts automatically resize with container.

**CSS Requirements:**
```css
.chart-container {
    position: relative;
    height: 400px;
    width: 100%;
}

canvas {
    width: 100% !important;
    height: 100% !important;
}
```

---

## Performance Optimization

### Data Limiting

```javascript
// Limit to 30 data points max
const maxPoints = 30;
if (data.labels.length > maxPoints) {
    data.labels = data.labels.slice(-maxPoints);
    data.datasets[0].data = data.datasets[0].data.slice(-maxPoints);
}
```

### Debounce Updates

```javascript
const debouncedUpdate = debounce(() => {
    chart.update();
}, 300);

window.addEventListener('resize', debouncedUpdate);
```

### Destroy Unused Charts

```javascript
// Before re-rendering
if (window.myChart) {
    window.myChart.destroy();
}
window.myChart = new Chart(...);
```

---

## Troubleshooting

### Chart Not Rendering

**Check:**
1. Canvas element exists
2. Chart.js library loaded
3. Data format correct
4. No JavaScript errors in console

### Chart Not Updating

**Solution:**
```javascript
// Call update() method
chart.update();

// Or reinitialize
chart.destroy();
chart.init();
```

### Colors Not Applied

**Check:**
1. `chart-utils.js` loaded
2. Color constants accessible
3. Chart options use color constants

---

## Related Documentation

- [Frontend JavaScript](../README_Frontend_JS.md) - Overall JavaScript architecture
- [Annotation System](../annotations/README_Annotation_System.md) - Chart annotations
- [Comparison Feature](../comparison/README_Comparison_Feature.md) - Chart comparison
- [API Application](../../../../api/README_API_Application.md) - Data endpoints

---

**Last Updated:** 2026-01-15
