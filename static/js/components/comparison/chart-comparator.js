/**
 * Chart Comparator
 * Handles side-by-side comparison of two date ranges
 */

class ChartComparator {
    constructor() {
        this.isCompareMode = false;
        this.period1 = { start: null, end: null };
        this.period2 = { start: null, end: null };
        this.originalChartData = null;
        this.comparisonCharts = {
            trend: { chart1: null, chart2: null },
            forecast: { chart1: null, chart2: null }
        };
    }

    /**
     * Enable comparison mode
     * @param {object} period1 - First period { start, end }
     * @param {object} period2 - Second period { start, end }
     */
    enableComparison(period1, period2) {
        this.isCompareMode = true;
        this.period1 = period1;
        this.period2 = period2;

        console.log('Comparison mode enabled');
        console.log('Period 1:', period1);
        console.log('Period 2:', period2);

        this.renderComparisonCharts();
        this.renderStatisticsPanel();
    }

    /**
     * Disable comparison mode (return to single chart view)
     */
    disableComparison() {
        this.isCompareMode = false;
        this.period1 = { start: null, end: null };
        this.period2 = { start: null, end: null };

        console.log('Comparison mode disabled');

        // Remove comparison containers
        this.removeComparisonCharts();
        this.removeStatisticsPanel();

        // Refresh original charts
        if (window.chartManager) {
            window.chartManager.refreshAll();
        }
    }

    /**
     * Render side-by-side comparison charts
     */
    async renderComparisonCharts() {
        // Store original chart data
        this.storeOriginalChartData();

        // Create comparison containers for each chart
        await this.createComparisonContainer('trend', 'G-Code Trend Comparison');
        await this.createComparisonContainer('forecast', 'Weekly Forecast Comparison');
    }

    /**
     * Create comparison container for a specific chart
     * @param {string} chartType - Type of chart (trend, forecast)
     * @param {string} title - Chart title
     */
    async createComparisonContainer(chartType, title) {
        // Find original chart container
        const originalChartId = `chart-${chartType}`;
        const originalContainer = document.getElementById(originalChartId);

        if (!originalContainer) {
            console.warn(`Chart container not found: ${originalChartId}`);
            return;
        }

        // Hide original chart
        originalContainer.style.display = 'none';

        // Create comparison wrapper
        const comparisonWrapper = document.createElement('div');
        comparisonWrapper.id = `comparison-${chartType}`;
        comparisonWrapper.className = 'comparison-wrapper';

        // Create header
        const header = document.createElement('div');
        header.className = 'comparison-header';
        header.innerHTML = `
            <h3>${title}</h3>
            <div class="comparison-periods">
                <div class="period-label">
                    <strong>Period 1:</strong>
                    <span class="period-date">${this.period1.start} to ${this.period1.end}</span>
                </div>
                <div class="period-label">
                    <strong>Period 2:</strong>
                    <span class="period-date">${this.period2.start} to ${this.period2.end}</span>
                </div>
            </div>
        `;

        // Create charts container
        const chartsContainer = document.createElement('div');
        chartsContainer.className = 'comparison-charts';

        // Create period 1 chart container
        const period1Container = document.createElement('div');
        period1Container.className = 'comparison-chart';
        period1Container.innerHTML = `
            <div class="comparison-chart-title">Period 1</div>
            <canvas id="comparison-${chartType}-period1"></canvas>
        `;

        // Create period 2 chart container
        const period2Container = document.createElement('div');
        period2Container.className = 'comparison-chart';
        period2Container.innerHTML = `
            <div class="comparison-chart-title">Period 2</div>
            <canvas id="comparison-${chartType}-period2"></canvas>
        `;

        chartsContainer.appendChild(period1Container);
        chartsContainer.appendChild(period2Container);

        comparisonWrapper.appendChild(header);
        comparisonWrapper.appendChild(chartsContainer);

        // Insert after original container
        originalContainer.parentNode.insertBefore(comparisonWrapper, originalContainer.nextSibling);

        // Fetch and render chart data for both periods
        await this.renderComparisonChart(chartType, 'period1', this.period1);
        await this.renderComparisonChart(chartType, 'period2', this.period2);
    }

    /**
     * Render a single comparison chart
     * @param {string} chartType - Type of chart
     * @param {string} period - 'period1' or 'period2'
     * @param {object} dateRange - { start, end }
     */
    async renderComparisonChart(chartType, period, dateRange) {
        const canvasId = `comparison-${chartType}-${period}`;
        const canvas = document.getElementById(canvasId);

        if (!canvas) {
            console.error(`Canvas not found: ${canvasId}`);
            return;
        }

        // Build chart type identifier
        const chartTypeMap = {
            'trend': 'gcode_trend_7d',
            'forecast': 'weekly_forecast'
        };

        const type = chartTypeMap[chartType];

        // Fetch data for specific date range
        const apiUrl = `/api/dashboard/charts/?type=${type}&start_date=${dateRange.start}&end_date=${dateRange.end}`;

        try {
            const response = await fetch(apiUrl);
            const data = await response.json();

            // Get chart configuration based on type
            let chartConfig;
            if (chartType === 'trend') {
                chartConfig = this.getTrendChartConfig(data, `Period ${period === 'period1' ? '1' : '2'}`);
            } else if (chartType === 'forecast') {
                chartConfig = this.getForecastChartConfig(data, `Period ${period === 'period1' ? '1' : '2'}`);
            }

            // Create chart
            const ctx = canvas.getContext('2d');
            const chart = new Chart(ctx, chartConfig);

            // Store chart reference
            this.comparisonCharts[chartType][period] = chart;

        } catch (error) {
            console.error(`Error rendering ${canvasId}:`, error);
            // Show error message
            canvas.parentNode.innerHTML = `
                <div class="comparison-chart-title">Period ${period === 'period1' ? '1' : '2'}</div>
                <div class="chart-error">Failed to load chart data</div>
            `;
        }
    }

    /**
     * Get trend chart configuration for comparison
     * @param {object} data - Chart data
     * @param {string} label - Dataset label
     * @returns {object} Chart.js configuration
     */
    getTrendChartConfig(data, label) {
        const chartData = data.gcode_trend_7d || [];

        return {
            type: 'line',
            data: {
                labels: chartData.map(d => d.date),
                datasets: [{
                    label: label,
                    data: chartData.map(d => d.score),
                    borderColor: '#00FF41',
                    backgroundColor: 'rgba(0, 255, 65, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 16 / 9,
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: '#E6EDF3',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#8B949E' },
                        grid: { color: '#21262d' }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { color: '#8B949E' },
                        grid: { color: '#21262d' }
                    }
                }
            }
        };
    }

    /**
     * Get forecast chart configuration for comparison
     * @param {object} data - Chart data
     * @param {string} label - Dataset label
     * @returns {object} Chart.js configuration
     */
    getForecastChartConfig(data, label) {
        const chartData = data.weekly_forecast || [];

        return {
            type: 'line',
            data: {
                labels: chartData.map(d => {
                    const date = new Date(d.date);
                    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
                }),
                datasets: [{
                    label: label,
                    data: chartData.map(d => d.score),
                    borderColor: '#58A6FF',
                    backgroundColor: 'rgba(88, 166, 255, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointStyle: 'star',
                    pointRadius: 8,
                    pointHoverRadius: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                aspectRatio: 16 / 9,
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: '#E6EDF3',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            afterLabel: function(context) {
                                const dataPoint = chartData[context.dataIndex];
                                return dataPoint.themes ? dataPoint.themes.join(', ') : '';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#8B949E' },
                        grid: { color: '#21262d' }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { color: '#8B949E' },
                        grid: { color: '#21262d' }
                    }
                }
            }
        };
    }

    /**
     * Render statistics panel
     */
    renderStatisticsPanel() {
        // Calculate statistics for both periods
        const stats1 = this.calculateStatistics(this.period1);
        const stats2 = this.calculateStatistics(this.period2);

        // Create statistics panel HTML
        const statsPanel = document.createElement('div');
        statsPanel.id = 'comparison-statistics';
        statsPanel.className = 'comparison-statistics card';
        statsPanel.innerHTML = `
            <h3>📊 Comparison Statistics</h3>
            <div class="statistics-grid">
                <div class="stat-group">
                    <h4>Period 1</h4>
                    <p class="stat-label">Date Range:</p>
                    <p class="stat-value">${this.period1.start} to ${this.period1.end}</p>
                    <p class="stat-label">Average Score:</p>
                    <p class="stat-value ${this.getScoreClass(stats1.avg)}">${stats1.avg.toFixed(1)}</p>
                    <p class="stat-label">Min Score:</p>
                    <p class="stat-value">${stats1.min}</p>
                    <p class="stat-label">Max Score:</p>
                    <p class="stat-value">${stats1.max}</p>
                </div>
                <div class="stat-divider"></div>
                <div class="stat-group">
                    <h4>Period 2</h4>
                    <p class="stat-label">Date Range:</p>
                    <p class="stat-value">${this.period2.start} to ${this.period2.end}</p>
                    <p class="stat-label">Average Score:</p>
                    <p class="stat-value ${this.getScoreClass(stats2.avg)}">${stats2.avg.toFixed(1)}</p>
                    <p class="stat-label">Min Score:</p>
                    <p class="stat-value">${stats2.min}</p>
                    <p class="stat-label">Max Score:</p>
                    <p class="stat-value">${stats2.max}</p>
                </div>
                <div class="stat-divider"></div>
                <div class="stat-group stat-diff">
                    <h4>Difference</h4>
                    <p class="stat-label">Average Change:</p>
                    <p class="stat-value ${this.getDiffClass(stats2.avg - stats1.avg)}">
                        ${stats2.avg > stats1.avg ? '+' : ''}${(stats2.avg - stats1.avg).toFixed(1)}
                    </p>
                    <p class="stat-label">Change %:</p>
                    <p class="stat-value ${this.getDiffClass(stats2.avg - stats1.avg)}">
                        ${stats2.avg > stats1.avg ? '+' : ''}${((stats2.avg - stats1.avg) / stats1.avg * 100).toFixed(1)}%
                    </p>
                </div>
            </div>
        `;

        // Insert before the first chart
        const firstChart = document.getElementById('chart-trend');
        if (firstChart && firstChart.parentNode) {
            firstChart.parentNode.insertBefore(statsPanel, firstChart);
        }
    }

    /**
     * Calculate statistics for a period
     * @param {object} period - { start, end }
     * @returns {object} Statistics { avg, min, max }
     */
    async calculateStatistics(period) {
        // Default values
        const stats = { avg: 0, min: 0, max: 0 };

        try {
            // Fetch trend data for the period
            const apiUrl = `/api/dashboard/charts/?type=gcode_trend_7d&start_date=${period.start}&end_date=${period.end}`;
            const response = await fetch(apiUrl);
            const data = await response.json();
            const chartData = data.gcode_trend_7d || [];

            if (chartData.length > 0) {
                const scores = chartData.map(d => d.score);
                stats.avg = scores.reduce((a, b) => a + b, 0) / scores.length;
                stats.min = Math.min(...scores);
                stats.max = Math.max(...scores);
            }
        } catch (error) {
            console.error('Error calculating statistics:', error);
        }

        return stats;
    }

    /**
     * Get CSS class for score
     * @param {number} score - G-Code score
     * @returns {string} CSS class
     */
    getScoreClass(score) {
        if (score >= 80) return 'text-red-500';
        if (score >= 60) return 'text-yellow-500';
        if (score >= 40) return 'text-gcode-green';
        return 'text-blue-500';
    }

    /**
     * Get CSS class for difference
     * @param {number} diff - Difference value
     * @returns {string} CSS class
     */
    getDiffClass(diff) {
        if (diff > 0) return 'text-gcode-green';
        if (diff < 0) return 'text-red-500';
        return 'text-gray-400';
    }

    /**
     * Store original chart data before comparison
     */
    storeOriginalChartData() {
        // Store reference to original charts if needed
        this.originalChartData = {};

        if (window.chartManager) {
            const trendChart = window.chartManager.getChart('trend');
            const forecastChart = window.chartManager.getChart('forecast');

            if (trendChart && trendChart.chart) {
                this.originalChartData.trend = trendChart.chart.data;
            }
            if (forecastChart && forecastChart.chart) {
                this.originalChartData.forecast = forecastChart.chart.data;
            }
        }
    }

    /**
     * Remove comparison charts and restore originals
     */
    removeComparisonCharts() {
        // Remove comparison containers
        const containers = document.querySelectorAll('.comparison-wrapper');
        containers.forEach(container => container.remove());

        // Show original charts
        document.getElementById('chart-trend').style.display = '';
        document.getElementById('chart-forecast').style.display = '';
    }

    /**
     * Remove statistics panel
     */
    removeStatisticsPanel() {
        const statsPanel = document.getElementById('comparison-statistics');
        if (statsPanel) {
            statsPanel.remove();
        }
    }

    /**
     * Destroy comparison charts
     */
    destroy() {
        // Destroy all comparison charts
        for (const chartType in this.comparisonCharts) {
            for (const period in this.comparisonCharts[chartType]) {
                const chart = this.comparisonCharts[chartType][period];
                if (chart && chart.destroy) {
                    chart.destroy();
                }
            }
        }

        this.comparisonCharts = {
            trend: { chart1: null, chart2: null },
            forecast: { chart1: null, chart2: null }
        };
    }
}

/**
 * Global chart comparator instance
 */
window.chartComparator = new ChartComparator();

// Export for global use
window.ChartComparator = ChartComparator;
