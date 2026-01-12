/**
 * Weekly Forecast Chart Component
 * Displays 7-day forecast with G-Code scores and themes
 */

class WeeklyForecastChart {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    async loadChartData() {
        try {
            const response = await fetch('/api/dashboard/charts/?type=weekly_forecast');
            if (!response.ok) throw new Error('Failed to fetch chart data');
            const data = await response.json();
            return data.weekly_forecast || [];
        } catch (error) {
            console.error('Error loading chart data:', error);
            return this.getMockData();
        }
    }

    getMockData() {
        // Mock forecast data
        const today = new Date();
        const data = [];
        for (let i = 1; i <= 7; i++) {
            const date = new Date(today);
            date.setDate(date.getDate() + i);
            data.push({
                date: date.toISOString().split('T')[0],
                score: Math.floor(Math.random() * 60) + 40,
                intensity: 'medium',
                themes: ['#Growth', '#Alignment', '#Transformation']
            });
        }
        return data;
    }

    render(data) {
        if (!this.canvas) {
            console.error('Canvas element not found');
            return;
        }

        const ctx = this.canvas.getContext('2d');
        const labels = data.map(d => {
            const date = new Date(d.date);
            return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
        });
        const scores = data.map(d => d.score);

        // Create gradient
        const gradient = window.GcodeChartUtils.createGradient(
            ctx,
            'rgb(88, 166, 255)'  // Accent color for forecast
        );

        // Destroy existing chart if any
        if (this.chart) {
            this.chart.destroy();
        }

        // Create chart
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Forecast G-Code Score',
                    data: scores,
                    borderColor: window.GcodeChartUtils.GCODE_COLORS.accent,
                    backgroundColor: gradient,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointHoverRadius: 9,
                    pointBackgroundColor: window.GcodeChartUtils.GCODE_COLORS.accent,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointStyle: 'star',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: window.GcodeChartUtils.GCODE_COLORS.text,
                            font: {
                                family: "'JetBrains Mono', monospace",
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: window.GcodeChartUtils.GCODE_COLORS.card,
                        titleColor: window.GcodeChartUtils.GCODE_COLORS.accent,
                        bodyColor: window.GcodeChartUtils.GCODE_COLORS.text,
                        borderColor: window.GcodeChartUtils.GCODE_COLORS.accent,
                        borderWidth: 1,
                        padding: 12,
                        callbacks: {
                            afterBody: function(context) {
                                const dataIndex = context[0].dataIndex;
                                const themes = data[dataIndex].themes || [];
                                if (themes.length > 0) {
                                    return '\nThemes: ' + themes.join(', ');
                                }
                                return '';
                            },
                            label: function(context) {
                                const score = context.parsed.y;
                                const intensity = score >= 75 ? 'Intense' :
                                                   score >= 50 ? 'High' :
                                                   score >= 25 ? 'Medium' : 'Low';
                                return `Forecast: ${score}/100 (${intensity})`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: window.GcodeChartUtils.GCODE_COLORS.border,
                            drawBorder: false,
                        },
                        ticks: {
                            color: window.GcodeChartUtils.GCODE_COLORS.textDim,
                            font: {
                                family: "'JetBrains Mono', monospace",
                                size: 11
                            }
                        }
                    },
                    y: {
                        min: 0,
                        max: 100,
                        grid: {
                            color: window.GcodeChartUtils.GCODE_COLORS.border,
                            drawBorder: false,
                        },
                        ticks: {
                            color: window.GcodeChartUtils.GCODE_COLORS.textDim,
                            font: {
                                family: "'JetBrains Mono', monospace",
                                size: 11
                            },
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    async init() {
        const data = await this.loadChartData();
        this.render(data);
    }
}

// Export for global use
window.WeeklyForecastChart = WeeklyForecastChart;
