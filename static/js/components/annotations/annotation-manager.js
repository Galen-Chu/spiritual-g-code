/**
 * Annotation Manager
 * Handles backend API interaction for chart annotations
 */

class AnnotationManager {
    constructor() {
        this.apiBaseUrl = '/api/annotations/';
        this.annotationsCache = new Map();
    }

    /**
     * Get authentication token
     * @returns {string|null} JWT token or null
     */
    getAuthToken() {
        return localStorage.getItem('access_token');
    }

    /**
     * Get API headers with authentication
     * @returns {object} Headers object
     */
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        const token = this.getAuthToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return headers;
    }

    /**
     * Fetch all annotations for current user
     * @param {object} filters - Optional filters (e.g., { chart_type: 'gcode_trend' })
     * @returns {Promise<Array>} List of annotations
     */
    async fetchAnnotations(filters = {}) {
        try {
            const queryParams = new URLSearchParams(filters).toString();
            const url = queryParams ? `${this.apiBaseUrl}?${queryParams}` : this.apiBaseUrl;

            const response = await fetch(url, {
                method: 'GET',
                headers: this.getHeaders(),
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch annotations: ${response.statusText}`);
            }

            const data = await response.json();
            const annotations = data.results || data;

            // Update cache
            annotations.forEach(annotation => {
                const key = this._getAnnotationKey(annotation.chart_type, annotation.data_point);
                this.annotationsCache.set(key, annotation);
            });

            return annotations;
        } catch (error) {
            console.error('Error fetching annotations:', error);
            throw error;
        }
    }

    /**
     * Fetch annotations by chart type
     * @param {string} chartType - Type of chart (e.g., 'gcode_trend', 'planetary')
     * @returns {Promise<Array>} List of annotations for the chart
     */
    async fetchAnnotationsByChartType(chartType) {
        try {
            const response = await fetch(`${this.apiBaseUrl}by_chart_type/?chart_type=${chartType}`, {
                method: 'GET',
                headers: this.getHeaders(),
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch annotations: ${response.statusText}`);
            }

            const data = await response.json();
            return data.results || data;
        } catch (error) {
            console.error('Error fetching annotations by chart type:', error);
            throw error;
        }
    }

    /**
     * Create a new annotation
     * @param {object} annotationData - Annotation data
     * @param {string} annotationData.chart_type - Type of chart
     * @param {object} annotationData.data_point - Data point being annotated
     * @param {string} annotationData.note - User's note
     * @returns {Promise<object>} Created annotation
     */
    async createAnnotation(annotationData) {
        try {
            const response = await fetch(this.apiBaseUrl, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(annotationData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || errorData.error || 'Failed to create annotation');
            }

            const annotation = await response.json();

            // Update cache
            const key = this._getAnnotationKey(annotation.chart_type, annotation.data_point);
            this.annotationsCache.set(key, annotation);

            return annotation;
        } catch (error) {
            console.error('Error creating annotation:', error);
            throw error;
        }
    }

    /**
     * Update an existing annotation
     * @param {number} id - Annotation ID
     * @param {object} updates - Fields to update
     * @returns {Promise<object>} Updated annotation
     */
    async updateAnnotation(id, updates) {
        try {
            const response = await fetch(`${this.apiBaseUrl}${id}/`, {
                method: 'PATCH',
                headers: this.getHeaders(),
                body: JSON.stringify(updates),
            });

            if (!response.ok) {
                throw new Error(`Failed to update annotation: ${response.statusText}`);
            }

            const annotation = await response.json();

            // Update cache
            const key = this._getAnnotationKey(annotation.chart_type, annotation.data_point);
            this.annotationsCache.set(key, annotation);

            return annotation;
        } catch (error) {
            console.error('Error updating annotation:', error);
            throw error;
        }
    }

    /**
     * Delete an annotation
     * @param {number} id - Annotation ID
     * @returns {Promise<boolean>} True if successful
     */
    async deleteAnnotation(id) {
        try {
            // Get annotation data before deleting for cache cleanup
            const annotation = await this.fetchAnnotationById(id);
            if (annotation) {
                const key = this._getAnnotationKey(annotation.chart_type, annotation.data_point);
                this.annotationsCache.delete(key);
            }

            const response = await fetch(`${this.apiBaseUrl}${id}/`, {
                method: 'DELETE',
                headers: this.getHeaders(),
            });

            if (!response.ok) {
                throw new Error(`Failed to delete annotation: ${response.statusText}`);
            }

            return true;
        } catch (error) {
            console.error('Error deleting annotation:', error);
            throw error;
        }
    }

    /**
     * Fetch a single annotation by ID
     * @param {number} id - Annotation ID
     * @returns {Promise<object|null>} Annotation or null
     */
    async fetchAnnotationById(id) {
        try {
            const response = await fetch(`${this.apiBaseUrl}${id}/`, {
                method: 'GET',
                headers: this.getHeaders(),
            });

            if (!response.ok) {
                if (response.status === 404) {
                    return null;
                }
                throw new Error(`Failed to fetch annotation: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching annotation by ID:', error);
            throw error;
        }
    }

    /**
     * Get annotation from cache by chart type and data point
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point object
     * @returns {object|null} Cached annotation or null
     */
    getCachedAnnotation(chartType, dataPoint) {
        const key = this._getAnnotationKey(chartType, dataPoint);
        return this.annotationsCache.get(key) || null;
    }

    /**
     * Check if a data point has an annotation
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point object
     * @returns {boolean} True if annotated
     */
    hasAnnotation(chartType, dataPoint) {
        return this.getCachedAnnotation(chartType, dataPoint) !== null;
    }

    /**
     * Get all annotations for a chart type from cache
     * @param {string} chartType - Chart type
     * @returns {Array} List of annotations
     */
    getCachedAnnotationsByChartType(chartType) {
        return Array.from(this.annotationsCache.values()).filter(
            annotation => annotation.chart_type === chartType
        );
    }

    /**
     * Generate a unique key for caching annotations
     * @private
     * @param {string} chartType - Chart type
     * @param {object} dataPoint - Data point object
     * @returns {string} Unique key
     */
    _getAnnotationKey(chartType, dataPoint) {
        // Sort data point keys to ensure consistent keys
        const sortedKeys = Object.keys(dataPoint).sort();
        const dataPointStr = sortedKeys.map(k => `${k}:${dataPoint[k]}`).join('|');
        return `${chartType}::${dataPointStr}`;
    }

    /**
     * Clear the annotations cache
     */
    clearCache() {
        this.annotationsCache.clear();
    }

    /**
     * Preload annotations for a chart
     * @param {string} chartType - Chart type to preload
     * @returns {Promise<Array>} Loaded annotations
     */
    async preloadAnnotations(chartType) {
        try {
            const annotations = await this.fetchAnnotationsByChartType(chartType);
            console.log(`Preloaded ${annotations.length} annotations for ${chartType}`);
            return annotations;
        } catch (error) {
            console.error('Error preloading annotations:', error);
            return [];
        }
    }
}

/**
 * Global annotation manager instance
 */
window.annotationManager = new AnnotationManager();

// Export for global use
window.AnnotationManager = AnnotationManager;
