/**
 * Planetary Positions Polar Chart Component
 * Displays 10 planets in their zodiac positions
 */

class PlanetaryPositionsChart {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    async loadChartData() {
        try {
            const response = await fetch('/api/dashboard/charts/?type=planetary_positions');
            if (!response.ok) throw new Error('Failed to fetch chart data');
            const data = await response.json();
            return data.planetary_positions || [];
        } catch (error) {
            console.error('Error loading chart data:', error);
            return this.getMockData();
        }
    }

    getMockData() {
        // Mock planetary data
        const planets = [
            { planet: 'Sun', sign: 'Leo', degree: 120, element: 'fire' },
            { planet: 'Moon', sign: 'Cancer', degree: 90, element: 'water' },
            { planet: 'Mercury', sign: 'Virgo', degree: 150, element: 'earth' },
            { planet: 'Venus', sign: 'Libra', degree: 180, element: 'air' },
            { planet: 'Mars', sign: 'Scorpio', degree: 210, element: 'water' },
            { planet: 'Jupiter', sign: 'Sagittarius', degree: 240, element: 'fire' },
            { planet: 'Saturn', sign: 'Capricorn', degree: 270, element: 'earth' },
            { planet: 'Uranus', sign: 'Aquarius', degree: 300, element: 'air' },
            { planet: 'Neptune', sign: 'Pisces', degree: 330, element: 'water' },
            { planet: 'Pluto', sign: 'Aries', degree: 30, element: 'fire' },
        ];
        return planets;
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

        // Prepare data for polar area chart
        const labels = data.map(d => d.planet);
        const values = data.map(d => d.degree || 0);
        const backgroundColors = data.map(d => {
            const element = d.element || 'air';
            return window.GcodeChartUtils.ELEMENT_COLORS[element] || '#999';
        });

        // Create chart
        this.chart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Planetary Positions',
                    data: values,
                    backgroundColor: backgroundColors.map(color =>
                        color.replace(')', ', 0.6)').replace('rgb', 'rgba')
                    ),
                    borderColor: backgroundColors,
                    borderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'right',
                        labels: {
                            color: window.GcodeChartUtils.GCODE_COLORS.text,
                            font: {
                                family: "'JetBrains Mono', monospace",
                                size: 11
                            },
                            generateLabels: function(chart) {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map((label, i) => {
                                        const planet = data.labels[i];
                                        const sign = data.datasets[0].data[i];
                                        return `${planet} (${sign}°)`;
                                    });
                                }
                                return [];
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
                                const planet = context.label;
                                const data = context.dataset.data;
                                return `${planet}: Position`;
                            }
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 360,
                        grid: {
                            color: window.GcodeChartUtils.GCODE_COLORS.border,
                        },
                        angleLines: {
                            color: window.GcodeChartUtils.GCODE_COLORS.border,
                        },
                        points: {
                            display: false
                        },
                        ticks: {
                            display: false,
                            stepSize: 30
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
window.PlanetaryPositionsChart = PlanetaryPositionsChart;
