/**
 * Annotation UI Components
 * Handles visual components for annotations (modals, tooltips, markers)
 */

class AnnotationUI {
    constructor() {
        this.modal = null;
        this.currentChartType = null;
        this.currentDataPoint = null;
        this.modalInitialized = false;
    }

    /**
     * Initialize the annotation modal
     */
    initModal() {
        if (this.modalInitialized) {
            return;
        }

        // Create modal HTML if it doesn't exist
        if (!document.getElementById('annotation-modal')) {
            const modalHTML = `
                <div id="annotation-modal" class="annotation-modal" style="display: none;">
                    <div class="annotation-modal-content">
                        <div class="annotation-modal-header">
                            <h3>Add Annotation</h3>
                            <button class="annotation-modal-close" onclick="window.annotationUI.closeModal()">&times;</button>
                        </div>
                        <div class="annotation-modal-body">
                            <div class="annotation-data-point-info" id="annotation-data-point-info"></div>
                            <textarea
                                id="annotation-note-input"
                                placeholder="Enter your note or insight..."
                                rows="4"
                                maxlength="500"
                            ></textarea>
                            <div class="annotation-char-count">
                                <span id="annotation-char-count">0</span>/500 characters
                            </div>
                        </div>
                        <div class="annotation-modal-footer">
                            <button class="annotation-btn annotation-btn-cancel" onclick="window.annotationUI.closeModal()">
                                Cancel
                            </button>
                            <button class="annotation-btn annotation-btn-save" onclick="window.annotationUI.saveAnnotation()">
                                Save Annotation
                            </button>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHTML);

            // Add character count listener
            const textarea = document.getElementById('annotation-note-input');
            const charCount = document.getElementById('annotation-char-count');
            textarea.addEventListener('input', () => {
                charCount.textContent = textarea.value.length;
            });

            // Close modal on outside click
            document.getElementById('annotation-modal').addEventListener('click', (e) => {
                if (e.target.id === 'annotation-modal') {
                    this.closeModal();
                }
            });

            // Close modal on Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isModalOpen()) {
                    this.closeModal();
                }
            });
        }

        this.modalInitialized = true;
    }

    /**
     * Open annotation modal for a data point
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point object
     * @param {string} existingNote - Existing note (for editing)
     */
    openModal(chartType, dataPoint, existingNote = '') {
        this.initModal();

        this.currentChartType = chartType;
        this.currentDataPoint = dataPoint;

        // Set existing note
        const textarea = document.getElementById('annotation-note-input');
        textarea.value = existingNote;
        document.getElementById('annotation-char-count').textContent = existingNote.length;

        // Display data point info
        const dataPointInfo = this.formatDataPointDisplay(chartType, dataPoint);
        document.getElementById('annotation-data-point-info').textContent = dataPointInfo;

        // Show modal
        document.getElementById('annotation-modal').style.display = 'block';
        textarea.focus();
    }

    /**
     * Close the annotation modal
     */
    closeModal() {
        const modal = document.getElementById('annotation-modal');
        if (modal) {
            modal.style.display = 'none';
        }

        this.currentChartType = null;
        this.currentDataPoint = null;
    }

    /**
     * Check if modal is open
     * @returns {boolean}
     */
    isModalOpen() {
        const modal = document.getElementById('annotation-modal');
        return modal && modal.style.display === 'block';
    }

    /**
     * Save the annotation from modal
     * @returns {Promise<boolean>} Success status
     */
    async saveAnnotation() {
        const textarea = document.getElementById('annotation-note-input');
        const note = textarea.value.trim();

        if (!note) {
            alert('Please enter a note');
            return false;
        }

        const annotationData = {
            chart_type: this.currentChartType,
            data_point: this.currentDataPoint,
            note: note,
        };

        try {
            // Check if annotation already exists
            const existingAnnotation = window.annotationManager.getCachedAnnotation(
                this.currentChartType,
                this.currentDataPoint
            );

            if (existingAnnotation) {
                // Update existing annotation
                await window.annotationManager.updateAnnotation(existingAnnotation.id, { note });
            } else {
                // Create new annotation
                await window.annotationManager.createAnnotation(annotationData);
            }

            this.closeModal();

            // Refresh chart annotations
            this.refreshChartAnnotations(this.currentChartType);

            return true;
        } catch (error) {
            console.error('Error saving annotation:', error);
            alert('Failed to save annotation: ' + error.message);
            return false;
        }
    }

    /**
     * Format data point for display
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point object
     * @returns {string} Formatted string
     */
    formatDataPointDisplay(chartType, dataPoint) {
        switch (chartType) {
            case 'gcode_trend':
                const date = dataPoint.date || dataPoint.x;
                const score = dataPoint.value || dataPoint.y || dataPoint.g_code_score;
                return `Date: ${date}, G-Code Score: ${score}`;

            case 'planetary':
                const planet = dataPoint.planet;
                const sign = dataPoint.sign;
                return `${planet} in ${sign}`;

            case 'element':
                const element = dataPoint.element;
                const value = dataPoint.value;
                return `${element}: ${value}`;

            case 'forecast':
                const fDate = dataPoint.date;
                const fScore = dataPoint.value || dataPoint.score;
                return `Forecast for ${fDate}: ${fScore}`;

            case 'network':
                const p1 = dataPoint.planet1;
                const p2 = dataPoint.planet2;
                return `${p1} aspect ${p2}`;

            default:
                return JSON.stringify(dataPoint);
        }
    }

    /**
     * Add annotation markers to a chart
     * @param {string} chartType - Chart type
     * @param {Array} annotations - List of annotations
     * @param {object} chartInstance - Chart.js instance (optional)
     */
    addAnnotationMarkers(chartType, annotations, chartInstance = null) {
        if (!chartInstance || !annotations.length) {
            return;
        }

        // Get chart canvas
        const canvas = chartInstance.canvas;

        // Add annotation markers as custom plugin or overlay
        // This is a placeholder - actual implementation depends on chart library

        annotations.forEach(annotation => {
            const dataPoint = annotation.data_point;
            this.createAnnotationMarker(canvas, chartType, dataPoint, annotation.note);
        });
    }

    /**
     * Create a visual marker for an annotation
     * @param {HTMLElement} canvas - Chart canvas element
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point
     * @param {string} note - Annotation note
     */
    createAnnotationMarker(canvas, chartType, dataPoint, note) {
        // This is a simplified implementation
        // Full implementation would need to calculate position based on chart scales

        const marker = document.createElement('div');
        marker.className = 'annotation-marker';
        marker.innerHTML = '●'; // Bullet point as marker
        marker.title = note; // Simple tooltip

        // Position would be calculated based on data point coordinates
        // For now, this is a placeholder
        canvas.parentElement.appendChild(marker);
    }

    /**
     * Show annotation tooltip
     * @param {HTMLElement} targetElement - Target element
     * @param {object} annotation - Annotation object
     */
    showTooltip(targetElement, annotation) {
        const existingTooltip = document.getElementById('annotation-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }

        const tooltip = document.createElement('div');
        tooltip.id = 'annotation-tooltip';
        tooltip.className = 'annotation-tooltip';
        tooltip.innerHTML = `
            <div class="annotation-tooltip-header">
                <strong>${annotation.chart_type_display}</strong>
                <button onclick="this.parentElement.parentElement.remove()">&times;</button>
            </div>
            <div class="annotation-tooltip-body">
                <p>${this.escapeHtml(annotation.note)}</p>
                <small class="annotation-tooltip-date">
                    ${new Date(annotation.created_at).toLocaleDateString()}
                </small>
            </div>
        `;

        document.body.appendChild(tooltip);

        // Position tooltip
        const rect = targetElement.getBoundingClientRect();
        tooltip.style.top = `${rect.bottom + 10}px`;
        tooltip.style.left = `${rect.left}px`;

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (tooltip.parentElement) {
                tooltip.remove();
            }
        }, 5000);
    }

    /**
     * Refresh annotations on a chart
     * @param {string} chartType - Chart type to refresh
     */
    async refreshChartAnnotations(chartType) {
        // Reload annotations from backend
        try {
            const annotations = await window.annotationManager.fetchAnnotationsByChartType(chartType);

            // Trigger chart refresh if chart manager exists
            if (window.chartManager) {
                const chart = window.chartManager.getChart(chartType);
                if (chart) {
                    this.addAnnotationMarkers(chartType, annotations, chart);
                }
            }
        } catch (error) {
            console.error('Error refreshing chart annotations:', error);
        }
    }

    /**
     * Show annotation context menu
     * @param {HTMLElement} target - Target element
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point
     * @param {number} x - Mouse X position
     * @param {number} y - Mouse Y position
     */
    showContextMenu(target, chartType, dataPoint, x, y) {
        // Remove existing context menu
        const existingMenu = document.getElementById('annotation-context-menu');
        if (existingMenu) {
            existingMenu.remove();
        }

        const menu = document.createElement('div');
        menu.id = 'annotation-context-menu';
        menu.className = 'annotation-context-menu';
        menu.style.left = `${x}px`;
        menu.style.top = `${y}px`;

        // Check if annotation exists
        const existingAnnotation = window.annotationManager.getCachedAnnotation(chartType, dataPoint);

        if (existingAnnotation) {
            menu.innerHTML = `
                <div class="context-menu-item" onclick="window.annotationUI.viewAnnotation(${existingAnnotation.id})">
                    📝 View Annotation
                </div>
                <div class="context-menu-item" onclick="window.annotationUI.editAnnotation(${existingAnnotation.id})">
                    ✏️ Edit Annotation
                </div>
                <div class="context-menu-item context-menu-danger" onclick="window.annotationUI.deleteAnnotation(${existingAnnotation.id})">
                    🗑️ Delete Annotation
                </div>
            `;
        } else {
            menu.innerHTML = `
                <div class="context-menu-item" onclick="window.annotationUI.openModalFromPoint('${chartType}', ${JSON.stringify(dataPoint).replace(/"/g, '&quot;')})">
                    ➕ Add Annotation
                </div>
            `;
        }

        document.body.appendChild(menu);

        // Close menu when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeMenu(e) {
                if (!menu.contains(e.target)) {
                    menu.remove();
                    document.removeEventListener('click', closeMenu);
                }
            });
        }, 0);
    }

    /**
     * Open modal from context menu
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point
     */
    openModalFromPoint(chartType, dataPoint) {
        this.openModal(chartType, dataPoint);
    }

    /**
     * View an annotation
     * @param {number} id - Annotation ID
     */
    async viewAnnotation(id) {
        try {
            const annotation = await window.annotationManager.fetchAnnotationById(id);
            if (annotation) {
                alert(`Annotation:\n\n${annotation.note}`);
            }
        } catch (error) {
            console.error('Error viewing annotation:', error);
        }
    }

    /**
     * Edit an annotation
     * @param {number} id - Annotation ID
     */
    async editAnnotation(id) {
        try {
            const annotation = await window.annotationManager.fetchAnnotationById(id);
            if (annotation) {
                this.openModal(annotation.chart_type, annotation.data_point, annotation.note);
            }
        } catch (error) {
            console.error('Error editing annotation:', error);
        }
    }

    /**
     * Delete an annotation
     * @param {number} id - Annotation ID
     */
    async deleteAnnotation(id) {
        if (!confirm('Are you sure you want to delete this annotation?')) {
            return;
        }

        try {
            await window.annotationManager.deleteAnnotation(id);

            // Refresh chart
            if (window.chartManager) {
                const chartTypes = ['gcode_trend', 'planetary', 'element', 'forecast', 'network'];
                chartTypes.forEach(type => this.refreshChartAnnotations(type));
            }

            alert('Annotation deleted successfully');
        } catch (error) {
            console.error('Error deleting annotation:', error);
            alert('Failed to delete annotation: ' + error.message);
        }
    }

    /**
     * Escape HTML to prevent XSS
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Create annotation summary for a chart
     * @param {string} chartType - Chart type
     * @returns {Promise<string>} HTML string with annotation summary
     */
    async createAnnotationSummary(chartType) {
        try {
            const annotations = await window.annotationManager.fetchAnnotationsByChartType(chartType);

            if (annotations.length === 0) {
                return '<p class="no-annotations">No annotations for this chart yet.</p>';
            }

            let html = `<div class="annotation-summary">
                <h4>Annotations (${annotations.length})</h4>
                <ul class="annotation-list">`;

            annotations.forEach(annotation => {
                html += `
                    <li class="annotation-summary-item">
                        <div class="annotation-summary-header">
                            <strong>${annotation.data_point_display}</strong>
                            <small>${new Date(annotation.created_at).toLocaleDateString()}</small>
                        </div>
                        <p>${this.escapeHtml(annotation.note)}</p>
                    </li>
                `;
            });

            html += '</ul></div>';
            return html;
        } catch (error) {
            console.error('Error creating annotation summary:', error);
            return '<p class="error">Failed to load annotations.</p>';
        }
    }
}

/**
 * Global annotation UI instance
 */
window.annotationUI = new AnnotationUI();

// Export for global use
window.AnnotationUI = AnnotationUI;
