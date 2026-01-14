/**
 * Date Range Picker for Comparison Mode
 * Handles date range selection and comparison toggle
 */

class DateRangePicker {
    constructor() {
        this.isCompareMode = false;
        this.period1 = { start: null, end: null };
        this.period2 = { start: null, end: null };
    }

    /**
     * Initialize date range picker
     */
    init() {
        this.createComparisonControls();
        this.setupEventListeners();
        console.log('✓ Date Range Picker initialized');
    }

    /**
     * Create comparison controls in the DOM
     */
    createComparisonControls() {
        // Find the customization controls section
        const controlsSection = document.querySelector('.card.p-4 .flex.flex-wrap');
        if (!controlsSection) {
            console.warn('Customization controls section not found');
            return;
        }

        // Create comparison toggle section
        const comparisonSection = document.createElement('div');
        comparisonSection.className = 'comparison-controls';
        comparisonSection.innerHTML = `
            <div class="flex items-center gap-3 mb-3">
                <span class="text-sm text-gray-400">📊 Compare Mode:</span>
                <button id="compare-toggle" class="global-action-btn" onclick="window.dateRangePicker.toggleCompareMode()">
                    Enable Comparison
                </button>
            </div>

            <div id="comparison-date-ranges" class="comparison-date-ranges" style="display: none;">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Period 1 -->
                    <div class="period-inputs">
                        <h4 class="text-sm font-semibold text-white mb-2">Period 1</h4>
                        <div class="flex items-center gap-2 mb-2">
                            <label class="text-xs text-gray-400">Start:</label>
                            <input type="date" id="period1-start" class="comparison-date-input"
                                onchange="window.dateRangePicker.updatePeriod1()">
                        </div>
                        <div class="flex items-center gap-2">
                            <label class="text-xs text-gray-400">End:</label>
                            <input type="date" id="period1-end" class="comparison-date-input"
                                onchange="window.dateRangePicker.updatePeriod1()">
                        </div>
                    </div>

                    <!-- Period 2 -->
                    <div class="period-inputs">
                        <h4 class="text-sm font-semibold text-white mb-2">Period 2</h4>
                        <div class="flex items-center gap-2 mb-2">
                            <label class="text-xs text-gray-400">Start:</label>
                            <input type="date" id="period2-start" class="comparison-date-input"
                                onchange="window.dateRangePicker.updatePeriod2()">
                        </div>
                        <div class="flex items-center gap-2">
                            <label class="text-xs text-gray-400">End:</label>
                            <input type="date" id="period2-end" class="comparison-date-input"
                                onchange="window.dateRangePicker.updatePeriod2()">
                        </div>
                    </div>
                </div>

                <div class="comparison-actions mt-3">
                    <button class="global-action-btn" onclick="window.dateRangePicker.applyComparison()">
                        Apply Comparison
                    </button>
                    <button class="global-action-btn" onclick="window.dateRangePicker.resetComparison()">
                        Reset
                    </button>
                </div>
            </div>
        `;

        // Insert after the existing customization controls
        controlsSection.parentNode.insertBefore(comparisonSection, controlsSection.nextSibling);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Listen for custom date range changes
        const dateRangeStart = document.getElementById('date-range-start');
        const dateRangeEnd = document.getElementById('date-range-end');

        if (dateRangeStart) {
            dateRangeStart.addEventListener('change', () => {
                this.syncWithSingleRange();
            });
        }

        if (dateRangeEnd) {
            dateRangeEnd.addEventListener('change', () => {
                this.syncWithSingleRange();
            });
        }
    }

    /**
     * Toggle comparison mode
     */
    toggleCompareMode() {
        this.isCompareMode = !this.isCompareMode;

        const toggleBtn = document.getElementById('compare-toggle');
        const dateRangesSection = document.getElementById('comparison-date-ranges');

        if (this.isCompareMode) {
            // Enable comparison mode
            toggleBtn.textContent = 'Disable Comparison';
            toggleBtn.style.background = 'rgba(0, 255, 65, 0.25)';
            toggleBtn.style.borderColor = '#00FF41';
            dateRangesSection.style.display = 'block';

            // Set default date ranges (last 7 days vs previous 7 days)
            this.setDefaultRanges();

            console.log('✓ Comparison mode enabled');
        } else {
            // Disable comparison mode
            toggleBtn.textContent = 'Enable Comparison';
            toggleBtn.style.background = '';
            toggleBtn.style.borderColor = '';
            dateRangesSection.style.display = 'none';

            // Reset comparison
            this.resetComparison();

            console.log('✓ Comparison mode disabled');
        }
    }

    /**
     * Set default date ranges for comparison
     */
    setDefaultRanges() {
        const today = new Date();
        const sevenDaysAgo = new Date(today);
        sevenDaysAgo.setDate(today.getDate() - 7);

        const fourteenDaysAgo = new Date(sevenDaysAgo);
        fourteenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

        // Period 1: Previous 7 days
        this.period1 = {
            start: this.formatDate(fourteenDaysAgo),
            end: this.formatDate(sevenDaysAgo)
        };

        // Period 2: Recent 7 days
        this.period2 = {
            start: this.formatDate(sevenDaysAgo),
            end: this.formatDate(today)
        };

        // Update inputs
        document.getElementById('period1-start').value = this.period1.start;
        document.getElementById('period1-end').value = this.period1.end;
        document.getElementById('period2-start').value = this.period2.start;
        document.getElementById('period2-end').value = this.period2.end;
    }

    /**
     * Update period 1 from inputs
     */
    updatePeriod1() {
        this.period1.start = document.getElementById('period1-start').value;
        this.period1.end = document.getElementById('period1-end').value;
        console.log('Period 1 updated:', this.period1);
    }

    /**
     * Update period 2 from inputs
     */
    updatePeriod2() {
        this.period2.start = document.getElementById('period2-start').value;
        this.period2.end = document.getElementById('period2-end').value;
        console.log('Period 2 updated:', this.period2);
    }

    /**
     * Apply comparison with current date ranges
     */
    async applyComparison() {
        // Validate inputs
        if (!this.period1.start || !this.period1.end) {
            alert('Please select both start and end dates for Period 1');
            return;
        }

        if (!this.period2.start || !this.period2.end) {
            alert('Please select both start and end dates for Period 2');
            return;
        }

        // Validate date ranges
        if (this.period1.start > this.period1.end) {
            alert('Period 1: Start date must be before end date');
            return;
        }

        if (this.period2.start > this.period2.end) {
            alert('Period 2: Start date must be before end date');
            return;
        }

        console.log('Applying comparison...');
        console.log('Period 1:', this.period1);
        console.log('Period 2:', this.period2);

        // Enable comparison via chart comparator
        if (window.chartComparator) {
            await window.chartComparator.enableComparison(this.period1, this.period2);
            console.log('✓ Comparison applied successfully');
        } else {
            console.error('Chart comparator not found');
            alert('Chart comparator not available');
        }
    }

    /**
     * Reset comparison mode
     */
    resetComparison() {
        if (window.chartComparator) {
            window.chartComparator.disableComparison();
        }

        this.period1 = { start: null, end: null };
        this.period2 = { start: null, end: null };

        // Clear inputs
        document.getElementById('period1-start').value = '';
        document.getElementById('period1-end').value = '';
        document.getElementById('period2-start').value = '';
        document.getElementById('period2-end').value = '';

        console.log('✓ Comparison reset');
    }

    /**
     * Sync with single date range picker
     */
    syncWithSingleRange() {
        // If single date range is selected, use it as period 2
        const singleStart = document.getElementById('date-range-start')?.value;
        const singleEnd = document.getElementById('date-range-end')?.value;

        if (singleStart && singleEnd && this.isCompareMode) {
            document.getElementById('period2-start').value = singleStart;
            document.getElementById('period2-end').value = singleEnd;
            this.updatePeriod2();
        }
    }

    /**
     * Format date as YYYY-MM-DD
     * @param {Date} date
     * @returns {string}
     */
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    /**
     * Get current date ranges
     * @returns {object} { period1, period2 }
     */
    getDateRanges() {
        return {
            period1: { ...this.period1 },
            period2: { ...this.period2 }
        };
    }

    /**
     * Check if in compare mode
     * @returns {boolean}
     */
    isInCompareMode() {
        return this.isCompareMode;
    }
}

/**
 * Global date range picker instance
 */
window.dateRangePicker = new DateRangePicker();

// Export for global use
window.DateRangePicker = DateRangePicker;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.dateRangePicker.init();
    });
} else {
    window.dateRangePicker.init();
}
