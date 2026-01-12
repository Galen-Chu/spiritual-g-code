/**
 * Aspects Network Chart Component
 * Displays planetary aspect relationships using Cytoscape.js
 */

class AspectsNetworkChart {
    constructor(containerId) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        this.cy = null;
    }

    async loadChartData() {
        try {
            const response = await fetch('/api/dashboard/charts/?type=aspects_network');
            if (!response.ok) throw new Error('Failed to fetch chart data');
            const data = await response.json();
            return data.aspects_network || this.getMockData();
        } catch (error) {
            console.error('Error loading chart data:', error);
            return this.getMockData();
        }
    }

    getMockData() {
        // Mock network data for testing
        return {
            nodes: [
                { data: { id: 'sun', label: 'Sun', group: 'personal' } },
                { data: { id: 'moon', label: 'Moon', group: 'personal' } },
                { data: { id: 'mercury', label: 'Mercury', group: 'personal' } },
                { data: { id: 'venus', label: 'Venus', group: 'personal' } },
                { data: { id: 'mars', label: 'Mars', group: 'personal' } },
                { data: { id: 'jupiter', label: 'Jupiter', group: 'social' } },
                { data: { id: 'saturn', label: 'Saturn', group: 'social' } },
                { data: { id: 'uranus', label: 'Uranus', group: 'outer' } },
                { data: { id: 'neptune', label: 'Neptune', group: 'outer' } },
                { data: { id: 'pluto', label: 'Pluto', group: 'outer' } },
            ],
            edges: [
                { data: { source: 'sun', target: 'moon', type: 'conjunction', value: 2 } },
                { data: { source: 'sun', target: 'jupiter', type: 'trine', value: 1 } },
                { data: { source: 'moon', target: 'venus', type: 'sextile', value: 3 } },
                { data: { source: 'mercury', target: 'mars', type: 'square', value: 4 } },
                { data: { source: 'venus', target: 'neptune', type: 'opposition', value: 2 } },
                { data: { source: 'mars', target: 'pluto', type: 'conjunction', value: 1 } },
                { data: { source: 'jupiter', target: 'saturn', type: 'square', value: 3 } },
                { data: { source: 'uranus', target: 'mars', type: 'trine', value: 2 } },
                { data: { source: 'neptune', target: 'mercury', type: 'sextile', value: 4 } },
                { data: { source: 'pluto', target: 'sun', type: 'opposition', value: 1 } },
            ]
        };
    }

    render(data) {
        if (!this.container) {
            console.error('Container element not found');
            return;
        }

        // Convert API data format to Cytoscape format
        const elements = this._convertToCytoscapeFormat(data);

        // Destroy existing instance
        if (this.cy) {
            this.cy.destroy();
        }

        // Initialize Cytoscape
        this.cy = cytoscape({
            container: this.container,
            elements: elements,
            style: this._getStylesheet(),
            layout: {
                name: 'cose',
                // Ideal edge length
                idealEdgeLength: 80,
                // Divisor to compute edge ideal length
                edgeElasticity: 100,
                // Nested layout (for compound graphs)
                nestingFactor: 5,
                // Gravity to pull nodes toward center
                gravity: 1,
                // Number of iterations
                numIter: 1000,
                // Initial temperature (minimum)
                initialTemp: 200,
                // Temperature cooling factor
                coolingFactor: 0.95,
                // Minimum temperature
                minTemp: 1.0
            },
            minZoom: 0.5,
            maxZoom: 3,
            wheelSensitivity: 0.2
        });

        // Add interaction handlers
        this._addInteractions();

        console.log('✓ Aspects Network Chart rendered');
    }

    _convertToCytoscapeFormat(data) {
        const elements = [];

        // Convert nodes
        if (data.nodes && Array.isArray(data.nodes)) {
            data.nodes.forEach(node => {
                elements.push({
                    group: 'nodes',
                    data: {
                        id: node.id,
                        label: node.label,
                        group: node.group
                    }
                });
            });
        }

        // Convert links/edges
        if (data.links && Array.isArray(data.links)) {
            data.links.forEach((link, index) => {
                elements.push({
                    group: 'edges',
                    data: {
                        id: `edge-${index}`,
                        source: link.source,
                        target: link.target,
                        type: link.type,
                        value: link.value
                    }
                });
            });
        }

        return elements;
    }

    _getStylesheet() {
        const colors = window.GcodeChartUtils?.GCODE_COLORS || {
            green: '#00FF41',
            accent: '#58A6FF',
            red: '#FF5A5F',
            yellow: '#F4D03F',
            text: '#E6EDF3',
            bg: '#0D1117'
        };

        return [
            // Node styles - by group
            {
                selector: 'node[group="personal"]',
                style: {
                    'background-color': colors.green,
                    'label': 'data(label)',
                    'color': colors.bg,
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '14px',
                    'font-weight': 'bold',
                    'width': '50px',
                    'height': '50px',
                    'border-width': 3,
                    'border-color': colors.bg
                }
            },
            {
                selector: 'node[group="social"]',
                style: {
                    'background-color': colors.yellow,
                    'label': 'data(label)',
                    'color': colors.bg,
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '14px',
                    'font-weight': 'bold',
                    'width': '55px',
                    'height': '55px',
                    'border-width': 3,
                    'border-color': colors.bg
                }
            },
            {
                selector: 'node[group="outer"]',
                style: {
                    'background-color': colors.accent,
                    'label': 'data(label)',
                    'color': colors.bg,
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '12px',
                    'font-weight': 'bold',
                    'width': '45px',
                    'height': '45px',
                    'border-width': 3,
                    'border-color': colors.bg
                }
            },
            // Node hover effect
            {
                selector: 'node:hover',
                style: {
                    'border-width': 4,
                    'border-color': colors.text,
                    'width': '60px',
                    'height': '60px',
                    'transition-property': 'width, height, border-width',
                    'transition-duration': '0.2s'
                }
            },
            // Edge styles - by aspect type
            {
                selector: 'edge[type="conjunction"]',
                style: {
                    'width': 4,
                    'line-color': colors.green,
                    'target-arrow-color': colors.green,
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.8
                }
            },
            {
                selector: 'edge[type="opposition"]',
                style: {
                    'width': 4,
                    'line-color': colors.red,
                    'target-arrow-color': colors.red,
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.8,
                    'line-style': 'dashed'
                }
            },
            {
                selector: 'edge[type="trine"]',
                style: {
                    'width': 3,
                    'line-color': colors.green,
                    'target-arrow-color': colors.green,
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.7
                }
            },
            {
                selector: 'edge[type="square"]',
                style: {
                    'width': 3,
                    'line-color': colors.red,
                    'target-arrow-color': colors.red,
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.7
                }
            },
            {
                selector: 'edge[type="sextile"]',
                style: {
                    'width': 2,
                    'line-color': colors.yellow,
                    'target-arrow-color': colors.yellow,
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.6
                }
            },
            // Edge hover effect
            {
                selector: 'edge:hover',
                style: {
                    'width': 6,
                    'opacity': 1,
                    'transition-property': 'width, opacity',
                    'transition-duration': '0.2s'
                }
            }
        ];
    }

    _addInteractions() {
        if (!this.cy) return;

        // Show tooltip on node hover
        this.cy.on('mouseover', 'node', (evt) => {
            const node = evt.target;
            const label = node.data('label');
            const group = node.data('group');
            console.log(`Planet: ${label} (${group})`);
        });

        // Show edge info on hover
        this.cy.on('mouseover', 'edge', (evt) => {
            const edge = evt.target;
            const source = this.cy.getElementById(edge.data('source')).data('label');
            const target = this.cy.getElementById(edge.data('target')).data('label');
            const type = edge.data('type');
            console.log(`Aspect: ${source} ${type} ${target}`);
        });

        // Highlight connected nodes on tap
        this.cy.on('tap', 'node', (evt) => {
            const node = evt.target;
            const neighborhood = node.closedNeighborhood();

            // Reset all
            this.cy.elements().style('opacity', 0.3);

            // Highlight node and its neighbors
            neighborhood.style('opacity', 1);
            node.style('border-width', 5);
        });

        // Reset on background tap
        this.cy.on('tap', (evt) => {
            if (evt.target === this.cy) {
                this.cy.elements().style('opacity', 1);
                this.cy.nodes().style('border-width', 3);
            }
        });
    }

    async init() {
        // Check if Cytoscape.js is loaded
        if (typeof cytoscape === 'undefined') {
            console.error('Cytoscape.js is not loaded. Please include the library.');
            // Show message in container
            if (this.container) {
                this.container.innerHTML = `
                    <div class="flex items-center justify-center h-full text-gcode-red">
                        <p>Cytoscape.js library not loaded</p>
                    </div>
                `;
            }
            return;
        }

        const data = await this.loadChartData();
        this.render(data);
    }

    destroy() {
        if (this.cy) {
            this.cy.destroy();
            this.cy = null;
        }
    }
}

// Export for global use
window.AspectsNetworkChart = AspectsNetworkChart;
