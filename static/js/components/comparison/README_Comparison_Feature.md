# Date Range Comparison Feature Documentation

## Overview

The comparison feature allows users to compare G-Code data across different date ranges side-by-side.

**Components:**
- `chart-comparator.js` - Comparison logic and chart rendering
- `date-range-picker.js` - HTML5 date picker integration

---

## Features

- Select two date ranges for comparison
- Side-by-side chart visualization
- Statistical comparison (average, min, max, trend)
- Export comparison results

---

## Chart Comparator

### ChartComparator Class

Compares chart data between two date ranges.

**Constructor:**
```javascript
const comparator = new ChartComparator();
```

**Methods:**

#### `setRanges(range1, range2)`
Sets the two date ranges to compare.

**Parameters:**
```javascript
{
    start: '2026-01-01',
    end: '2026-01-07'
}
```

#### `fetchData(range)`
Fetches G-Code data for a date range.

**Parameters:**
- `range` (object) - Date range with start/end

**Returns:** Promise with transit data

#### `compare()
Fetches data for both ranges and generates comparison.

**Returns:** Promise with comparison results

#### `renderComparison()`
Renders side-by-side comparison charts.

#### `getStatistics()`
Calculates statistics for both ranges.

**Returns:**
```javascript
{
    range1: {
        average: 72.5,
        min: 65,
        max: 82,
        trend: 'increasing'
    },
    range2: {
        average: 68.3,
        min: 60,
        max: 75,
        trend: 'stable'
    },
    difference: {
        average: -4.2,
        trend: 'range1 higher'
    }
}
```

---

## Date Range Picker

### DateRangePicker Class

HTML5 date input wrapper for selecting date ranges.

**Constructor:**
```javascript
const picker = new DateRangePicker('start-input-id', 'end-input-id');
```

**Methods:**

#### `setRange(start, end)`
Sets the date range programmatically.

#### `getRange()`
Gets the current date range.

**Returns:**
```javascript
{
    start: '2026-01-01',
    end: '2026-01-07'
}
```

#### `validate()`
Validates the selected date range.

**Returns:** Boolean (true if valid)

---

## Usage Example

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize date pickers
    const range1Picker = new DateRangePicker('range1-start', 'range1-end');
    const range2Picker = new DateRangePicker('range2-start', 'range2-end');

    // Initialize comparator
    const comparator = new ChartComparator();

    // Compare button
    document.getElementById('compare-btn').addEventListener('click', async () => {
        const range1 = range1Picker.getRange();
        const range2 = range2Picker.getRange();

        // Validate ranges
        if (!range1Picker.validate() || !range2Picker.validate()) {
            showToast('Invalid date range', 'error');
            return;
        }

        // Set ranges and compare
        comparator.setRanges(range1, range2);
        await comparator.compare();

        // Render results
        comparator.renderComparison();

        // Display statistics
        const stats = comparator.getStatistics();
        console.log('Comparison statistics:', stats);
    });
});
```

---

## UI Requirements

### HTML Structure

```html
<div class="comparison-container">
    <!-- Range 1 -->
    <div class="date-range">
        <h3>Range 1</h3>
        <input type="date" id="range1-start">
        <input type="date" id="range1-end">
    </div>

    <!-- Range 2 -->
    <div class="date-range">
        <h3>Range 2</h3>
        <input type="date" id="range2-start">
        <input type="date" id="range2-end">
    </div>

    <!-- Compare Button -->
    <button id="compare-btn">Compare Ranges</button>

    <!-- Results -->
    <div id="comparison-results">
        <div class="chart-container">
            <canvas id="comparison-chart"></canvas>
        </div>
        <div class="statistics"></div>
    </div>
</div>
```

---

## Related Documentation

- [Chart Components](../charts/README_Chart_Components.md) - Chart rendering
- [Frontend JavaScript](../README_Frontend_JS.md) - Overall JS architecture

---

**Last Updated:** 2026-01-15
