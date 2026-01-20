"""
G-Code Calculator for Spiritual G-Code.
Handles natal chart and transit calculations.
"""

from datetime import datetime, date
from typing import Dict, Optional
import pytz
import ephem


class GCodeCalculator:
    """
    Calculator for natal charts and daily transits.
    Uses PyEphem for astronomical calculations.
    """

    def __init__(self):
        """Initialize calculator with extended celestial bodies."""
        # Classical Planets (11 including Earth)
        self.planets = {
            'sun': ephem.Sun(),
            'moon': ephem.Moon(),
            'mercury': ephem.Mercury(),
            'venus': ephem.Venus(),
            'earth': ephem.Earth(),  # NEW: Earth added
            'mars': ephem.Mars(),
            'jupiter': ephem.Jupiter(),
            'saturn': ephem.Saturn(),
            'uranus': ephem.Uranus(),
            'neptune': ephem.Neptune(),
            'pluto': ephem.Pluto(),
        }

        # Major Asteroids (NEW section)
        self.asteroids = {
            'ceres': ephem.readd('Ceres,1'),
            'pallas': ephem.readd('2 Pallas'),
            'juno': ephem.readd('3 Juno'),
            'vesta': ephem.readd('4 Vesta'),
        }

        # Centaurs (NEW section)
        self.centaurs = {
            'chiron': ephem.readd('2060 Chiron'),
        }

        # Combine all for iteration
        self.all_celestial_bodies = {**self.planets, **self.asteroids, **self.centaurs}

        # Zodiac signs
        self.zodiac_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer',
            'Leo', 'Virgo', 'Libra', 'Scorpio',
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]

    def calculate_natal_chart(
        self,
        birth_date: date,
        birth_time: Optional[str] = None,
        birth_location: str = 'Unknown',
        timezone: str = 'UTC'
    ) -> Dict:
        """
        Calculate complete natal chart.

        Args:
            birth_date: User's birth date
            birth_time: User's birth time (optional)
            birth_location: Birth location
            timezone: Timezone

        Returns:
            Dictionary with complete natal chart data
        """
        try:
            # Parse date/time
            if birth_time:
                dt = datetime.combine(birth_date, datetime.strptime(birth_time, '%H:%M').time())
            else:
                dt = datetime.combine(birth_date, datetime.min.time())

            # Make timezone-aware
            tz = pytz.timezone(timezone)
            dt = tz.localize(dt)

            # Create observer
            observer = self._create_observer(birth_location, dt)

            # Calculate planetary positions (including asteroids and centaurs)
            chart_data = {}
            sun_sign = None
            moon_sign = None

            for planet_name, planet in self.all_celestial_bodies.items():
                planet.compute(observer)
                lon = ephem.deg(planet.ra + observer.sidereal_time())
                sign = self._get_zodiac_sign(lon)
                degree = self._get_degree_in_sign(lon)

                chart_data[planet_name] = {
                    'sign': sign,
                    'degree': degree,
                    'longitude': float(lon)
                }

                if planet_name == 'sun':
                    sun_sign = sign
                elif planet_name == 'moon':
                    moon_sign = sign

            # Calculate ascendant
            ascendant = self._calculate_ascendant(observer)

            # Calculate dominant elements
            dominant_elements = self._calculate_dominant_elements(chart_data)

            # Calculate key aspects
            key_aspects = self._calculate_aspects(chart_data)

            return {
                'chart_data': chart_data,
                'sun_sign': sun_sign,
                'moon_sign': moon_sign,
                'ascendant': ascendant,
                'dominant_elements': dominant_elements,
                'key_aspects': key_aspects
            }

        except Exception as e:
            raise Exception(f"Error calculating natal chart: {str(e)}")

    def calculate_transits(
        self,
        birth_date: date,
        birth_location: str,
        target_date: date,
        birth_time: Optional[str] = None
    ) -> Dict:
        """
        Calculate current transits and aspects to natal chart.

        Args:
            birth_date: User's birth date
            birth_location: Birth location
            target_date: Date to calculate transits for
            birth_time: Birth time (optional)

        Returns:
            Dictionary with transit data
        """
        try:
            # Calculate natal chart first
            natal_chart = self.calculate_natal_chart(
                birth_date, birth_time, birth_location
            )

            # Create observer for target date
            dt = datetime.combine(target_date, datetime.min.time())
            observer = self._create_observer(birth_location, dt)

            # Calculate current planetary positions (including asteroids and centaurs)
            transit_data = {}
            for planet_name, planet in self.all_celestial_bodies.items():
                planet.compute(observer)
                lon = ephem.deg(planet.ra + observer.sidereal_time())
                sign = self._get_zodiac_sign(lon)
                degree = self._get_degree_in_sign(lon)

                transit_data[planet_name] = {
                    'sign': sign,
                    'degree': degree,
                    'longitude': float(lon)
                }

            # Calculate aspects to natal positions
            aspects = self._calculate_transit_aspects(
                transit_data,
                natal_chart['chart_data']
            )

            return {
                'planets': transit_data,
                'aspects': aspects,
                'natal_chart': natal_chart
            }

        except Exception as e:
            raise Exception(f"Error calculating transits: {str(e)}")

    def _create_observer(self, location: str, dt: datetime) -> ephem.Observer:
        """Create PyEphem observer for location and time."""
        observer = ephem.Observer()

        # For now, use a default location
        # In production, you'd geocode the location string
        observer.lat = '0'  # Default to equator
        observer.lon = '0'  # Default to prime meridian
        observer.elevation = 0
        observer.date = dt

        return observer

    def _get_zodiac_sign(self, longitude: float) -> str:
        """Get zodiac sign from longitude."""
        # Convert to 0-360 range
        lon = longitude % 360
        index = int(lon / 30)
        return self.zodiac_signs[index]

    def _get_degree_in_sign(self, longitude: float) -> float:
        """Get degree within zodiac sign."""
        lon = longitude % 360
        return lon % 30

    def _calculate_ascendant(self, observer: ephem.Observer) -> str:
        """Calculate ascendant sign."""
        # Simplified calculation
        # In production, use proper astronomical calculation
        lst = observer.sidereal_time()
        asc = self._get_zodiac_sign(float(lst))
        return asc

    def _calculate_dominant_elements(self, chart_data: Dict) -> Dict:
        """Calculate dominant elements in natal chart."""
        elements = {
            'fire': 0,  # Aries, Leo, Sagittarius
            'earth': 0,  # Taurus, Virgo, Capricorn
            'air': 0,   # Gemini, Libra, Aquarius
            'water': 0   # Cancer, Scorpio, Pisces
        }

        fire_signs = ['Aries', 'Leo', 'Sagittarius']
        earth_signs = ['Taurus', 'Virgo', 'Capricorn']
        air_signs = ['Gemini', 'Libra', 'Aquarius']
        water_signs = ['Cancer', 'Scorpio', 'Pisces']

        for planet_data in chart_data.values():
            sign = planet_data['sign']
            if sign in fire_signs:
                elements['fire'] += 1
            elif sign in earth_signs:
                elements['earth'] += 1
            elif sign in air_signs:
                elements['air'] += 1
            elif sign in water_signs:
                elements['water'] += 1

        return elements

    def _calculate_aspects(self, chart_data: Dict) -> List[Dict]:
        """Calculate aspects between planets in natal chart."""
        aspects = []
        planets = list(chart_data.keys())

        aspect_types = {
            'conjunction': 0,
            'opposition': 180,
            'trine': 120,
            'square': 90,
            'sextile': 60
        }

        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                lon1 = chart_data[p1]['longitude']
                lon2 = chart_data[p2]['longitude']
                diff = abs(lon1 - lon2) % 360

                if diff > 180:
                    diff = 360 - diff

                # Check for aspects (with 8 degree orb)
                for aspect_name, aspect_angle in aspect_types.items():
                    if abs(diff - aspect_angle) <= 8:
                        aspects.append({
                            'planet1': p1,
                            'planet2': p2,
                            'aspect': aspect_name,
                            'orb': abs(diff - aspect_angle)
                        })

        return aspects

    def _calculate_transit_aspects(
        self,
        transit_data: Dict,
        natal_data: Dict
    ) -> List[Dict]:
        """Calculate aspects between transiting and natal planets."""
        aspects = []
        aspect_types = {
            'conjunction': 0,
            'opposition': 180,
            'trine': 120,
            'square': 90,
            'sextile': 60
        }

        for transit_planet, transit_pos in transit_data.items():
            for natal_planet, natal_pos in natal_data.items():
                diff = abs(transit_pos['longitude'] - natal_pos['longitude']) % 360

                if diff > 180:
                    diff = 360 - diff

                for aspect_name, aspect_angle in aspect_types.items():
                    if abs(diff - aspect_angle) <= 8:
                        aspects.append({
                            'transit_planet': transit_planet,
                            'natal_planet': natal_planet,
                            'aspect': aspect_name,
                            'orb': abs(diff - aspect_angle)
                        })

        return aspects

    def calculate_extended_aspects(
        self,
        natal_data: Dict,
        transit_data: Dict = None
    ) -> Dict:
        """
        Calculate extended aspects including asteroids and lunar nodes.

        Args:
            natal_data: Natal chart data
            transit_data: Current transit data (optional)

        Returns:
            Dictionary with all aspect categories
        """
        all_aspects = {
            'natal_aspects': [],  # Between natal planets (classic)
            'asteroid_aspects': [],  # Asteroid-to-asteroid and asteroid-to-natal
            'node_aspects': [],  # Lunar node aspects
            'extended_transit_aspects': []  # Transit asteroids/nodes to natal
        }

        aspect_types = {
            'conjunction': 0,
            'opposition': 180,
            'trine': 120,
            'square': 90,
            'sextile': 60
        }

        # Calculate natal aspects with asteroids included
        for body1_name, body1 in self.all_celestial_bodies.items():
            for body2_name, body2 in self.all_celestial_bodies.items():
                if body1_name >= body2_name:  # Avoid duplicates
                    continue

                # Get positions from natal_data
                if body1_name in natal_data and body2_name in natal_data:
                    lon1 = natal_data[body1_name]['longitude']
                    lon2 = natal_data[body2_name]['longitude']

                    # Calculate aspect
                    diff = abs(lon1 - lon2) % 360
                    if diff > 180:
                        diff = 360 - diff

                    for aspect_name, aspect_angle in aspect_types.items():
                        if abs(diff - aspect_angle) <= 8:
                            all_aspects['natal_aspects'].append({
                                'body1': body1_name,
                                'body2': body2_name,
                                'aspect': aspect_name,
                                'orb': abs(diff - aspect_angle)
                            })

        # Calculate lunar node aspects to natal
        if natal_data:
            # We'll calculate node positions based on the transit data
            # For now, create a simplified calculation
            node_orb = 6793.5  # 18.6 years
            epoch = date(2000, 1, 1)

            # Get user birth date from somewhere (this would need to be passed in)
            # For now, calculate current node positions
            if transit_data and 'lunar_nodes' in transit_data:
                nn_lon = transit_data['lunar_nodes']['north_node']['longitude']
                sn_lon = transit_data['lunar_nodes']['south_node']['longitude']

                # Check node aspects to natal planets
                for natal_planet, natal_pos in natal_data.items():
                    # North Node aspects
                    diff_nn = abs(nn_lon - natal_pos['longitude']) % 360
                    if diff_nn > 180:
                        diff_nn = 360 - diff_nn

                    for aspect_name, aspect_angle in aspect_types.items():
                        if abs(diff_nn - aspect_angle) <= 8:
                            all_aspects['node_aspects'].append({
                                'node': 'north_node',
                                'natal_planet': natal_planet,
                                'aspect': aspect_name,
                                'orb': abs(diff_nn - aspect_angle)
                            })

                    # South Node aspects
                    diff_sn = abs(sn_lon - natal_pos['longitude']) % 360
                    if diff_sn > 180:
                        diff_sn = 360 - diff_sn

                    for aspect_name, aspect_angle in aspect_types.items():
                        if abs(diff_sn - aspect_angle) <= 8:
                            all_aspects['node_aspects'].append({
                                'node': 'south_node',
                                'natal_planet': natal_planet,
                                'aspect': aspect_name,
                                'orb': abs(diff_sn - aspect_angle)
                            })

        return all_aspects

    def calculate_solar_system_transits(self, target_date: date) -> Dict:
        """
        Calculate heliocentric positions for all celestial bodies.
        Returns data for D3.js solar system visualization.
        """
        dt = datetime.combine(target_date, datetime.min.time())
        observer = ephem.Observer()
        observer.date = dt

        solar_system_data = {
            'date': target_date.isoformat(),
            'bodies': []
        }

        # Orbital radii in AU (for visualization scaling)
        orbital_radii = {
            'mercury': 0.39, 'venus': 0.72, 'earth': 1.0, 'mars': 1.52,
            'ceres': 2.77, 'pallas': 2.77, 'juno': 2.77, 'vesta': 2.77,
            'jupiter': 5.2, 'saturn': 9.58, 'chiron': 13.7,
            'uranus': 19.2, 'neptune': 30.05, 'pluto': 39.48
        }

        for body_name, body in self.all_celestial_bodies.items():
            body.compute(observer)

            # Get heliocentric longitude
            helio_lon = body.hlong
            geocentric_lon = ephem.deg(body.ra + observer.sidereal_time())

            solar_system_data['bodies'].append({
                'name': body_name,
                'symbol': self._get_planet_symbol(body_name),
                'category': self._get_celestial_category(body_name),
                'heliocentric_longitude': float(helio_lon),
                'geocentric_longitude': float(geocentric_lon),
                'orbital_radius_au': orbital_radii.get(body_name, 1.0),
                'zodiac_sign': self._get_zodiac_sign(geocentric_lon),
                'degree_in_sign': float(self._get_degree_in_sign(geocentric_lon))
            })

        # Calculate lunar nodes (geocentric)
        lunar_nodes = self.calculate_lunar_nodes(observer)
        solar_system_data['lunar_nodes'] = lunar_nodes

        return solar_system_data

    def _get_planet_symbol(self, body_name: str) -> str:
        """Get astronomical symbol for celestial body."""
        symbols = {
            'sun': '☉', 'moon': '☽', 'mercury': '☿', 'venus': '♀',
            'earth': '🌍', 'mars': '♂', 'jupiter': '♃', 'saturn': '♄',
            'uranus': '♅', 'neptune': '♆', 'pluto': '♇',
            'ceres': '⚳', 'pallas': '⚴', 'juno': '⚵', 'vesta': '⚶',
            'chiron': '⚷'
        }
        return symbols.get(body_name, body_name[0].upper())

    def _get_celestial_category(self, body_name: str) -> str:
        """Get category for visualization grouping."""
        categories = {
            'sun': 'star',
            'moon': 'satellite',
            'mercury': 'personal', 'venus': 'personal', 'earth': 'personal', 'mars': 'personal',
            'ceres': 'asteroid', 'pallas': 'asteroid', 'juno': 'asteroid', 'vesta': 'asteroid',
            'jupiter': 'social', 'saturn': 'social',
            'chiron': 'centaur',
            'uranus': 'outer', 'neptune': 'outer', 'pluto': 'outer'
        }
        return categories.get(body_name, 'unknown')

    def calculate_lunar_nodes(self, observer) -> Dict:
        """
        Calculate the true lunar nodes (North and South).
        Returns geocentric longitudes for both nodes.

        The nodes are mathematical points where the Moon's orbit
        crosses the ecliptic. They are always exactly 180° apart.
        """
        import math

        # Get Julian Date
        j2000_epoch = 2451545.0
        jd = observer.date + 2415020  # Convert to Julian Date
        days_since_j2000 = jd - j2000_epoch

        # Mean North Node calculation (simplified)
        # Based on lunar orbit precession period of 18.6 years
        node_period = 6793.5  # days
        node_offset = (days_since_j2000 % node_period) / node_period * 360

        # Nodes move in retrograde (backwards)
        north_node_longitude = (125.0445 - node_offset * 360 / node_period) % 360
        south_node_longitude = (north_node_longitude + 180) % 360

        return {
            'north_node': {
                'name': 'north_node',
                'symbol': '☊',
                'longitude': round(north_node_longitude, 4),
                'zodiac_sign': self._get_zodiac_sign(north_node_longitude),
                'degree_in_sign': round(north_node_longitude % 30, 2)
            },
            'south_node': {
                'name': 'south_node',
                'symbol': '☋',
                'longitude': round(south_node_longitude, 4),
                'zodiac_sign': self._get_zodiac_sign(south_node_longitude),
                'degree_in_sign': round(south_node_longitude % 30, 2)
            }
        }
