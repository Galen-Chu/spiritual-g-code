/**
 * D3.js Heliocentric Solar System Visualization
 * Displays current positions of planets, asteroids, and lunar nodes
 *
 * Features:
 * - 15 celestial bodies (Sun, Moon, Earth + 10 planets + 4 asteroids + Chiron)
 * - Lunar nodes with 3 configurable display methods
 * - Interactive zoom/pan
 * - Zodiac wheel
 * - Export to PNG
 */

class SolarSystemRenderer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            width: options.width || 800,
            height: options.height || 800,
            showAsteroids: options.showAsteroids !== undefined ? options.showAsteroids : true,
            showCentaurs: options.showCentaurs !== undefined ? options.showCentaurs : true,
            showOrbits: options.showOrbits !== undefined ? options.showOrbits : true,
            // Lunar node display options
            showLunarNodes: options.showLunarNodes !== undefined ? options.showLunarNodes : true,
            lunarNodeDisplay: options.lunarNodeDisplay || 'all', // 'all', 'overlay', 'markers', 'tooltip', 'none'
            animationDuration: options.animationDuration || 1000,
            ...options
        };

        this.svg = null;
        this.zoom = null;
        this.data = null;
        this.colorScale = this._createColorScale();
        this.lunarNodeColor = '#9370DB'; // Purple for North Node
        this.southNodeColor = '#696969'; // Dim gray for South Node
    }

    _createColorScale() {
        // Color categories for celestial bodies
        return {
            star: '#FFD700',      // Sun - Gold
            satellite: '#C0C0C0', // Moon - Silver
            personal: '#4ECDC4',  // Inner planets - Teal
            asteroid: '#A0522D',  // Asteroids - Brown
            social: '#DEB887',    // Gas giants - Burlywood
            centaur: '#9370DB',   // Chiron - Purple
            outer: '#5F9EA0',     // Outer planets - Cadet blue
            north_node: '#9370DB', // North Node - Purple
            south_node: '#696969'  // South Node - Dim gray (shadow)
        };
    }

    async loadData(targetDate = null) {
        try {
            const dateParam = targetDate || new Date().toISOString().split('T')[0];
            const url = targetDate
                ? `/api/solar-system/transits/?date=${dateParam}`
                : '/api/solar-system/transits/';

            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch solar system data');

            this.data = await response.json();
            return this.data;
        } catch (error) {
            console.error('Error loading solar system data:', error);
            throw error;
        }
    }

    render() {
        if (!this.data || !this.data.bodies) {
            console.error('No data to render');
            return;
        }

        // Clear existing content
        this.container.innerHTML = '';

        // Create SVG
        this.svg = d3.select(this.container)
            .append('svg')
            .attr('width', '100%')
            .attr('height', '100%')
            .attr('viewBox', `0 0 ${this.options.width} ${this.options.height}`)
            .attr('style', 'background: #0D1117; border-radius: 8px;');

        // Create main group with zoom capability
        const mainGroup = this.svg.append('g')
            .attr('transform', `translate(${this.options.width / 2}, ${this.options.height / 2})`);

        // Initialize zoom behavior
        this.zoom = d3.zoom()
            .scaleExtent([0.5, 3])
            .on('zoom', (event) => {
                mainGroup.attr('transform', event.transform);
            });

        this.svg.call(this.zoom);

        // Filter bodies based on options
        const bodies = this.data.bodies.filter(body => {
            if (body.category === 'asteroid' && !this.options.showAsteroids) return false;
            if (body.category === 'centaur' && !this.options.showCentaurs) return false;
            return true;
        });

        // Calculate scaled orbital radii (using square root scale for visibility)
        const maxRadius = Math.max(...bodies.map(b => b.orbital_radius_au));
        const scaleFactor = (this.options.width / 2 - 80) / Math.sqrt(maxRadius);

        const scaledBodies = bodies.map(body => ({
            ...body,
            scaled_radius: Math.sqrt(body.orbital_radius_au) * scaleFactor,
            x: Math.cos((body.heliocentric_longitude - 90) * Math.PI / 180) *
               Math.sqrt(body.orbital_radius_au) * scaleFactor,
            y: Math.sin((body.heliocentric_longitude - 90) * Math.PI / 180) *
               Math.sqrt(body.orbital_radius_au) * scaleFactor
        }));

        // Draw zodiac wheel (outer ring)
        this._drawZodiacWheel(mainGroup, this.options.width / 2 - 50);

        // Draw lunar nodes (if enabled)
        if (this.options.showLunarNodes && this.data.lunar_nodes) {
            this._drawLunarNodes(mainGroup, this.options.width / 2 - 50);
        }

        // Draw orbital paths
        if (this.options.showOrbits) {
            this._drawOrbits(mainGroup, scaledBodies);
        }

        // Draw celestial bodies
        this._drawBodies(mainGroup, scaledBodies);

        // Add legend
        this._drawLegend(this.svg);

        // Add date label
        this.svg.append('text')
            .attr('x', 20)
            .attr('y', 30)
            .attr('fill', '#00FF41')
            .attr('font-family', 'JetBrains Mono, monospace')
            .attr('font-size', '14px')
            .text(`Solar System Transit: ${this.data.date}`);
    }

    _drawZodiacWheel(group, radius) {
        const signs = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓'];
        const colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#45B7D1',
                       '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE',
                       '#85C1E2', '#F8B500', '#52B788', '#FF6F61'];

        // Outer circle
        group.append('circle')
            .attr('r', radius)
            .attr('fill', 'none')
            .attr('stroke', '#30363d')
            .attr('stroke-width', 2);

        // Sign sectors
        signs.forEach((sign, i) => {
            const startAngle = (i * 30 - 90) * Math.PI / 180;
            const endAngle = ((i + 1) * 30 - 90) * Math.PI / 180;

            // Draw sector arc
            const arc = d3.arc()
                .innerRadius(radius - 18)
                .outerRadius(radius)
                .startAngle(startAngle)
                .endAngle(endAngle);

            group.append('path')
                .attr('d', arc)
                .attr('fill', colors[i])
                .attr('opacity', 0.3);

            // Add sign symbol
            const midAngle = (startAngle + endAngle) / 2;
            const symbolRadius = radius - 9;
            group.append('text')
                .attr('x', Math.cos(midAngle) * symbolRadius)
                .attr('y', Math.sin(midAngle) * symbolRadius)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('fill', '#c9d1d9')
                .attr('font-size', '16px')
                .text(sign);
        });
    }

    _drawLunarNodes(group, zodiacRadius) {
        const displayMode = this.options.lunarNodeDisplay;
        const nodes = this.data.lunar_nodes;

        // Convert longitudes to angles
        const northAngle = (nodes.north_node.longitude - 90) * Math.PI / 180;
        const southAngle = (nodes.south_node.longitude - 90) * Math.PI / 180;

        // ==========================================
        // Option A: Geocentric Overlay Ring
        // ==========================================
        if (displayMode === 'all' || displayMode === 'overlay') {
            const overlayRadius = zodiacRadius + 25;

            // Draw dashed outer ring for nodal axis
            group.append('circle')
                .attr('r', overlayRadius)
                .attr('fill', 'none')
                .attr('stroke', this.lunarNodeColor)
                .attr('stroke-width', 1)
                .attr('stroke-dasharray', '5,5')
                .attr('opacity', 0.4);

            // Draw nodal axis line (connecting the two nodes)
            const northX = Math.cos(northAngle) * overlayRadius;
            const northY = Math.sin(northAngle) * overlayRadius;
            const southX = Math.cos(southAngle) * overlayRadius;
            const southY = Math.sin(southAngle) * overlayRadius;

            group.append('line')
                .attr('x1', northX)
                .attr('y1', northY)
                .attr('x2', southX)
                .attr('y2', southY)
                .attr('stroke', this.lunarNodeColor)
                .attr('stroke-width', 2)
                .attr('opacity', 0.6);

            // North Node marker (larger, purple)
            const northGroup = group.append('g')
                .attr('class', 'north-node')
                .attr('transform', `translate(${northX}, ${northY})`)
                .style('cursor', 'pointer');

            northGroup.append('circle')
                .attr('r', 10)
                .attr('fill', this.lunarNodeColor)
                .attr('stroke', '#fff')
                .attr('stroke-width', 2)
                .attr('filter', 'drop-shadow(0 0 10px rgba(147, 112, 219, 0.9))');

            northGroup.append('text')
                .attr('y', 5)
                .attr('text-anchor', 'middle')
                .attr('fill', '#fff')
                .attr('font-size', '14px')
                .attr('font-weight', 'bold')
                .text(nodes.north_node.symbol);

            // South Node marker (smaller, gray - shadow point)
            const southGroup = group.append('g')
                .attr('class', 'south-node')
                .attr('transform', `translate(${southX}, ${southY})`)
                .style('cursor', 'pointer');

            southGroup.append('circle')
                .attr('r', 7)
                .attr('fill', this.southNodeColor)
                .attr('stroke', '#888')
                .attr('stroke-width', 1)
                .attr('opacity', 0.7);

            southGroup.append('text')
                .attr('y', 3)
                .attr('text-anchor', 'middle')
                .attr('fill', '#fff')
                .attr('font-size', '11px')
                .text(nodes.south_node.symbol);

            // Tooltip
            northGroup.append('title')
                .text(`☊ North Node (Ascending)\n` +
                      `Sign: ${nodes.north_node.zodiac_sign} ${nodes.north_node.degree_in_sign}°\n` +
                      `Longitude: ${nodes.north_node.longitude.toFixed(2)}°\n` +
                      `Themes: Growth, destiny, soul's path`);

            southGroup.append('title')
                .text(`☋ South Node (Descending)\n` +
                      `Sign: ${nodes.south_node.zodiac_sign} ${nodes.south_node.degree_in_sign}°\n` +
                      `Longitude: ${nodes.south_node.longitude.toFixed(2)}°\n` +
                      `Themes: Past karma, release, comfort zone`);
        }

        // ==========================================
        // Option B: Zodiac Wheel Markers
        // ==========================================
        if (displayMode === 'all' || displayMode === 'markers') {
            const markerRadius = zodiacRadius - 24;

            // North Node marker on zodiac wheel
            const northMarkerX = Math.cos(northAngle) * markerRadius;
            const northMarkerY = Math.sin(northAngle) * markerRadius;

            group.append('circle')
                .attr('cx', northMarkerX)
                .attr('cy', northMarkerY)
                .attr('r', 6)
                .attr('fill', this.lunarNodeColor)
                .attr('stroke', '#fff')
                .attr('stroke-width', 1.5)
                .attr('filter', 'drop-shadow(0 0 6px rgba(147, 112, 219, 0.9))')
                .style('cursor', 'pointer');

            // Small symbol above marker
            group.append('text')
                .attr('x', northMarkerX)
                .attr('y', northMarkerY - 12)
                .attr('text-anchor', 'middle')
                .attr('fill', this.lunarNodeColor)
                .attr('font-size', '16px')
                .attr('font-weight', 'bold')
                .text('☊');

            // South Node marker on zodiac wheel
            const southMarkerX = Math.cos(southAngle) * markerRadius;
            const southMarkerY = Math.sin(southAngle) * markerRadius;

            group.append('circle')
                .attr('cx', southMarkerX)
                .attr('cy', southMarkerY)
                .attr('r', 5)
                .attr('fill', this.southNodeColor)
                .attr('stroke', '#666')
                .attr('stroke-width', 1)
                .attr('opacity', 0.6)
                .style('cursor', 'pointer');
        }

        // ==========================================
        // Option C: Tooltip Enhancement
        // ==========================================
        // This is handled in the _drawBodies method - Moon's tooltip will include nodes
        if (displayMode === 'all' || displayMode === 'tooltip' || displayMode === 'none') {
            // Store nodes for tooltip access
            this.lunarNodesData = nodes;
        }
    }

    _drawOrbits(group, bodies) {
        bodies.forEach(body => {
            group.append('circle')
                .attr('r', body.scaled_radius)
                .attr('fill', 'none')
                .attr('stroke', this.colorScale[body.category] || '#888')
                .attr('stroke-width', 1)
                .attr('stroke-dasharray', body.category === 'asteroid' ? '4,4' : 'none')
                .attr('opacity', 0.4);
        });
    }

    _drawBodies(group, bodies) {
        // Sun (center)
        group.append('circle')
            .attr('r', 18)
            .attr('fill', this.colorScale.star)
            .attr('stroke', '#FFD700')
            .attr('stroke-width', 2)
            .attr('filter', 'drop-shadow(0 0 15px rgba(255, 215, 0, 0.8))');

        group.append('text')
            .attr('y', 6)
            .attr('text-anchor', 'middle')
            .attr('fill', '#000')
            .attr('font-size', '16px')
            .attr('font-weight', 'bold')
            .text('☉');

        // Planets and asteroids
        bodies.filter(b => b.name !== 'sun').forEach(body => {
            const bodyGroup = group.append('g')
                .attr('class', 'celestial-body')
                .attr('transform', `translate(${body.x}, ${body.y})`)
                .style('cursor', 'pointer');

            // Planet circle
            const size = body.category === 'asteroid' ? 5 :
                        body.category === 'centaur' ? 7 : 9;

            bodyGroup.append('circle')
                .attr('r', size)
                .attr('fill', this.colorScale[body.category] || '#888')
                .attr('stroke', '#fff')
                .attr('stroke-width', 1.5)
                .attr('opacity', 0.9);

            // Planet symbol
            bodyGroup.append('text')
                .attr('y', 4)
                .attr('text-anchor', 'middle')
                .attr('fill', '#fff')
                .attr('font-size', '11px')
                .text(body.symbol);

            // Enhanced tooltip with lunar nodes (for Moon)
            let tooltipText = `${body.symbol} ${body.name.charAt(0).toUpperCase() + body.name.slice(1)}\n` +
                             `Sign: ${body.zodiac_sign} ${body.degree_in_sign.toFixed(2)}°\n` +
                             `Helio Long: ${body.heliocentric_longitude.toFixed(2)}°\n` +
                             `Orbit: ${body.orbital_radius_au} AU`;

            // Add lunar nodes to Moon tooltip (Option C)
            if (body.name === 'moon' && this.data.lunar_nodes &&
                (this.options.lunarNodeDisplay === 'all' || this.options.lunarNodeDisplay === 'tooltip')) {
                const nodes = this.data.lunar_nodes;
                tooltipText += `\n\n--- Nodal Axis ---\n` +
                              `☊ North: ${nodes.north_node.zodiac_sign} ${nodes.north_node.degree_in_sign}°\n` +
                              `☋ South: ${nodes.south_node.zodiac_sign} ${nodes.south_node.degree_in_sign}°`;
            }

            bodyGroup.append('title').text(tooltipText);

            // Hover effect
            bodyGroup
                .on('mouseenter', function() {
                    d3.select(this).select('circle')
                        .attr('r', size * 1.6)
                        .attr('stroke', '#00FF41')
                        .attr('stroke-width', 2);
                })
                .on('mouseleave', function() {
                    d3.select(this).select('circle')
                        .attr('r', size)
                        .attr('stroke', '#fff')
                        .attr('stroke-width', 1.5);
                });
        });
    }

    _drawLegend(svg) {
        const categories = [
            { key: 'star', label: 'Star' },
            { key: 'personal', label: 'Personal Planets' },
            { key: 'asteroid', label: 'Asteroids' },
            { key: 'social', label: 'Social Planets' },
            { key: 'centaur', label: 'Centaurs' },
            { key: 'outer', label: 'Outer Planets' }
        ];

        // Add lunar nodes to legend if enabled
        if (this.options.showLunarNodes) {
            categories.push(
                { key: 'north_node', label: '☊ North Node' },
                { key: 'south_node', label: '☋ South Node' }
            );
        }

        const legend = svg.append('g')
            .attr('transform', 'translate(20, 60)');

        categories.forEach((cat, i) => {
            const y = i * 25;

            legend.append('circle')
                .attr('cx', 8)
                .attr('cy', y)
                .attr('r', 6)
                .attr('fill', this.colorScale[cat.key] || this._getNodeColor(cat.key));

            legend.append('text')
                .attr('x', 20)
                .attr('y', y + 4)
                .attr('fill', '#c9d1d9')
                .attr('font-size', '12px')
                .attr('font-family', 'JetBrains Mono, monospace')
                .text(cat.label);
        });
    }

    _getNodeColor(key) {
        // Helper for node colors
        if (key === 'north_node') return this.lunarNodeColor;
        if (key === 'south_node') return this.southNodeColor;
        return '#888';
    }

    updateOptions(newOptions) {
        this.options = { ...this.options, ...newOptions };
        this.render();
    }

    // NEW: Specific method to toggle lunar nodes
    toggleLunarNodes(show) {
        this.options.showLunarNodes = show;
        this.render();
    }

    // NEW: Set lunar node display mode
    setLunarNodeDisplay(mode) {
        // mode: 'all', 'overlay', 'markers', 'tooltip', 'none'
        this.options.lunarNodeDisplay = mode;
        this.options.showLunarNodes = mode !== 'none';
        this.render();
    }

    exportAsPNG(filename = 'solar-system-transit.png') {
        const svgData = new XMLSerializer().serializeToString(this.svg.node());
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = function() {
            canvas.width = this.options.width;
            canvas.height = this.options.height;
            ctx.fillStyle = '#0D1117';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);

            const link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL('image/png');
            link.click();
        }.bind(this);

        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    }
}

// Export for global use
window.SolarSystemRenderer = SolarSystemRenderer;
