/**
 * Chart Export Utilities
 * Provides functions to export charts as PNG/SVG
 */

class ChartExportUtils {
    /**
     * Export Chart.js canvas as PNG
     * @param {string} canvasId - Canvas element ID
     * @param {string} filename - Download filename
     */
    static exportChartAsPNG(canvasId, filename) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            console.error(`Canvas ${canvasId} not found`);
            return false;
        }

        try {
            // Create a temporary link
            const link = document.createElement('a');
            link.download = filename || `${canvasId}-${new Date().toISOString().split('T')[0]}.png`;

            // Convert canvas to blob
            canvas.toBlob((blob) => {
                const url = URL.createObjectURL(blob);
                link.href = url;
                link.click();
                URL.revokeObjectURL(url);
                console.log(`✓ Exported ${canvasId} as PNG`);
            }, 'image/png');

            return true;
        } catch (error) {
            console.error('Error exporting canvas:', error);
            return false;
        }
    }

    /**
     * Export Chart.js chart as SVG (requires canvas-to-svg conversion)
     * @param {Object} chart - Chart.js instance
     * @param {string} filename - Download filename
     */
    static exportChartAsSVG(chart, filename) {
        if (!chart || !chart.canvas) {
            console.error('Chart instance not valid');
            return false;
        }

        try {
            const canvas = chart.canvas;

            // Basic SVG export using canvas data
            const svgData = this._canvasToSVG(canvas);

            // Create blob and download
            const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.download = filename || `chart-${Date.now()}.svg`;
            link.href = url;
            link.click();
            URL.revokeObjectURL(url);

            console.log('✓ Exported chart as SVG');
            return true;
        } catch (error) {
            console.error('Error exporting as SVG:', error);
            return false;
        }
    }

    /**
     * Export Cytoscape.js network as PNG
     * @param {Object} cy - Cytoscape instance
     * @param {string} filename - Download filename
     */
    static exportCytoscapeAsPNG(cy, filename) {
        if (!cy) {
            console.error('Cytoscape instance not found');
            return false;
        }

        try {
            // Use Cytoscape's built-in PNG export
            const png = cy.png({ full: true, scale: 2 });

            const link = document.createElement('a');
            link.download = filename || `network-${Date.now()}.png`;
            link.href = png;
            link.click();

            console.log('✓ Exported Cytoscape as PNG');
            return true;
        } catch (error) {
            console.error('Error exporting Cytoscape:', error);
            return false;
        }
    }

    /**
     * Export Cytoscape.js network as SVG
     * @param {Object} cy - Cytoscape instance
     * @param {string} filename - Download filename
     */
    static exportCytoscapeAsSVG(cy, filename) {
        if (!cy) {
            console.error('Cytoscape instance not found');
            return false;
        }

        try {
            // Use Cytoscape's built-in SVG export
            const svg = cy.svg({ full: true, scale: 1 });

            const blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.download = filename || `network-${Date.now()}.svg`;
            link.href = url;
            link.click();
            URL.revokeObjectURL(url);

            console.log('✓ Exported Cytoscape as SVG');
            return true;
        } catch (error) {
            console.error('Error exporting Cytoscape SVG:', error);
            return false;
        }
    }

    /**
     * Export all dashboard charts
     * @param {Object} chartManager - DashboardChartsManager instance
     * @param {string} format - Export format ('png' or 'svg')
     */
    static exportAllCharts(chartManager, format = 'png') {
        if (!chartManager || !chartManager.charts) {
            console.error('Chart manager not found');
            return;
        }

        const timestamp = new Date().toISOString().split('T')[0];
        let successCount = 0;

        // Export Chart.js charts
        ['trend', 'planetary', 'element', 'forecast'].forEach(chartName => {
            const chart = chartManager.charts[chartName];
            if (chart && chart.chart) {
                if (format === 'svg') {
                    this.exportChartAsSVG(chart.chart, `${chartName}-${timestamp}.svg`);
                } else {
                    this.exportChartAsPNG(`${chartName}-chart`, `${chartName}-${timestamp}.png`);
                }
                successCount++;
            }
        });

        // Export Cytoscape chart
        const network = chartManager.charts.network;
        if (network && network.cy) {
            if (format === 'svg') {
                this.exportCytoscapeAsSVG(network.cy, `aspects-network-${timestamp}.svg`);
            } else {
                this.exportCytoscapeAsPNG(network.cy, `aspects-network-${timestamp}.png`);
            }
            successCount++;
        }

        console.log(`✓ Exported ${successCount} charts as ${format.toUpperCase()}`);
    }

    /**
     * Convert canvas to basic SVG (helper method)
     * @private
     */
    static _canvasToSVG(canvas) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Get image data
        const imageData = ctx.getImageData(0, 0, width, height);
        const dataURL = canvas.toDataURL('image/png');

        // Create basic SVG structure
        return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <image width="${width}" height="${height}" xlink:href="${dataURL}" />
</svg>`;
    }

    /**
     * Create export button HTML
     * @param {string} type - Button type ('chart' or 'network')
     * @param {string} chartId - Chart identifier
     * @param {string} label - Button label
     */
    static createExportButton(type, chartId, label = 'Export') {
        const btn = document.createElement('button');
        btn.className = 'export-btn';
        btn.innerHTML = `
            <span class="export-icon">📥</span>
            <span class="export-text">${label}</span>
        `;
        btn.setAttribute('data-export-type', type);
        btn.setAttribute('data-chart-id', chartId);

        // Add styles
        Object.assign(btn.style, {
            padding: '6px 12px',
            backgroundColor: 'rgba(0, 255, 65, 0.1)',
            border: '1px solid rgba(0, 255, 65, 0.3)',
            borderRadius: '4px',
            color: '#00FF41',
            cursor: 'pointer',
            fontSize: '12px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            transition: 'all 0.2s'
        });

        // Hover effect
        btn.addEventListener('mouseenter', () => {
            btn.style.backgroundColor = 'rgba(0, 255, 65, 0.2)';
            btn.style.borderColor = '#00FF41';
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.backgroundColor = 'rgba(0, 255, 65, 0.1)';
            btn.style.borderColor = 'rgba(0, 255, 65, 0.3)';
        });

        return btn;
    }
}

// Export for global use
window.ChartExportUtils = ChartExportUtils;
