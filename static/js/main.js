/**
 * Spiritual G-Code - Main JavaScript
 * Common utilities and helper functions
 */

// API Base URL
const API_BASE_URL = '/api';

// Access Token
let accessToken = localStorage.getItem('access_token');

/**
 * Make authenticated API request
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            // Token expired, try to refresh
            await refreshAccessToken();
            // Retry the request
            return apiRequest(endpoint, options);
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

/**
 * Refresh access token
 */
async function refreshAccessToken() {
    try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (response.ok) {
            const data = await response.json();
            accessToken = data.access;
            localStorage.setItem('access_token', data.access);
        } else {
            // Refresh failed, redirect to login
            window.location.href = '/auth/login/';
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
        window.location.href = '/auth/login/';
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');

    const colors = {
        success: 'bg-gcode-green border-gcode-green text-white',
        error: 'bg-gcode-red border-gcode-red text-white',
        warning: 'bg-gcode-yellow border-gcode-yellow text-white',
        info: 'bg-gcode-accent border-gcode-accent text-white',
    };

    toast.className = `rounded-lg p-4 shadow-lg border ${colors[type] || colors.info}`;
    toast.textContent = message;

    container.appendChild(toast);

    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

/**
 * Format date time
 */
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Loading overlay
 */
function showLoading(message = 'Loading...') {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    overlay.innerHTML = `
        <div class="bg-gcode-card border border-gcode-border rounded-lg p-8 text-center">
            <div class="w-16 h-2 bg-gcode-border rounded-full overflow-hidden mx-auto mb-4">
                <div class="loading-bar h-full rounded-full"></div>
            </div>
            <p class="text-gcode-green">${message}</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

/**
 * Initialize charts
 */
function initializeCharts() {
    // Chart.js global configuration
    Chart.defaults.color = '#c9d1d9';
    Chart.defaults.font.family = '"JetBrains Mono", monospace';
    Chart.defaults.borderColor = '#30363d';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start',
                });
            }
        });
    });
});
