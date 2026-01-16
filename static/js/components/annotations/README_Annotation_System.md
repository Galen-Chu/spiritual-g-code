# Annotation System Documentation

## Overview

The annotation system allows users to add notes to chart data points. Users can annotate specific dates with their thoughts, observations, and interpretations.

**Components:**
- `annotation-manager.js` - CRUD operations for annotations
- `annotation-ui.js` - Modal, tooltips, and context menu UI

---

## Features

- **Create** annotations on any date/chart
- **Read** all annotations for a user
- **Update** existing annotations
- **Delete** annotations
- **View** annotations as tooltips on hover
- **Filter** annotations by date range

---

## Annotation Manager

### AnnotationManager Class

Manages annotation CRUD operations.

**Constructor:**
```javascript
const manager = new AnnotationManager();
```

**Methods:**

#### `create(annotationData)`
Creates a new annotation.

**Parameters:**
```javascript
{
    chart_type: 'daily',      // daily, natal, transit
    date: '2026-01-15',
    g_code_score: 78,
    intensity: 'high',
    note: 'My observation about this day'
}
```

**Returns:** Promise with created annotation

#### `getAll(filters?)`
Fetches all annotations for current user.

**Parameters:**
- `filters` (optional):
  ```javascript
  {
      chart_type: 'daily',
      date_from: '2026-01-01',
      date_to: '2026-01-31'
  }
  ```

**Returns:** Promise with annotations array

#### `getById(id)`
Fetches a single annotation by ID.

**Parameters:**
- `id` (number) - Annotation ID

**Returns:** Promise with annotation object

#### `update(id, data)`
Updates an existing annotation.

**Parameters:**
- `id` (number) - Annotation ID
- `data` (object) - Updated fields

**Returns:** Promise with updated annotation

#### `delete(id)`
Deletes an annotation.

**Parameters:**
- `id` (number) - Annotation ID

**Returns:** Promise

---

## Annotation UI

### AnnotationUI Class

Manages annotation user interface elements.

**Constructor:**
```javascript
const ui = new AnnotationUI(manager);
```

**Methods:**

#### `showCreateModal(date, score, intensity)`
Displays modal for creating annotation.

**Usage:**
```javascript
ui.showCreateModal('2026-01-15', 78, 'high');
```

#### `showEditModal(annotation)`
Displays modal for editing annotation.

**Usage:**
```javascript
ui.showEditModal(annotationObject);
```

#### `showTooltip(annotation, element)`
Displays tooltip with annotation text.

**Usage:**
```javascript
ui.showTooltip(annotation, document.getElementById('chart-canvas'));
```

#### `hideTooltip()`
Hides the annotation tooltip.

**Usage:**
```javascript
ui.hideTooltip();
```

---

## Usage Example

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize manager and UI
    const manager = new AnnotationManager();
    const ui = new AnnotationUI(manager);

    // Create annotation button
    document.getElementById('add-annotation-btn').addEventListener('click', async () => {
        const date = document.getElementById('date-input').value;
        const score = parseInt(document.getElementById('score-input').value);
        const intensity = document.getElementById('intensity-input').value;

        ui.showCreateModal(date, score, intensity);
    });

    // Load annotations
    manager.getAll().then(annotations => {
        console.log('Loaded annotations:', annotations);
    });
});
```

---

## API Endpoints

The annotation system uses these API endpoints:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/annotations/` | List annotations |
| POST | `/api/annotations/` | Create annotation |
| GET | `/api/annotations/{id}/` | Get annotation |
| PUT | `/api/annotations/{id}/` | Update annotation |
| DELETE | `/api/annotations/{id}/` | Delete annotation |

---

## Related Documentation

- [Frontend JavaScript](../README_Frontend_JS.md) - Overall JS architecture
- [Chart Components](../charts/README_Chart_Components.md) - Chart integration

---

**Last Updated:** 2026-01-15
