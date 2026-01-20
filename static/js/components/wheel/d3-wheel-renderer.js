/**
 * D3.js Natal Wheel Renderer
 * Renders traditional circular zodiac wheel with Placidus houses
 */

class D3WheelRenderer {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);

        if (!this.container) {
            throw new Error(`Container ${containerId} not found`);
        }

        // Dimensions
        this.width = options.width || 700;
        this.height = options.height || 700;
        this.margin = options.margin || 40;
        this.radius = Math.min(this.width, this.height) / 2 - this.margin;

        // Colors (Terminal-Chic theme)
        this.colors = {
            fire: '#FF6B6B',      // Aries, Leo, Sagittarius
            earth: '#4ECDC4',     // Taurus, Virgo, Capricorn
            air: '#95E1D3',       // Gemini, Libra, Aquarius
            water: '#45B7D1',     // Cancer, Scorpio, Pisces
            background: '#0D1117',
            wheelBorder: '#30363d',
            text: '#E6EDF3',
            aspectLines: {
                conjunction: '#FFD93D',
                opposition: '#FF5A5F',
                trine: '#00FF41',
                square: '#FF6B6B',
                sextile: '#4ECDC4'
            }
        };

        // Zodiac symbols
        this.zodiacSymbols = {
            'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊',
            'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍',
            'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐',
            'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'
        };

        // Planet symbols (including Earth, asteroids, and centaurs)
        this.planetSymbols = {
            'sun': '☉', 'moon': '☽', 'mercury': '☿',
            'venus': '♀', 'earth': '🌍', 'mars': '♂',
            'jupiter': '♃', 'saturn': '♄', 'uranus': '♅',
            'neptune': '♆', 'pluto': '♇',
            'ceres': '⚳', 'pallas': '⚴', 'juno': '⚵', 'vesta': '⚶',
            'chiron': '⚷'
        };

        // Sign colors
        this.signColors = {
            'Aries': this.colors.fire,
            'Leo': this.colors.fire,
            'Sagittarius': this.colors.fire,
            'Taurus': this.colors.earth,
            'Virgo': this.colors.earth,
            'Capricorn': this.colors.earth,
            'Gemini': this.colors.air,
            'Libra': this.colors.air,
            'Aquarius': this.colors.air,
            'Cancer': this.colors.water,
            'Scorpio': this.colors.water,
            'Pisces': this.colors.water
        };

        // D3 selection
        this.svg = null;
        this.g = null;

        // Data
        this.wheelData = null;

        console.log(`✓ D3WheelRenderer initialized for ${containerId}`);
    }

    /**
     * Initialize the wheel
     */
    init() {
        // Clear container
        this.container.innerHTML = '';

        // Create SVG
        this.svg = d3.select(`#${this.containerId}`)
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('class', 'natal-wheel-svg')
            .style('background-color', this.colors.background);

        // Create main group centered
        this.g = this.svg.append('g')
            .attr('transform', `translate(${this.width / 2}, ${this.height / 2})`);

        console.log('✓ D3WheelRenderer SVG initialized');
    }

    /**
     * Render the complete wheel
     */
    render(wheelData) {
        if (!wheelData) {
            console.error('No wheel data provided');
            return;
        }

        this.wheelData = wheelData;

        // Clear previous rendering
        this.g.selectAll('*').remove();

        // Draw components
        this.drawZodiacWheel();
        this.drawHouses();
        this.drawPlanets();
        this.drawAspects();
        this.drawCenter();

        console.log('✓ Natal wheel rendered successfully');
    }

    /**
     * Draw the zodiac wheel (12 signs)
     */
    drawZodiacWheel() {
        const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];

        // Outer wheel (zodiac signs)
        const outerRadius = this.radius;
        const innerRadius = this.radius * 0.75;

        signs.forEach((sign, i) => {
            const startAngle = (i * 30 - 90) * (Math.PI / 180);
            const endAngle = ((i + 1) * 30 - 90) * (Math.PI / 180);

            // Draw sign segment
            this.g.append('path')
                .attr('d', d3.arc()
                    .innerRadius(innerRadius)
                    .outerRadius(outerRadius)
                    .startAngle(startAngle)
                    .endAngle(endAngle))
                .attr('fill', this.signColors[sign])
                .attr('stroke', this.colors.wheelBorder)
                .attr('stroke-width', 2)
                .attr('opacity', 0.3)
                .attr('class', 'zodiac-segment')
                .datum({ sign: sign })
                .on('mouseover', (event, d) => this.showTooltip(event, d.sign))
                .on('mouseout', () => this.hideTooltip());

            // Add sign symbol
            const midAngle = (startAngle + endAngle) / 2;
            const symbolRadius = (innerRadius + outerRadius) / 2;
            const x = symbolRadius * Math.cos(midAngle);
            const y = symbolRadius * Math.sin(midAngle);

            this.g.append('text')
                .attr('x', x)
                .attr('y', y)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('fill', this.colors.text)
                .attr('font-size', '28px')
                .attr('font-weight', 'bold')
                .text(this.zodiacSymbols[sign]);
        });

        // Degree markers
        for (let i = 0; i < 360; i += 5) {
            const angle = (i - 90) * (Math.PI / 180);
            const isMajor = i % 30 === 0;
            const markLength = isMajor ? 15 : 8;
            const markRadius = outerRadius + markLength;

            this.g.append('line')
                .attr('x1', outerRadius * Math.cos(angle))
                .attr('y1', outerRadius * Math.sin(angle))
                .attr('x2', markRadius * Math.cos(angle))
                .attr('y2', markRadius * Math.sin(angle))
                .attr('stroke', isMajor ? this.colors.text : '#8B949E')
                .attr('stroke-width', isMajor ? 2 : 1);
        }
    }

    /**
     * Draw house cusps
     */
    drawHouses() {
        if (!this.wheelData.houses) {
            console.warn('No house data available');
            return;
        }

        const innerRadius = this.radius * 0.75;
        const centerRadius = this.radius * 0.4;

        // Draw house divisions
        for (let i = 1; i <= 12; i++) {
            const house = this.wheelData.houses[i];
            if (!house) continue;

            const longitude = house.longitude;
            const angle = (longitude - 90) * (Math.PI / 180);

            // Draw house cusp line
            this.g.append('line')
                .attr('x1', centerRadius * Math.cos(angle))
                .attr('y1', centerRadius * Math.sin(angle))
                .attr('x2', innerRadius * Math.cos(angle))
                .attr('y2', innerRadius * Math.sin(angle))
                .attr('stroke', '#00FF41')
                .attr('stroke-width', 2)
                .attr('stroke-dasharray', '5,3');

            // Add house number
            const textRadius = (innerRadius + centerRadius) / 2;
            const nextHouse = this.wheelData.houses[i % 12 + 1] || this.wheelData.houses[1];
            const nextLongitude = nextHouse.longitude;
            const nextAngle = (nextLongitude - 90) * (Math.PI / 180);
            const midAngle = (angle + nextAngle) / 2;

            const x = textRadius * Math.cos(midAngle);
            const y = textRadius * Math.sin(midAngle);

            this.g.append('text')
                .attr('x', x)
                .attr('y', y)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('fill', '#00FF41')
                .attr('font-size', '14px')
                .attr('font-weight', 'bold')
                .text(i);
        }
    }

    /**
     * Draw planets
     */
    drawPlanets() {
        if (!this.wheelData.planets) {
            console.warn('No planet data available');
            return;
        }

        const planetRadius = this.radius * 0.85;

        Object.entries(this.wheelData.planets).forEach(([planetName, planetData]) => {
            const longitude = planetData.longitude;
            const angle = (longitude - 90) * (Math.PI / 180);

            const x = planetRadius * Math.cos(angle);
            const y = planetRadius * Math.sin(angle);

            // Draw planet circle
            this.g.append('circle')
                .attr('cx', x)
                .attr('cy', y)
                .attr('r', 22)
                .attr('fill', '#161b22')
                .attr('stroke', '#00FF41')
                .attr('stroke-width', 2)
                .attr('class', 'planet-marker')
                .datum({ planet: planetName, data: planetData })
                .on('mouseover', (event, d) => this.showPlanetTooltip(event, d))
                .on('mouseout', () => this.hideTooltip());

            // Draw planet symbol
            this.g.append('text')
                .attr('x', x)
                .attr('y', y)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .attr('fill', this.colors.text)
                .attr('font-size', '20px')
                .text(this.planetSymbols[planetName]);
        });
    }

    /**
     * Draw aspect lines
     */
    drawAspects() {
        if (!this.wheelData.aspects || this.wheelData.aspects.length === 0) {
            console.warn('No aspect data available');
            return;
        }

        const aspectRadius = this.radius * 0.6;

        this.wheelData.aspects.forEach(aspect => {
            const planet1 = this.wheelData.planets[aspect.planet1];
            const planet2 = this.wheelData.planets[aspect.planet2];

            if (!planet1 || !planet2) return;

            const angle1 = (planet1.longitude - 90) * (Math.PI / 180);
            const angle2 = (planet2.longitude - 90) * (Math.PI / 180);

            const x1 = aspectRadius * Math.cos(angle1);
            const y1 = aspectRadius * Math.sin(angle1);
            const x2 = aspectRadius * Math.cos(angle2);
            const y2 = aspectRadius * Math.sin(angle2);

            // Get aspect color
            const color = this.colors.aspectLines[aspect.aspect] || '#8B949E';

            // Determine line style
            let dashArray = 'none';
            if (aspect.aspect === 'opposition') {
                dashArray = '8,4';
            } else if (aspect.aspect === 'square') {
                dashArray = '5,3';
            } else if (aspect.aspect === 'trine') {
                dashArray = '10,5';
            } else if (aspect.aspect === 'sextile') {
                dashArray = '3,3';
            }

            // Draw aspect line
            this.g.append('line')
                .attr('x1', x1)
                .attr('y1', y1)
                .attr('x2', x2)
                .attr('y2', y2)
                .attr('stroke', color)
                .attr('stroke-width', 1.5)
                .attr('stroke-dasharray', dashArray)
                .attr('opacity', 0.6)
                .attr('class', 'aspect-line')
                .datum(aspect)
                .on('mouseover', (event, d) => this.showAspectTooltip(event, d))
                .on('mouseout', () => this.hideTooltip());
        });
    }

    /**
     * Draw center information
     */
    drawCenter() {
        const centerRadius = this.radius * 0.3;

        // Draw center circle
        this.g.append('circle')
            .attr('r', centerRadius)
            .attr('fill', '#161b22')
            .attr('stroke', '#30363d')
            .attr('stroke-width', 2);

        // Add sun sign
        if (this.wheelData.sun_sign) {
            this.g.append('text')
                .attr('y', -10)
                .attr('text-anchor', 'middle')
                .attr('fill', this.colors.text)
                .attr('font-size', '16px')
                .text(`Sun: ${this.zodiacSymbols[this.wheelData.sun_sign] || this.wheelData.sun_sign}`);
        }

        // Add moon sign
        if (this.wheelData.moon_sign) {
            this.g.append('text')
                .attr('y', 15)
                .attr('text-anchor', 'middle')
                .attr('fill', this.colors.text)
                .attr('font-size', '16px')
                .text(`Moon: ${this.zodiacSymbols[this.wheelData.moon_sign] || this.wheelData.moon_sign}`);
        }

        // Add ascendant
        if (this.wheelData.ascendant) {
            this.g.append('text')
                .attr('y', 40)
                .attr('text-anchor', 'middle')
                .attr('fill', '#00FF41')
                .attr('font-size', '14px')
                .attr('font-weight', 'bold')
                .text(`Asc: ${this.wheelData.ascendant}`);
        }
    }

    /**
     * Show tooltip
     */
    showTooltip(event, text) {
        let tooltip = document.getElementById('wheel-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'wheel-tooltip';
            tooltip.className = 'wheel-tooltip';
            document.body.appendChild(tooltip);
        }

        tooltip.textContent = text;
        tooltip.style.display = 'block';
        tooltip.style.left = (event.pageX + 15) + 'px';
        tooltip.style.top = (event.pageY - 10) + 'px';
    }

    /**
     * Show planet tooltip
     */
    showPlanetTooltip(event, d) {
        const text = `${d.planet.charAt(0).toUpperCase() + d.planet.slice(1)} in ${d.data.sign} ${d.data.degree.toFixed(2)}°`;
        this.showTooltip(event, text);
    }

    /**
     * Show aspect tooltip
     */
    showAspectTooltip(event, d) {
        const text = `${d.planet1} ${d.aspect} ${d.planet2} (orb: ${d.orb}°)`;
        this.showTooltip(event, text);
    }

    /**
     * Hide tooltip
     */
    hideTooltip() {
        const tooltip = document.getElementById('wheel-tooltip');
        if (tooltip) {
            tooltip.style.display = 'none';
        }
    }

    /**
     * Clear the wheel
     */
    clear() {
        if (this.g) {
            this.g.selectAll('*').remove();
        }
        console.log('✓ Wheel cleared');
    }

    /**
     * Destroy the wheel
     */
    destroy() {
        this.clear();
        if (this.svg) {
            this.svg.remove();
        }
        console.log('✓ Wheel destroyed');
    }

    /**
     * Export wheel as PNG
     */
    exportAsPNG(filename = 'natal-wheel.png') {
        const svgElement = this.container.querySelector('svg');
        if (!svgElement) {
            console.error('No SVG element found');
            return;
        }

        // Serialize SVG
        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(svgElement);

        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.width = this.width;
        canvas.height = this.height;
        const ctx = canvas.getContext('2d');

        // Create image
        const img = new Image();
        img.onload = () => {
            ctx.drawImage(img, 0, 0);

            // Download
            const link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL('image/png');
            link.click();
        };

        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgString)));
    }

    /**
     * Export wheel as SVG
     */
    exportAsSVG(filename = 'natal-wheel.svg') {
        const svgElement = this.container.querySelector('svg');
        if (!svgElement) {
            console.error('No SVG element found');
            return;
        }

        // Serialize SVG
        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(svgElement);

        // Create blob
        const blob = new Blob([svgString], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);

        // Download
        const link = document.createElement('a');
        link.download = filename;
        link.href = url;
        link.click();

        URL.revokeObjectURL(url);
    }
}

// Export for global use
window.D3WheelRenderer = D3WheelRenderer;
