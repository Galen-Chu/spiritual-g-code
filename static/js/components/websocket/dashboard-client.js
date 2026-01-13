/**
 * Dashboard WebSocket Client
 * Manages WebSocket connection for real-time dashboard updates
 */

class DashboardWebSocketClient {
    constructor(options = {}) {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
        this.reconnectDelay = options.reconnectDelay || 3000;
        this.isConnected = false;
        this.listeners = {};
        this.url = options.url || null;

        // Connection status callback
        this.onConnectionChange = options.onConnectionChange || null;
    }

    /**
     * Connect to WebSocket server
     * @param {string} url - WebSocket URL (optional, uses default if not provided)
     */
    connect(url) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            console.warn('WebSocket already connected');
            return;
        }

        this.url = url || this.url;

        if (!this.url) {
            // Auto-detect WebSocket URL from current location
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const host = window.location.host;
            this.url = `${protocol}//${host}/ws/dashboard/`;
        }

        console.log(`Connecting to WebSocket: ${this.url}`);

        try {
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => this._handleOpen();
            this.ws.onmessage = (event) => this._handleMessage(event);
            this.ws.onerror = (error) => this._handleError(error);
            this.ws.onclose = () => this._handleClose();

        } catch (error) {
            console.error('WebSocket connection error:', error);
            this._reconnect();
        }
    }

    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        if (this.ws) {
            this.reconnectAttempts = this.maxReconnectAttempts; // Prevent auto-reconnect
            this.ws.close();
            this.ws = null;
        }
    }

    /**
     * Send message to WebSocket server
     * @param {object} data - Data to send (will be JSON stringified)
     */
    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket not connected. Message not sent:', data);
        }
    }

    /**
     * Subscribe to WebSocket events
     * @param {string} eventType - Type of event to listen for
     * @param {function} callback - Callback function when event occurs
     */
    on(eventType, callback) {
        if (!this.listeners[eventType]) {
            this.listeners[eventType] = [];
        }
        this.listeners[eventType].push(callback);
    }

    /**
     * Unsubscribe from WebSocket events
     * @param {string} eventType - Type of event to stop listening for
     * @param {function} callback - Callback function to remove
     */
    off(eventType, callback) {
        if (this.listeners[eventType]) {
            this.listeners[eventType] = this.listeners[eventType].filter(cb => cb !== callback);
        }
    }

    /**
     * Handle WebSocket open event
     * @private
     */
    _handleOpen() {
        console.log('✓ WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;

        // Notify listeners
        this._emit('connected', { timestamp: new Date() });

        // Notify connection status callback
        if (this.onConnectionChange) {
            this.onConnectionChange(true);
        }

        // Send ping to verify connection
        this.send({ type: 'ping' });
    }

    /**
     * Handle WebSocket message event
     * @private
     */
    _handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            console.log('WebSocket message received:', data);

            // Notify listeners based on message type
            this._emit(data.type, data);

        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    }

    /**
     * Handle WebSocket error event
     * @private
     */
    _handleError(error) {
        console.error('WebSocket error:', error);
        this._emit('error', { error });
    }

    /**
     * Handle WebSocket close event
     * @private
     */
    _handleClose() {
        console.log('WebSocket disconnected');
        this.isConnected = false;
        this.ws = null;

        // Notify listeners
        this._emit('disconnected', { timestamp: new Date() });

        // Notify connection status callback
        if (this.onConnectionChange) {
            this.onConnectionChange(false);
        }

        // Attempt to reconnect
        this._reconnect();
    }

    /**
     * Attempt to reconnect to WebSocket server
     * @private
     */
    _reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * this.reconnectAttempts;

            console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

            setTimeout(() => {
                this.connect();
            }, delay);

        } else {
            console.error('Max reconnection attempts reached. WebSocket not connected.');
            this._emit('reconnect_failed', { attempts: this.reconnectAttempts });
        }
    }

    /**
     * Emit event to all registered listeners
     * @private
     */
    _emit(eventType, data) {
        if (this.listeners[eventType]) {
            this.listeners[eventType].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in WebSocket event listener for ${eventType}:`, error);
                }
            });
        }
    }
}

/**
 * Global WebSocket client instance
 * Initialized on dashboard load
 */
window.dashboardWebSocket = null;

/**
 * Initialize WebSocket connection for dashboard
 * @returns {DashboardWebSocketClient} WebSocket client instance
 */
function initDashboardWebSocket() {
    // Check if user is authenticated
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        console.warn('No access token found. WebSocket not initialized.');
        return null;
    }

    // Create WebSocket client
    const wsClient = new DashboardWebSocketClient({
        maxReconnectAttempts: 5,
        reconnectDelay: 3000,
        onConnectionChange: (isConnected) => {
            updateConnectionStatus(isConnected);
        }
    });

    // Register event listeners
    wsClient.on('connected', (data) => {
        console.log('Dashboard WebSocket connected:', data);
    });

    wsClient.on('disconnected', (data) => {
        console.log('Dashboard WebSocket disconnected:', data);
    });

    wsClient.on('connection_established', (data) => {
        console.log('Dashboard connection confirmed:', data);
    });

    wsClient.on('gcode_update', (data) => {
        console.log('G-Code update received:', data);
        handleGCodeUpdate(data);
    });

    // Connect to WebSocket
    wsClient.connect();

    // Store globally
    window.dashboardWebSocket = wsClient;

    return wsClient;
}

/**
 * Update connection status indicator in UI
 * @param {boolean} isConnected - Whether WebSocket is connected
 */
function updateConnectionStatus(isConnected) {
    const statusIndicator = document.getElementById('ws-status-indicator');

    if (!statusIndicator) {
        return;
    }

    if (isConnected) {
        statusIndicator.className = 'ws-status ws-connected';
        statusIndicator.title = 'WebSocket connected - Real-time updates active';
    } else {
        statusIndicator.className = 'ws-status ws-disconnected';
        statusIndicator.title = 'WebSocket disconnected - Using polling fallback';
    }
}

/**
 * Handle G-Code update from WebSocket
 * @param {object} data - G-Code update data
 */
function handleGCodeUpdate(data) {
    // Update dashboard without full refresh
    if (window.chartManager && window.chartManager.charts) {
        // Refresh trend chart to show new data
        window.chartManager.refreshChart('trend');
    }

    // Update today's G-Code section
    // (This would trigger a partial update of the dashboard)
    if (data.update_score) {
        updateTodayGCodeScore(data.g_code_score);
    }
}

/**
 * Update today's G-Code score (helper function)
 * @param {number} score - New G-Code score
 */
function updateTodayGCodeScore(score) {
    const scoreElement = document.getElementById('score-circle');

    if (scoreElement) {
        const scoreValue = scoreElement.querySelector('.score-value');
        if (scoreValue) {
            scoreValue.textContent = score;

            // Update color based on score
            scoreElement.classList.remove('intensity-low', 'intensity-medium', 'intensity-high', 'intensity-intense');

            let intensityClass = 'intensity-low';
            if (score >= 80) intensityClass = 'intensity-intense';
            else if (score >= 60) intensityClass = 'intensity-high';
            else if (score >= 40) intensityClass = 'intensity-medium';

            scoreElement.classList.add(intensityClass);
        }
    }
}

// Export for global use
window.DashboardWebSocketClient = DashboardWebSocketClient;
window.initDashboardWebSocket = initDashboardWebSocket;
