"""Solar system transits (Phase 7): the radians-bug guards, retrograde, nodes.

The real calculator's heliocentric/geocentric longitudes must be DEGREES —
an earlier implementation fed ephem radians into the degree-based zodiac
helpers, which made every body report Aries. These tests pin the degrees
contract through known-astronomy assertions (late-November Sun = Sagittarius).
"""

from datetime import date

import pytest

from ai_engine.calculator import GCodeCalculator
from ai_engine.mock_calculator import MockGCodeCalculator

# Late November 2026: the Sun's geocentric ecliptic longitude is ~245°
# (Sagittarius spans 240-270°). A radians leak would index Aries instead.
KNOWN_DATE = date(2026, 11, 27)


@pytest.mark.unit
class TestRealCalculatorSolarSystem:
    @pytest.fixture
    def result(self) -> dict:
        return GCodeCalculator().calculate_solar_system_transits(KNOWN_DATE)

    def test_sixteen_bodies(self, result):
        names = {b["name"] for b in result["bodies"]}
        assert {
            "sun",
            "earth",
            "moon",
            "ceres",
            "pallas",
            "juno",
            "vesta",
            "chiron",
        } <= names
        assert (
            len(result["bodies"]) == 16
        )  # 10 planets + derived earth + 4 asteroids + chiron

    def test_sun_in_sagittarius_in_late_november(self, result):
        """The degrees-contract guard: radians leak would report Aries here."""
        sun = next(b for b in result["bodies"] if b["name"] == "sun")
        assert sun["zodiac_sign"] == "Sagittarius"
        assert 240.0 <= sun["geocentric_longitude"] <= 250.0

    def test_earth_is_sun_opposite_and_has_no_geocentric_view(self, result):
        sun = next(b for b in result["bodies"] if b["name"] == "sun")
        earth = next(b for b in result["bodies"] if b["name"] == "earth")
        expected = (sun["geocentric_longitude"] + 180.0) % 360.0
        assert abs(earth["heliocentric_longitude"] - expected) < 1e-6
        assert earth["geocentric_longitude"] is None  # the viewpoint itself

    def test_moon_never_retrograde(self, result):
        moon = next(b for b in result["bodies"] if b["name"] == "moon")
        assert moon["retrograde"] is False

    def test_retrograde_flags_are_booleans(self, result):
        for body in result["bodies"]:
            assert isinstance(body["retrograde"], bool), body["name"]

    def test_deterministic(self, result):
        again = GCodeCalculator().calculate_solar_system_transits(KNOWN_DATE)
        assert again == result

    def test_lunar_nodes_exactly_opposite(self, result):
        nodes = result["lunar_nodes"]
        separation = (
            nodes["north_node"]["longitude"] - nodes["south_node"]["longitude"]
        ) % 360.0
        assert abs(separation - 180.0) < 1e-6
        # Mean-node formula recomputed independently (Meeus simplified):
        jd = __import__("ephem").julian_date(
            __import__("datetime").datetime.combine(
                KNOWN_DATE, __import__("datetime").time.min
            )
        )
        expected_north = (125.0445 - 0.0529538 * (jd - 2451545.0)) % 360.0
        assert (
            abs(nodes["north_node"]["longitude"] - expected_north) < 1e-3
        )  # calculator rounds to 4dp


@pytest.mark.unit
class TestMockSolarSystem:
    def test_bodies_and_determinism(self):
        calculator = MockGCodeCalculator()
        result = calculator.calculate_solar_system_transits(KNOWN_DATE)
        assert len(result["bodies"]) == 16
        again = calculator.calculate_solar_system_transits(KNOWN_DATE)
        assert again == result

    def test_retrograde_flags_are_booleans(self):
        result = MockGCodeCalculator().calculate_solar_system_transits(KNOWN_DATE)
        for body in result["bodies"]:
            assert isinstance(body["retrograde"], bool), body["name"]


@pytest.mark.django_db
class TestSolarSystemEndpoint:
    def test_endpoint_serves_all_bodies(self, authenticated_client):
        response = authenticated_client.get("/api/solar-system/transits/")
        assert response.status_code == 200
        assert len(response.data["bodies"]) == 16
        assert response.data["lunar_nodes"]["north_node"]["symbol"] == "☊"

    def test_endpoint_rejects_bad_dates(self, authenticated_client):
        response = authenticated_client.get(
            "/api/solar-system/transits/?date=not-a-date"
        )
        assert response.status_code == 400
