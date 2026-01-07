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
        """Initialize calculator."""
        # Planetary bodies to track
        self.planets = {
            'sun': ephem.Sun(),
            'moon': ephem.Moon(),
            'mercury': ephem.Mercury(),
            'venus': ephem.Venus(),
            'mars': ephem.Mars(),
            'jupiter': ephem.Jupiter(),
            'saturn': ephem.Saturn(),
            'uranus': ephem.Uranus(),
            'neptune': ephem.Neptune(),
            'pluto': ephem.Pluto(),
        }

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

            # Calculate planetary positions
            chart_data = {}
            sun_sign = None
            moon_sign = None

            for planet_name, planet in self.planets.items():
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

            # Calculate current planetary positions
            transit_data = {}
            for planet_name, planet in self.planets.items():
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
