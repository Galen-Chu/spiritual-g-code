/**
 * Chart.js Configuration for Spiritual G-Code
 * Provides theme colors and default configurations
 */

// G-Code Terminal Theme Colors
const GCODE_COLORS = {
    bg: '#0D1117',
    dark: '#010409',
    green: '#00FF41',
    greenDim: '#00B82D',
    greenTransparent: 'rgba(0, 255, 65, 0.1)',
    accent: '#58A6FF',
    purple: '#A371F7',
    red: '#FF5A5F',
    yellow: '#F4D03F',
    border: '#30363d',
    card: '#161b22',
    text: '#c9d1d9',
    textDim: '#8b949e',
};

// Element Colors (Fire, Earth, Air, Water)
const ELEMENT_COLORS = {
    fire: '#FF6B6B',      // Red
    earth: '#4ECDC4',     // Teal
    air: '#95E1D3',       // Light Blue
    water: '#45B7D1',     // Blue
};

// Planet Colors
const PLANET_COLORS = {
    sun: '#F4D03F',       // Yellow
    moon: '#C0C0C0',      // Silver
    mercury: '#A9A9A9',   // Gray
    venus: '#FFC0CB',     // Pink
    mars: '#FF4500',      // Red-Orange
    jupiter: '#FFA500',   // Orange
    saturn: '#DAA520',    // Golden
    uranus: '#40E0D0',    // Cyan
    neptune: '#4169E1',   // Royal Blue
    pluto: '#8B0000',     // Dark Red
};

// Default Chart Options
const DEFAULT_CHART_OPTIONS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            labels: {
                color: GCODE_COLORS.text,
                font: {
                    family: "'JetBrains Mono', monospace"
                }
            }
        },
        tooltip: {
            backgroundColor: GCODE_COLORS.card,
            titleColor: GCODE_COLORS.green,
            bodyColor: GCODE_COLORS.text,
            borderColor: GCODE_COLORS.green,
            borderWidth: 1,
            padding: 12,
            displayColors: true,
        }
    },
    scales: {
        x: {
            grid: {
                color: GCODE_COLORS.border,
                drawBorder: false,
            },
            ticks: {
                color: GCODE_COLORS.textDim,
                font: {
                    family: "'JetBrains Mono', monospace"
                }
            }
        },
        y: {
            grid: {
                color: GCODE_COLORS.border,
                drawBorder: false,
            },
            ticks: {
                color: GCODE_COLORS.textDim,
                font: {
                    family: "'JetBrains Mono', monospace"
                }
            }
        }
    }
};

// G-Code Intensity Level Colors
function getIntensityColor(score) {
    if (score >= 75) return GCODE_COLORS.red;      // Intense
    if (score >= 50) return GCODE_COLORS.yellow;   // High
    if (score >= 25) return GCODE_COLORS.green;    // Medium
    return GCODE_COLORS.accent;                   // Low
}

// Format date for display
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = { month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Create gradient for line charts
function createGradient(ctx, color) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color.replace(')', ', 0.3)').replace('rgb', 'rgba'));
    gradient.addColorStop(1, color.replace(')', ', 0.0)').replace('rgb', 'rgba'));
    return gradient;
}

// Export utilities
window.GcodeChartUtils = {
    GCODE_COLORS,
    ELEMENT_COLORS,
    PLANET_COLORS,
    DEFAULT_CHART_OPTIONS,
    getIntensityColor,
    formatDate,
    createGradient,
};
