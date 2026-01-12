/**
 * Element Distribution Bar Chart Component
 * Displays distribution of Fire, Earth, Air, Water elements in natal chart
 */

class ElementDistributionChart {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    async loadChartData() {
        try {
            const response = await fetch('/api/dashboard/charts/?type=element_distribution');
            if (!response.ok) throw new Error('Failed to fetch chart data');
            const data = await response.json();
            return data.element_distribution || [];
        } catch (error) {
            console.error('Error loading chart data:', error);
            return this.getMockData();
        }
    }

    getMockData() {
        // Mock element distribution data
        return [
            { element: 'Fire', count: 3, color: '#FF6B6B' },
            { element: 'Earth', count: 2, color: '#4ECDC4' },
            { element: 'Air', count: 3, color: '#95E1D3' },
            { element: 'Water', count: 2, color: '#45B7D1' },
        ];
    }

    render(data) {
        if (!this.canvas) {
            console.error('Canvas element not found');
            return;
        }

        const ctx = this.canvas.getContext('2d');

        // Destroy existing chart if any
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = data.map(d => d.element);
        const values = data.map(d => d.count);
        const backgroundColors = data.map(d => d.color);

        // Calculate total for percentage
        const total = values.reduce((sum, val) => sum + val, 0);
        const maxVal = Math.max(...values) + 1;

        // Create chart
        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Planets',
                    data: values,
                    backgroundColor: backgroundColors.map(color =>
                        color.replace(')', ', 0.7)').replace('rgb', 'rgba')
                    ),
                    borderColor: backgroundColors,
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
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
                                const value = context.parsed.x;
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${value} planets (${percentage}%)`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: maxVal,
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
                            stepSize: 1
                        },
                        title: {
                            display: true,
                            text: 'Planet Count',
                            color: window.GcodeChartUtils.GCODE_COLORS.textDim,
                            font: {
                                family: "'JetBrains Mono', monospace",
                                size: 12
                            }
                        }
                    },
                    y: {
                        grid: {
                            display: false,
                            drawBorder: false,
                        },
                        ticks: {
                            color: window.GcodeChartUtils.GCODE_COLORS.text,
                            font: {
                                family: "'JetBrains Mono', monospace",
                                size: 13,
                                weight: 'bold'
                            }
                        }
                    }
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
window.ElementDistributionChart = ElementDistributionChart;
