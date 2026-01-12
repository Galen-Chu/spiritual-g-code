/**
 * G-Code 7-Day Trend Chart Component
 * Displays G-Code intensity scores over the last 7 days
 */

class GCodeTrendChart {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    async loadChartData() {
        try {
            const response = await fetch('/api/dashboard/charts/?type=gcode_trend_7d');
            if (!response.ok) throw new Error('Failed to fetch chart data');
            const data = await response.json();
            return data.gcode_trend_7d || [];
        } catch (error) {
            console.error('Error loading chart data:', error);
            return this.getMockData();
        }
    }

    getMockData() {
        // Mock data for testing
        const today = new Date();
        const data = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            data.push({
                date: date.toISOString().split('T')[0],
                score: Math.floor(Math.random() * 60) + 40,
                intensity: 'medium'
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
        const labels = data.map(d => window.GcodeChartUtils.formatDate(d.date));
        const scores = data.map(d => d.score);

        // Create gradient
        const gradient = window.GcodeChartUtils.createGradient(
            ctx,
            'rgb(0, 255, 65)'
        );

        // Destroy existing chart if any
        if (this.chart) {
            this.chart.destroy();
        }

        // Create new chart
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'G-Code Intensity Score',
                    data: scores,
                    borderColor: window.GcodeChartUtils.GCODE_COLORS.green,
                    backgroundColor: gradient,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    pointBackgroundColor: scores.map(score =>
                        window.GcodeChartUtils.getIntensityColor(score)
                    ),
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
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
                        titleColor: window.GcodeChartUtils.GCODE_COLORS.green,
                        bodyColor: window.GcodeChartUtils.GCODE_COLORS.text,
                        borderColor: window.GcodeChartUtils.GCODE_COLORS.green,
                        borderWidth: 1,
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                const score = context.parsed.y;
                                const intensity = score >= 75 ? 'Intense' :
                                                   score >= 50 ? 'High' :
                                                   score >= 25 ? 'Medium' : 'Low';
                                return `Score: ${score}/100 (${intensity})`;
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
                        },
                        title: {
                            display: true,
                            text: 'Intensity Score',
                            color: window.GcodeChartUtils.GCODE_COLORS.textDim,
                            font: {
                                family: "'JetBrains Mono', monospace",
                                size: 12
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
window.GCodeTrendChart = GCodeTrendChart;
