"""
G-Code Calculator for Spiritual G-Code.
Handles natal chart and transit calculations.
"""

import math
from datetime import date, datetime, timedelta

import ephem
import pytz


class GCodeCalculator:
    """
    Calculator for natal charts and daily transits.
    Uses PyEphem for astronomical calculations.

    Asteroids/centaurs load from JPL SBDB approximate orbital elements
    (epoch 2023-09-13) via ephem.EllipticalBody — visualization-grade
    (±1° position); refine with ephemeris files when sub-degree matters.
    Loud by design: a malformed element set raises instead of silently
    emptying the body list.
    """

    # Visualization radii (AU), including the derived Earth (see
    # calculate_solar_system_transits).
    ORBITAL_RADII = {
        "sun": 0.0,
        "mercury": 0.39,
        "venus": 0.72,
        "earth": 1.0,
        "moon": 1.0,  # rides Earth at this scale
        "mars": 1.52,
        "ceres": 2.77,
        "pallas": 2.77,
        "juno": 2.77,
        "vesta": 2.36,
        "jupiter": 5.2,
        "saturn": 9.58,
        "chiron": 13.7,
        "uranus": 19.2,
        "neptune": 30.05,
        "pluto": 39.48,
    }

    # (a_AU, eccentricity, inclination°, ascending node°, perihelion arg°, mean anomaly°)
    SMALL_BODY_ELEMENTS = {
        "ceres": (2.7663, 0.0794, 10.588, 80.329, 73.725, 6.75),
        "pallas": (2.7728, 0.2303, 34.837, 173.07, 310.35, 62.5),
        "juno": (2.6700, 0.2568, 12.999, 169.85, 248.40, 271.0),
        "vesta": (2.3618, 0.0887, 7.142, 103.81, 151.05, 343.5),
        "chiron": (13.6565, 0.3826, 6.934, 209.30, 339.93, 339.93),
    }

    @staticmethod
    def _make_small_body(name: str, elements: tuple) -> ephem.EllipticalBody:
        """Build one elliptical body from (a, e, i, Ω, ω, M) at the elements epoch."""
        a, e, inc, node, peri, mean = elements
        body = ephem.EllipticalBody()
        body.name = name
        body._a = a
        body._e = e
        body._inc = ephem.degrees(str(inc))
        body._Om = ephem.degrees(str(node))
        body._om = ephem.degrees(str(peri))
        body._M = ephem.degrees(str(mean))
        body._epoch = ephem.Date("2023/09/13")
        return body

    def __init__(self):
        """Initialize calculator with extended celestial bodies."""
        # Classical Planets (10; PyEphem has no Earth ephemeris — you're on it)
        self.planets = {
            "sun": ephem.Sun(),
            "moon": ephem.Moon(),
            "mercury": ephem.Mercury(),
            "venus": ephem.Venus(),
            "mars": ephem.Mars(),
            "jupiter": ephem.Jupiter(),
            "saturn": ephem.Saturn(),
            "uranus": ephem.Uranus(),
            "neptune": ephem.Neptune(),
            "pluto": ephem.Pluto(),
        }

        # Major asteroids + centaur, from explicit elements (loud, not silent).
        self.asteroids = {
            name: self._make_small_body(name, elements)
            for name, elements in self.SMALL_BODY_ELEMENTS.items()
            if name != "chiron"
        }
        self.centaurs = {
            name: self._make_small_body(name, elements)
            for name, elements in self.SMALL_BODY_ELEMENTS.items()
            if name == "chiron"
        }

        # Combine all for iteration
        self.all_celestial_bodies = {**self.planets, **self.asteroids, **self.centaurs}

        # Zodiac signs
        self.zodiac_signs = [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]

    def calculate_natal_chart(
        self,
        birth_date: date,
        birth_time: str | None = None,
        birth_location: str = "Unknown",
        timezone: str = "UTC",
    ) -> dict:
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
                dt = datetime.combine(
                    birth_date, datetime.strptime(birth_time, "%H:%M").time()
                )
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
                # Ecliptic longitude in DEGREES — the zodiac helpers are
                # degree-based; feeding them radians made every sign Aries.
                lon = math.degrees(float(ephem.Ecliptic(planet).lon)) % 360.0
                sign = self._get_zodiac_sign(lon)
                degree = self._get_degree_in_sign(lon)

                chart_data[planet_name] = {
                    "sign": sign,
                    "degree": degree,
                    "longitude": lon,
                }

                if planet_name == "sun":
                    sun_sign = sign
                elif planet_name == "moon":
                    moon_sign = sign

            # Calculate ascendant
            ascendant = self._calculate_ascendant(observer)

            # Calculate dominant elements
            dominant_elements = self._calculate_dominant_elements(chart_data)

            # Calculate key aspects
            key_aspects = self._calculate_aspects(chart_data)

            return {
                "chart_data": chart_data,
                "sun_sign": sun_sign,
                "moon_sign": moon_sign,
                "ascendant": ascendant,
                "dominant_elements": dominant_elements,
                "key_aspects": key_aspects,
            }

        except Exception as e:
            raise Exception(f"Error calculating natal chart: {e!s}")

    def calculate_transits(
        self,
        birth_date: date,
        birth_location: str,
        target_date: date,
        birth_time: str | None = None,
    ) -> dict:
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
                lon = math.degrees(float(ephem.Ecliptic(planet).lon)) % 360.0
                sign = self._get_zodiac_sign(lon)
                degree = self._get_degree_in_sign(lon)

                transit_data[planet_name] = {
                    "sign": sign,
                    "degree": degree,
                    "longitude": float(lon),
                }

            # Calculate aspects to natal positions
            aspects = self._calculate_transit_aspects(
                transit_data, natal_chart["chart_data"]
            )

            return {
                "planets": transit_data,
                "aspects": aspects,
                "natal_chart": natal_chart,
            }

        except Exception as e:
            raise Exception(f"Error calculating transits: {e!s}")

    def _create_observer(self, location: str, dt: datetime) -> ephem.Observer:
        """Create PyEphem observer for location and time."""
        observer = ephem.Observer()

        # For now, use a default location
        # In production, you'd geocode the location string
        observer.lat = "0"  # Default to equator
        observer.lon = "0"  # Default to prime meridian
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
        asc = self._get_zodiac_sign(math.degrees(float(lst)))
        return asc

    def _calculate_dominant_elements(self, chart_data: dict) -> dict:
        """Calculate dominant elements in natal chart."""
        elements = {
            "fire": 0,  # Aries, Leo, Sagittarius
            "earth": 0,  # Taurus, Virgo, Capricorn
            "air": 0,  # Gemini, Libra, Aquarius
            "water": 0,  # Cancer, Scorpio, Pisces
        }

        fire_signs = ["Aries", "Leo", "Sagittarius"]
        earth_signs = ["Taurus", "Virgo", "Capricorn"]
        air_signs = ["Gemini", "Libra", "Aquarius"]
        water_signs = ["Cancer", "Scorpio", "Pisces"]

        for planet_data in chart_data.values():
            sign = planet_data["sign"]
            if sign in fire_signs:
                elements["fire"] += 1
            elif sign in earth_signs:
                elements["earth"] += 1
            elif sign in air_signs:
                elements["air"] += 1
            elif sign in water_signs:
                elements["water"] += 1

        return elements

    def _calculate_aspects(self, chart_data: dict) -> list[dict]:
        """Calculate aspects between planets in natal chart."""
        aspects = []
        planets = list(chart_data.keys())

        aspect_types = {
            "conjunction": 0,
            "opposition": 180,
            "trine": 120,
            "square": 90,
            "sextile": 60,
        }

        for i, p1 in enumerate(planets):
            for p2 in planets[i + 1 :]:
                lon1 = chart_data[p1]["longitude"]
                lon2 = chart_data[p2]["longitude"]
                diff = abs(lon1 - lon2) % 360

                if diff > 180:
                    diff = 360 - diff

                # Check for aspects (with 8 degree orb)
                for aspect_name, aspect_angle in aspect_types.items():
                    if abs(diff - aspect_angle) <= 8:
                        aspects.append(
                            {
                                "planet1": p1,
                                "planet2": p2,
                                "aspect": aspect_name,
                                "orb": abs(diff - aspect_angle),
                            }
                        )

        return aspects

    def _calculate_transit_aspects(
        self, transit_data: dict, natal_data: dict
    ) -> list[dict]:
        """Calculate aspects between transiting and natal planets."""
        aspects = []
        aspect_types = {
            "conjunction": 0,
            "opposition": 180,
            "trine": 120,
            "square": 90,
            "sextile": 60,
        }

        for transit_planet, transit_pos in transit_data.items():
            for natal_planet, natal_pos in natal_data.items():
                diff = abs(transit_pos["longitude"] - natal_pos["longitude"]) % 360

                if diff > 180:
                    diff = 360 - diff

                for aspect_name, aspect_angle in aspect_types.items():
                    if abs(diff - aspect_angle) <= 8:
                        aspects.append(
                            {
                                "transit_planet": transit_planet,
                                "natal_planet": natal_planet,
                                "aspect": aspect_name,
                                "orb": abs(diff - aspect_angle),
                            }
                        )

        return aspects

    def calculate_extended_aspects(
        self, natal_data: dict, transit_data: dict = None
    ) -> dict:
        """
        Calculate extended aspects including asteroids and lunar nodes.

        Args:
            natal_data: Natal chart data
            transit_data: Current transit data (optional)

        Returns:
            Dictionary with all aspect categories
        """
        all_aspects = {
            "natal_aspects": [],  # Between natal planets (classic)
            "asteroid_aspects": [],  # Asteroid-to-asteroid and asteroid-to-natal
            "node_aspects": [],  # Lunar node aspects
            "extended_transit_aspects": [],  # Transit asteroids/nodes to natal
        }

        aspect_types = {
            "conjunction": 0,
            "opposition": 180,
            "trine": 120,
            "square": 90,
            "sextile": 60,
        }

        # Calculate natal aspects with asteroids included
        for body1_name, body1 in self.all_celestial_bodies.items():
            for body2_name, body2 in self.all_celestial_bodies.items():
                if body1_name >= body2_name:  # Avoid duplicates
                    continue

                # Get positions from natal_data
                if body1_name in natal_data and body2_name in natal_data:
                    lon1 = natal_data[body1_name]["longitude"]
                    lon2 = natal_data[body2_name]["longitude"]

                    # Calculate aspect
                    diff = abs(lon1 - lon2) % 360
                    if diff > 180:
                        diff = 360 - diff

                    for aspect_name, aspect_angle in aspect_types.items():
                        if abs(diff - aspect_angle) <= 8:
                            all_aspects["natal_aspects"].append(
                                {
                                    "body1": body1_name,
                                    "body2": body2_name,
                                    "aspect": aspect_name,
                                    "orb": abs(diff - aspect_angle),
                                }
                            )

        # Calculate lunar node aspects to natal
        if natal_data:
            # We'll calculate node positions based on the transit data
            # For now, create a simplified calculation
            node_orb = 6793.5  # 18.6 years
            epoch = date(2000, 1, 1)

            # Get user birth date from somewhere (this would need to be passed in)
            # For now, calculate current node positions
            if transit_data and "lunar_nodes" in transit_data:
                nn_lon = transit_data["lunar_nodes"]["north_node"]["longitude"]
                sn_lon = transit_data["lunar_nodes"]["south_node"]["longitude"]

                # Check node aspects to natal planets
                for natal_planet, natal_pos in natal_data.items():
                    # North Node aspects
                    diff_nn = abs(nn_lon - natal_pos["longitude"]) % 360
                    if diff_nn > 180:
                        diff_nn = 360 - diff_nn

                    for aspect_name, aspect_angle in aspect_types.items():
                        if abs(diff_nn - aspect_angle) <= 8:
                            all_aspects["node_aspects"].append(
                                {
                                    "node": "north_node",
                                    "natal_planet": natal_planet,
                                    "aspect": aspect_name,
                                    "orb": abs(diff_nn - aspect_angle),
                                }
                            )

                    # South Node aspects
                    diff_sn = abs(sn_lon - natal_pos["longitude"]) % 360
                    if diff_sn > 180:
                        diff_sn = 360 - diff_sn

                    for aspect_name, aspect_angle in aspect_types.items():
                        if abs(diff_sn - aspect_angle) <= 8:
                            all_aspects["node_aspects"].append(
                                {
                                    "node": "south_node",
                                    "natal_planet": natal_planet,
                                    "aspect": aspect_name,
                                    "orb": abs(diff_sn - aspect_angle),
                                }
                            )

        return all_aspects

    def calculate_solar_system_transits(self, target_date: date) -> dict:
        """
        Calculate heliocentric positions for all celestial bodies.
        Returns data for D3.js solar system visualization.

        Astronomical notes (Rational Grounding):
        - Earth is DERIVED exactly: Earth's heliocentric longitude is the
          Sun's geocentric longitude + 180° (PyEphem has no Earth ephemeris —
          you're standing on it).
        - The Moon has no heliocentric ephemeris either; it rides Earth's
          orbital radius (they differ by ~0.003 AU — invisible at solar-system
          scale) with its own geocentric ecliptic longitude.
        - Retrograde = the geocentric ecliptic longitude shrinks from today to
          tomorrow (never true for the Sun or Moon, always apparent motion).
        """
        dt = datetime.combine(target_date, datetime.min.time())
        observer = ephem.Observer()
        observer.date = dt
        next_observer = ephem.Observer()
        next_observer.date = dt + timedelta(days=1)

        sun = self.planets["sun"]
        sun.compute(observer)
        sun_geo = math.degrees(float(ephem.Ecliptic(sun).lon)) % 360.0
        earth_helio = (sun_geo + 180.0) % 360.0

        solar_system_data: dict = {
            "date": target_date.isoformat(),
            "bodies": [
                {
                    "name": "sun",
                    "symbol": self._get_planet_symbol("sun"),
                    "category": self._get_celestial_category("sun"),
                    "heliocentric_longitude": 0.0,  # the centre, by definition
                    "geocentric_longitude": sun_geo,
                    "orbital_radius_au": 0.0,
                    "zodiac_sign": self._get_zodiac_sign(sun_geo),
                    "degree_in_sign": float(self._get_degree_in_sign(sun_geo)),
                    "retrograde": False,  # apparent solar motion is always direct
                },
                {
                    # Earth: derived exactly, never stored in self.planets.
                    "name": "earth",
                    "symbol": self._get_planet_symbol("earth"),
                    "category": self._get_celestial_category("earth"),
                    "heliocentric_longitude": earth_helio,
                    "geocentric_longitude": None,  # undefined: the viewpoint itself
                    "orbital_radius_au": self.ORBITAL_RADII["earth"],
                    "zodiac_sign": self._get_zodiac_sign(earth_helio),
                    "degree_in_sign": float(self._get_degree_in_sign(earth_helio)),
                    "retrograde": False,
                },
            ],
        }

        for body_name, body in self.all_celestial_bodies.items():
            if body_name == "sun":
                continue  # emitted above
            body.compute(observer)
            if body_name == "moon":
                helio_lon = earth_helio  # rides Earth at this scale (see docstring)
                geo_lon = math.degrees(float(ephem.Ecliptic(body).lon)) % 360.0
            else:
                helio_lon = math.degrees(float(body.hlong)) % 360.0
                geo_lon = math.degrees(float(ephem.Ecliptic(body).lon)) % 360.0

            # Retrograde: geocentric ecliptic longitude shrinking day-over-day.
            body.compute(next_observer)
            geo_lon_next = math.degrees(float(ephem.Ecliptic(body).lon)) % 360.0
            delta = (geo_lon_next - geo_lon + 180.0) % 360.0 - 180.0
            retrograde = bool(delta < -0.05)  # shrinking; |Δ|<0.05°/day ≈ station

            solar_system_data["bodies"].append(
                {
                    "name": body_name,
                    "symbol": self._get_planet_symbol(body_name),
                    "category": self._get_celestial_category(body_name),
                    "heliocentric_longitude": helio_lon,
                    "geocentric_longitude": geo_lon,
                    "orbital_radius_au": self.ORBITAL_RADII.get(body_name, 1.0),
                    "zodiac_sign": self._get_zodiac_sign(geo_lon),
                    "degree_in_sign": float(self._get_degree_in_sign(geo_lon)),
                    "retrograde": retrograde,
                }
            )

        # Calculate lunar nodes (geocentric)
        lunar_nodes = self.calculate_lunar_nodes(target_date)
        solar_system_data["lunar_nodes"] = lunar_nodes

        return solar_system_data

    def calculate_lunar_nodes(self, target_date: date) -> dict:
        """
        Mean lunar nodes: where the Moon's orbit crosses the ecliptic.

        Standard mean-node formula (Meeus, simplified ch. 47): the ascending
        node regresses 0.0529538°/day from 125.0445° at J2000. Always exactly
        180° apart; both are imaginary points, not bodies.
        """
        jd = ephem.julian_date(datetime.combine(target_date, datetime.min.time()))
        days_since_j2000 = jd - 2451545.0
        north = (125.0445 - 0.0529538 * days_since_j2000) % 360.0
        south = (north + 180.0) % 360.0

        def _node(name: str, symbol: str, longitude: float) -> dict:
            return {
                "name": name,
                "symbol": symbol,
                "longitude": round(longitude, 4),
                "zodiac_sign": self._get_zodiac_sign(longitude),
                "degree_in_sign": float(self._get_degree_in_sign(longitude)),
            }

        return {
            "north_node": _node("north_node", "☊", north),
            "south_node": _node("south_node", "☋", south),
        }

    def _get_planet_symbol(self, body_name: str) -> str:
        """Get astronomical symbol for celestial body."""
        symbols = {
            "sun": "☉",
            "moon": "☽",
            "mercury": "☿",
            "venus": "♀",
            "earth": "🌍",
            "mars": "♂",
            "jupiter": "♃",
            "saturn": "♄",
            "uranus": "♅",
            "neptune": "♆",
            "pluto": "♇",
            "ceres": "⚳",
            "pallas": "⚴",
            "juno": "⚵",
            "vesta": "⚶",
            "chiron": "⚷",
        }
        return symbols.get(body_name, body_name[0].upper())

    def _get_celestial_category(self, body_name: str) -> str:
        """Get category for visualization grouping."""
        categories = {
            "sun": "star",
            "moon": "satellite",
            "mercury": "personal",
            "venus": "personal",
            "earth": "personal",
            "mars": "personal",
            "ceres": "asteroid",
            "pallas": "asteroid",
            "juno": "asteroid",
            "vesta": "asteroid",
            "jupiter": "social",
            "saturn": "social",
            "chiron": "centaur",
            "uranus": "outer",
            "neptune": "outer",
            "pluto": "outer",
        }
        return categories.get(body_name, "unknown")
