/**
 * Dashboard Charts Manager
 * Initializes and manages all dashboard charts
 */

class DashboardChartsManager {
    constructor() {
        this.charts = {};
        this.isInitialized = false;
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

    destroyAll() {
        // Destroy all charts
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
}

// Export for global use
window.DashboardChartsManager = DashboardChartsManager;
