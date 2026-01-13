/**
 * Dashboard Charts Manager
 * Initializes and manages all dashboard charts
 */

class DashboardChartsManager {
    constructor() {
        this.charts = {};
        this.isInitialized = false;
        this.autoRefreshInterval = null;
        this.autoRefreshEnabled = false;
    }

    async initAll() {
        if (this.isInitialized) {
            console.warn('Charts already initialized');
            return;
        }

        console.log('Initializing dashboard charts...');

        // Initialize G-Code Trend Chart
        const trendCanvas = document.getElementById('gcode-trend-chart');
        if (trendCanvas) {
            this.charts.trend = new window.GCodeTrendChart('gcode-trend-chart');
            await this.charts.trend.init();
            console.log('✓ G-Code Trend Chart initialized');
        }

        // Initialize Planetary Positions Chart
        const planetaryCanvas = document.getElementById('planetary-chart');
        if (planetaryCanvas) {
            this.charts.planetary = new window.PlanetaryPositionsChart('planetary-chart');
            await this.charts.planetary.init();
            console.log('✓ Planetary Positions Chart initialized');
        }

        // Initialize Element Distribution Chart
        const elementCanvas = document.getElementById('element-chart');
        if (elementCanvas) {
            this.charts.element = new window.ElementDistributionChart('element-chart');
            await this.charts.element.init();
            console.log('✓ Element Distribution Chart initialized');
        }

        // Initialize Weekly Forecast Chart
        const forecastCanvas = document.getElementById('forecast-chart');
        if (forecastCanvas) {
            this.charts.forecast = new window.WeeklyForecastChart('forecast-chart');
            await this.charts.forecast.init();
            console.log('✓ Weekly Forecast Chart initialized');
        }

        // Initialize Aspects Network Chart
        const networkContainer = document.getElementById('aspects-network-chart');
        if (networkContainer) {
            this.charts.network = new window.AspectsNetworkChart('aspects-network-chart');
            await this.charts.network.init();
            console.log('✓ Aspects Network Chart initialized');
        }

        this.isInitialized = true;
        console.log('All dashboard charts initialized successfully!');
    }

    refreshAll() {
        // Refresh all charts
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.init) {
                chart.init();
            }
        });
    }

    refreshChart(chartName) {
        if (this.charts[chartName] && this.charts[chartName].init) {
            this.charts[chartName].init();
        }
    }

    exportNetwork(format) {
        const network = this.charts.network;
        if (!network || !network.cy) {
            console.error('Network chart not found');
            return false;
        }

        const timestamp = new Date().toISOString().split('T')[0];

        try {
            if (format === 'svg') {
                window.ChartExportUtils.exportCytoscapeAsSVG(network.cy, `aspects-network-${timestamp}.svg`);
            } else {
                window.ChartExportUtils.exportCytoscapeAsPNG(network.cy, `aspects-network-${timestamp}.png`);
            }
            return true;
        } catch (error) {
            console.error('Error exporting network chart:', error);
            return false;
        }
    }

    destroyAll() {
        // Destroy all charts
        this.stopAutoRefresh();
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.cy) {
                // Cytoscape instance
                chart.cy.destroy();
            } else if (chart && chart.chart) {
                // Chart.js instance
                chart.chart.destroy();
            }
        });
        this.charts = {};
        this.isInitialized = false;
    }

    /**
     * Enable auto-refresh with configurable interval
     * @param {number} intervalMinutes - Refresh interval in minutes (default: 5)
     */
    startAutoRefresh(intervalMinutes = 5) {
        if (this.autoRefreshEnabled) {
            console.warn('Auto-refresh is already enabled');
            return;
        }

        const intervalMs = intervalMinutes * 60 * 1000;
        this.autoRefreshEnabled = true;

        this.autoRefreshInterval = setInterval(() => {
            console.log(`Auto-refreshing charts (${new Date().toLocaleTimeString()})`);
            this.refreshAll();
        }, intervalMs);

        console.log(`✓ Auto-refresh enabled: ${intervalMinutes} minutes`);
    }

    /**
     * Disable auto-refresh
     */
    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
            this.autoRefreshEnabled = false;
            console.log('✓ Auto-refresh disabled');
        }
    }

    /**
     * Toggle auto-refresh on/off
     * @param {number} intervalMinutes - Refresh interval in minutes
     */
    toggleAutoRefresh(intervalMinutes = 5) {
        if (this.autoRefreshEnabled) {
            this.stopAutoRefresh();
        } else {
            this.startAutoRefresh(intervalMinutes);
        }
        return this.autoRefreshEnabled;
    }

    /**
     * Set auto-refresh interval
     * @param {number} intervalMinutes - New interval in minutes
     */
    setAutoRefreshInterval(intervalMinutes) {
        const wasEnabled = this.autoRefreshEnabled;
        this.stopAutoRefresh();
        if (wasEnabled) {
            this.startAutoRefresh(intervalMinutes);
        }
    }
}

// Export for global use
window.DashboardChartsManager = DashboardChartsManager;
