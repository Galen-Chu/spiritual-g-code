/**
 * Solar System Transit Manager
 * Manages D3.js solar system visualization with controls
 */

class SolarSystemManager {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.renderer = new SolarSystemRenderer(containerId, options);
        this.isLoading = false;
        this.lastUpdateDate = null;
    }

    async init(targetDate = null) {
        if (this.isLoading) return;

        this.isLoading = true;
        this._showLoading();

        try {
            await this.renderer.loadData(targetDate);
            this.renderer.render();
            this.lastUpdateDate = targetDate;
            this._hideLoading();
            console.log('✓ Solar System visualization initialized');
        } catch (error) {
            console.error('✗ Failed to initialize solar system:', error);
            this._showError('Failed to load solar system data');
        } finally {
            this.isLoading = false;
        }
    }

    async refresh(date = null) {
        await this.init(date || this.lastUpdateDate);
    }

    toggleAsteroids(show) {
        this.renderer.updateOptions({ showAsteroids: show });
    }

    toggleCentaurs(show) {
        this.renderer.updateOptions({ showCentaurs: show });
    }

    toggleOrbits(show) {
        this.renderer.updateOptions({ showOrbits: show });
    }

    toggleLunarNodes(show) {
        this.renderer.toggleLunarNodes(show);
    }

    setLunarNodeDisplay(mode) {
        this.renderer.setLunarNodeDisplay(mode);
    }

    exportAsPNG() {
        this.renderer.exportAsPNG();
    }

    _showLoading() {
        const container = document.getElementById(this.containerId);
        container.innerHTML = `
            <div class="flex flex-col items-center justify-center py-20">
                <div class="w-64 h-2 bg-gcode-border rounded-full overflow-hidden">
                    <div class="loading-bar h-full rounded-full"></div>
                </div>
                <p class="mt-4 text-gcode-green text-sm">Calculating planetary positions...</p>
            </div>
        `;
    }

    _hideLoading() {
        // Loading state is cleared when renderer.render() is called
    }

    _showError(message) {
        const container = document.getElementById(this.containerId);
        container.innerHTML = `
            <div class="flex flex-col items-center justify-center py-20">
                <p class="text-red-500 text-lg mb-4">⚠️ ${message}</p>
                <button onclick="window.solarSystemManager.refresh()"
                        class="global-action-btn">
                    Retry
                </button>
            </div>
        `;
    }
}

// Export for global use
window.SolarSystemManager = SolarSystemManager;
