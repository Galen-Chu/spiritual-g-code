# WebSocket Client Documentation

## Overview

The WebSocket client provides real-time dashboard updates by maintaining a persistent connection with the Django Channels backend.

**Component:**
- `dashboard-client.js` - WebSocket client with auto-reconnect

---

## Features

- **Auto-connect** on page load
- **Auto-reconnect** with exponential backoff
- **User-specific** channel subscription
- **Real-time updates** for new data
- **Ping/pong** keep-alive mechanism
- **Graceful** connection close

---

## DashboardWebSocketClient Class

### Constructor

```javascript
const client = new DashboardWebSocketClient(options);
```

**Options:**
```javascript
{
    url: 'ws://localhost:8000/ws/dashboard/',  // WebSocket URL
    autoConnect: true,                          // Auto-connect on init
    reconnectInterval: 1000,                    // Initial reconnect delay (ms)
    maxReconnectAttempts: 10,                   // Max reconnect attempts
    pingInterval: 30000                         // Ping interval (ms)
}
```

---

## Methods

### `connect()`
Establishes WebSocket connection.

**Usage:**
```javascript
client.connect();
```

### `disconnect()`
Closes WebSocket connection gracefully.

**Usage:**
```javascript
client.disconnect();
```

### `isConnected()`
Checks if WebSocket is connected.

**Returns:** Boolean

### `send(data)`
Sends data to server.

**Parameters:**
- `data` (object) - Data to send (will be JSON stringified)

**Usage:**
```javascript
client.send({ action: 'ping' });
```

---

## Events

The client emits these events (can be listened to):

### `connected`
Fired when WebSocket connection established.

```javascript
client.addEventListener('connected', () => {
    console.log('WebSocket connected');
    showToast('Real-time updates enabled', 'success');
});
```

### `disconnected`
Fired when WebSocket connection closed.

```javascript
client.addEventListener('disconnected', () => {
    console.log('WebSocket disconnected');
    showToast('Connection lost', 'warning');
});
```

### `message`
Fired when message received from server.

**Event Data:**
```javascript
{
    type: 'gcode_updated',
    data: { ... }
}
```

```javascript
client.addEventListener('message', (event) => {
    console.log('Message received:', event.data);
    if (event.data.type === 'gcode_updated') {
        // Refresh dashboard
        refreshDashboard();
    }
});
```

### `error`
Fired when WebSocket error occurs.

```javascript
client.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
    showToast('Connection error', 'error');
});
```

---

## Message Types

### Server → Client Messages

#### `gcode_updated`
New daily G-Code calculated.

```javascript
{
    type: 'gcode_updated',
    data: {
        date: '2026-01-15',
        g_code_score: 78,
        intensity: 'high',
        themes: ['creativity', 'transformation']
    }
}
```

#### `annotation_added`
New annotation created.

```javascript
{
    type: 'annotation_added',
    data: {
        id: 123,
        date: '2026-01-15',
        note: 'My annotation'
    }
}
```

#### `content_generated`
New content generated.

```javascript
{
    type: 'content_generated',
    data: {
        id: 456,
        platform: 'twitter',
        status: 'draft'
    }
}
```

### Client → Server Messages

#### `ping`
Keep-alive ping.

```javascript
{ action: 'ping' }
```

#### `subscribe`
Subscribe to user-specific channel.

```javascript
{
    action: 'subscribe',
    channel: 'user_123'
}
```

---

## Usage Example

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize WebSocket client
    const wsClient = new DashboardWebSocketClient({
        url: 'ws://localhost:8000/ws/dashboard/',
        autoConnect: true
    });

    // Listen for events
    wsClient.addEventListener('connected', () => {
        console.log('WebSocket connected');
    });

    wsClient.addEventListener('message', (event) => {
        switch(event.data.type) {
            case 'gcode_updated':
                // Refresh dashboard data
                loadDashboardData();
                showToast('New G-Code available!', 'info');
                break;
            case 'annotation_added':
                // Add annotation to UI
                addAnnotationToUI(event.data.data);
                break;
            case 'content_generated':
                // Update content list
                updateContentList();
                break;
        }
    });

    wsClient.addEventListener('disconnected', () => {
        showToast('Real-time updates disabled', 'warning');
    });

    wsClient.addEventListener('error', (error) => {
        console.error('WebSocket error:', error);
    });

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        wsClient.disconnect();
    });
});
```

---

## Auto-Reconnect Logic

The client automatically reconnects using exponential backoff:

1. **Initial Delay:** 1 second
2. **Max Delay:** 30 seconds
3. **Max Attempts:** 10 (configurable)

**Reconnect Flow:**
```
Connection Lost → Wait 1s → Try Reconnect
              ↓ (failed)
              Wait 2s → Try Reconnect
              ↓ (failed)
              Wait 4s → Try Reconnect
              ...
              ↓ (after 10 attempts)
              Give Up
```

---

## Browser Compatibility

**Supported:**
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

**Required:**
- WebSocket API
- ES6+ (Promises, arrow functions, classes)

---

## Troubleshooting

### Connection Fails

**Check:**
1. WebSocket server is running
2. Correct WebSocket URL (ws:// or wss://)
3. No firewall blocking WebSocket connection
4. User is authenticated

### No Messages Received

**Check:**
1. Server is sending messages
2. Correct event listeners attached
3. No JavaScript errors in console

### Frequent Disconnections

**Solutions:**
1. Check internet connection stability
2. Increase ping interval
3. Adjust reconnect settings

---

## Related Documentation

- [Frontend JavaScript](../README_Frontend_JS.md) - Overall JS architecture
- [Django Core](../../../../core/README_Django_Core.md) - WebSocket configuration
- [API Application](../../../../api/README_API_Application.md) - WebSocket consumer

---

**Last Updated:** 2026-01-15
