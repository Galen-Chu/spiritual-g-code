"""
Calculator Tests for Spiritual G-Code.
"""

import pytest
from datetime import date
from ai_engine.calculator import GCodeCalculator


@pytest.mark.django_db
class TestGCodeCalculator:
    """Test G-Code calculator."""

    @pytest.fixture
    def calculator(self):
        """Return calculator instance."""
        return GCodeCalculator()

    def test_calculate_natal_chart(self, calculator):
        """Test natal chart calculation."""
        result = calculator.calculate_natal_chart(
            birth_date=date(1990, 6, 15),
            birth_time='14:30',
            birth_location='Taipei, Taiwan',
            timezone='Asia/Taipei'
        )

        assert 'chart_data' in result
        assert 'sun_sign' in result
        assert 'moon_sign' in result
        assert 'ascendant' in result
        assert 'dominant_elements' in result
        assert 'key_aspects' in result

    def test_calculate_transits(self, calculator):
        """Test transit calculation."""
        result = calculator.calculate_transits(
            birth_date=date(1990, 6, 15),
            birth_time='14:30',
            birth_location='Taipei, Taiwan',
            target_date=date.today()
        )

        assert 'planets' in result
        assert 'aspects' in result
        assert 'natal_chart' in result

    def test_get_zodiac_sign(self, calculator):
        """Test zodiac sign calculation."""
        assert calculator._get_zodiac_sign(0) == 'Aries'
        assert calculator._get_zodiac_sign(30) == 'Taurus'
        assert calculator._get_zodiac_sign(60) == 'Gemini'

    def test_calculate_dominant_elements(self, calculator):
        """Test dominant element calculation."""
        chart_data = {
            'sun': {'sign': 'Aries'},  # Fire
            'moon': {'sign': 'Leo'},   # Fire
            'mercury': {'sign': 'Gemini'},  # Air
        }

        elements = calculator._calculate_dominant_elements(chart_data)

        assert elements['fire'] == 2
        assert elements['air'] == 1
