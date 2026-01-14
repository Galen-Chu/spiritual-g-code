"""
Mock G-Code Calculator for Spiritual G-Code.
Provides simulated astronomical calculations without requiring PyEphem.
Use this for development and testing when PyEphem is not available.
"""

from datetime import datetime, date, timedelta
from typing import Dict, Optional, List
import math
import hashlib


class MockGCodeCalculator:
    """
    Mock calculator for natal charts and daily transits.
    Uses deterministic algorithms to simulate astronomical calculations.
    Results are consistent for the same inputs (reproducible).
    """

    def __init__(self):
        """Initialize mock calculator."""
        # Zodiac signs with date ranges (approximate)
        self.zodiac_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer',
            'Leo', 'Virgo', 'Libra', 'Scorpio',
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]

        # Planets with their approximate orbital periods (in days)
        self.planet_periods = {
            'sun': 365.25,
            'moon': 27.32,
            'mercury': 87.97,
            'venus': 224.7,
            'mars': 687,
            'jupiter': 4332.59,
            'saturn': 10759.22,
            'uranus': 30685.4,
            'neptune': 60189,
            'pluto': 90560
        }

    def calculate_natal_chart(
        self,
        birth_date: date,
        birth_time: Optional[str] = None,
        birth_location: str = 'Unknown',
        timezone: str = 'UTC'
    ) -> Dict:
        """
        Calculate complete natal chart (simulated).

        Args:
            birth_date: User's birth date
            birth_time: User's birth time (optional)
            birth_location: Birth location
            timezone: Timezone

        Returns:
            Dictionary with complete natal chart data
        """
        try:
            # Create seed from birth data for consistent results
            seed = self._create_seed(birth_date, birth_time, birth_location)

            # Calculate planetary positions
            chart_data = {}
            sun_sign = None
            moon_sign = None

            for planet_name in self.planet_periods.keys():
                position = self._calculate_planet_position(
                    planet_name,
                    birth_date,
                    seed
                )

                chart_data[planet_name] = position

                if planet_name == 'sun':
                    sun_sign = position['sign']
                elif planet_name == 'moon':
                    moon_sign = position['sign']

            # Calculate ascendant (based on birth time)
            ascendant = self._calculate_ascendant(birth_date, birth_time, seed)

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
        Calculate current transits and aspects to natal chart (simulated).

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

            # Calculate current planetary positions
            transit_data = {}
            for planet_name in self.planet_periods.keys():
                position = self._calculate_planet_position(
                    planet_name,
                    target_date,
                    self._create_seed(target_date)
                )

                transit_data[planet_name] = position

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

    def calculate_g_code_intensity(
        self,
        transit_data: Dict,
        aspects: List[Dict]
    ) -> int:
        """
        Calculate G-Code intensity score based on transits and aspects.

        Args:
            transit_data: Current planetary positions
            aspects: Aspects to natal chart

        Returns:
            Intensity score (1-100)
        """
        # Base score
        score = 50

        # Add points for major aspects
        major_aspects = ['conjunction', 'opposition', 'square']
        for aspect in aspects:
            if aspect['aspect'] in major_aspects:
                score += 5
            elif aspect['aspect'] in ['trine', 'sextile']:
                score += 3

        # Consider planetary positions
        # Outer planets (slow movers) in aspect = more intensity
        outer_planets = ['uranus', 'neptune', 'pluto']
        for aspect in aspects:
            if aspect.get('transit_planet') in outer_planets:
                score += 7

        # Moon aspects add emotional intensity
        for aspect in aspects:
            if aspect.get('transit_planet') == 'moon':
                score += 4

        # Normalize to 1-100 range
        return max(1, min(100, score))

    def _create_seed(
        self,
        date_obj: date,
        time_str: Optional[str] = None,
        location: str = 'Unknown'
    ) -> float:
        """Create a deterministic seed from date/time/location."""
        # Create a string representation
        date_str = date_obj.isoformat()
        time_str = time_str or '00:00'
        combined = f"{date_str}_{time_str}_{location}"

        # Create hash
        hash_obj = hashlib.md5(combined.encode())
        hash_hex = hash_obj.hexdigest()

        # Convert to float
        return float(int(hash_hex[:8], 16)) / 42949672.95

    def _calculate_planet_position(
        self,
        planet_name: str,
        date_obj: date,
        seed: float
    ) -> Dict:
        """Calculate simulated planet position for a given date."""
        # Days since epoch
        epoch = date(2000, 1, 1)
        days_since_epoch = (date_obj - epoch).days

        # Calculate position based on orbital period
        period = self.planet_periods[planet_name]

        # Use seed to add variation based on planet name
        planet_seed = seed * sum(ord(c) for c in planet_name) / 1000.0

        # Calculate longitude (0-360)
        longitude = (days_since_epoch / period * 360 + planet_seed * 360) % 360

        # Get zodiac sign
        sign_index = int(longitude / 30) % 12
        sign = self.zodiac_signs[sign_index]

        # Degree within sign
        degree = longitude % 30

        return {
            'sign': sign,
            'degree': round(degree, 2),
            'longitude': round(longitude, 2)
        }

    def _calculate_ascendant(
        self,
        birth_date: date,
        birth_time: Optional[str],
        seed: float
    ) -> str:
        """Calculate ascendant sign (simulated)."""
        if birth_time:
            hour, minute = map(int, birth_time.split(':'))
            time_decimal = hour + minute / 60.0
        else:
            time_decimal = 12.0  # Default to noon

        # Calculate based on birth time and date
        day_of_year = (birth_date - date(birth_date.year, 1, 1)).days

        # Ascendant changes every 2 hours
        ascendant_offset = int((time_decimal / 2.0 + day_of_year / 30.0) * seed) % 12

        return self.zodiac_signs[ascendant_offset]

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

        # Calculate percentages
        total = sum(elements.values())
        if total > 0:
            for element in elements:
                elements[element] = round(elements[element] / total * 100, 1)

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
                            'orb': round(abs(diff - aspect_angle), 2)
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
                            'orb': round(abs(diff - aspect_angle), 2)
                        })

        return aspects

    def calculate_placidus_houses(
        self,
        birth_date: date,
        birth_time: Optional[str] = None,
        birth_location: str = 'Unknown',
        timezone: str = 'UTC'
    ) -> Dict:
        """
        Calculate Placidus house cusps (simplified approximation for MVP).

        Args:
            birth_date: User's birth date
            birth_time: User's birth time (optional)
            birth_location: Birth location
            timezone: Timezone

        Returns:
            Dictionary with house cusp positions
        """
        try:
            # Create seed for consistency
            seed = self._create_seed(birth_date, birth_time, birth_location)

            # Calculate ascendant
            ascendant_sign = self._calculate_ascendant(birth_date, birth_time, seed)
            ascendant_degree = (seed * 30) % 30  # Simplified degree calculation

            # Convert sign to degree offset
            sign_degrees = self.zodiac_signs.index(ascendant_sign) * 30
            ascendant_longitude = sign_degrees + ascendant_degree

            # Calculate MC (Medium Coeli) - simplified
            mc_longitude = (ascendant_longitude + 90 + seed * 10) % 360

            # Calculate house sizes
            house_sizes = self._calculate_placidus_house_sizes(ascendant_longitude, mc_longitude, seed)

            # Calculate house cusps
            houses = {}
            current_longitude = ascendant_longitude

            for i in range(1, 13):
                house_size = house_sizes[i]
                cusp_longitude = current_longitude % 360

                # Get sign and degree
                sign_index = int(cusp_longitude / 30) % 12
                sign = self.zodiac_signs[sign_index]
                degree = cusp_longitude % 30

                houses[i] = {
                    'cusp': round(degree, 2),
                    'sign': sign,
                    'longitude': round(cusp_longitude, 2)
                }

                # Move to next house
                current_longitude += house_size

            return houses

        except Exception as e:
            # Fallback to equal houses if calculation fails
            return self._calculate_equal_houses(birth_date, birth_time, birth_location, timezone)

    def _calculate_placidus_house_sizes(
        self,
        ascendant_longitude: float,
        mc_longitude: float,
        seed: float
    ) -> Dict:
        """Calculate house sizes for Placidus system (simplified)."""
        base_size = 30
        variation = (seed - 0.5) * 10  # -5 to +5 degrees variation

        house_sizes = {}

        for i in range(1, 13):
            if i <= 6:
                # Vary sizes for houses 1-6
                if i in [1, 7]:
                    size = base_size + variation * 0.5  # Angular houses
                elif i in [4, 10]:
                    size = base_size + variation * 0.3  # Succedent houses
                else:
                    size = base_size + variation * 0.2  # Cadent houses
            else:
                # Mirror for houses 7-12
                size = house_sizes[i - 6]

            # Ensure minimum and maximum sizes
            size = max(20, min(40, size))
            house_sizes[i] = size

        return house_sizes

    def _calculate_equal_houses(
        self,
        birth_date: date,
        birth_time: Optional[str] = None,
        birth_location: str = 'Unknown',
        timezone: str = 'UTC'
    ) -> Dict:
        """Calculate equal house cusps as fallback (30 degrees each)."""
        seed = self._create_seed(birth_date, birth_time, birth_location)
        ascendant_sign = self._calculate_ascendant(birth_date, birth_time, seed)
        ascendant_degree = (seed * 30) % 30

        # Convert to longitude
        sign_degrees = self.zodiac_signs.index(ascendant_sign) * 30
        ascendant_longitude = sign_degrees + ascendant_degree

        houses = {}
        for i in range(1, 13):
            cusp_longitude = (ascendant_longitude + (i - 1) * 30) % 360
            sign_index = int(cusp_longitude / 30) % 12
            sign = self.zodiac_signs[sign_index]
            degree = cusp_longitude % 30

            houses[i] = {
                'cusp': round(degree, 2),
                'sign': sign,
                'longitude': round(cusp_longitude, 2)
            }

        return houses

    def calculate_natal_wheel_data(
        self,
        birth_date: date,
        birth_time: Optional[str] = None,
        birth_location: str = 'Unknown',
        timezone: str = 'UTC'
    ) -> Dict:
        """
        Calculate complete natal wheel data for D3.js rendering.

        Returns:
            Dictionary with planets, houses, and aspects
        """
        # Calculate natal chart
        natal_chart = self.calculate_natal_chart(
            birth_date, birth_time, birth_location, timezone
        )

        # Calculate houses
        houses = self.calculate_placidus_houses(
            birth_date, birth_time, birth_location, timezone
        )

        # Calculate aspects between planets
        aspects = self._calculate_aspects(natal_chart['chart_data'])

        # Get planet symbols
        planet_symbols = {
            'sun': '☉',
            'moon': '☽',
            'mercury': '☿',
            'venus': '♀',
            'mars': '♂',
            'jupiter': '♃',
            'saturn': '♄',
            'uranus': '♅',
            'neptune': '♆',
            'pluto': '♇'
        }

        # Get zodiac symbols
        zodiac_symbols = {
            'Aries': '♈',
            'Taurus': '♉',
            'Gemini': '♊',
            'Cancer': '♋',
            'Leo': '♌',
            'Virgo': '♍',
            'Libra': '♎',
            'Scorpio': '♏',
            'Sagittarius': '♐',
            'Capricorn': '♑',
            'Aquarius': '♒',
            'Pisces': '♓'
        }

        return {
            'planets': natal_chart['chart_data'],
            'planet_symbols': planet_symbols,
            'houses': houses,
            'aspects': aspects,
            'zodiac_symbols': zodiac_symbols,
            'ascendant': natal_chart['ascendant'],
            'sun_sign': natal_chart['sun_sign'],
            'moon_sign': natal_chart['moon_sign']
        }


# Convenience function to get calculator
def get_calculator():
    """
    Get appropriate calculator based on availability.
    Returns MockGCodeCalculator for now, can be switched to real one later.
    """
    try:
        # Try to import PyEphem
        import ephem
        # If successful, you could return the real calculator
        # from .calculator import GCodeCalculator
        # return GCodeCalculator()
    except ImportError:
        pass

    # Fall back to mock calculator
    return MockGCodeCalculator()
