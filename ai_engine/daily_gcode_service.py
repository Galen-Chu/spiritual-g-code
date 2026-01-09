"""
Daily G-Code Service for Spiritual G-Code.
Orchestrates natal chart calculation, transit calculation, and AI interpretation.
"""

from datetime import date, datetime, timedelta
from typing import Dict, Optional
from django.utils import timezone

from .mock_calculator import MockGCodeCalculator
from .mock_gemini_client import MockGeminiGCodeClient


class DailyGCodeService:
    """
    Service for calculating and interpreting daily G-Code.
    """

    def __init__(self):
        """Initialize the service with calculator and AI client."""
        self.calculator = MockGCodeCalculator()
        self.ai_client = MockGeminiGCodeClient()

    def calculate_daily_gcode_for_user(
        self,
        user,
        target_date: Optional[date] = None
    ) -> Dict:
        """
        Calculate complete daily G-Code for a user.

        Args:
            user: GCodeUser instance
            target_date: Date to calculate for (defaults to today)

        Returns:
            Complete daily G-Code data with interpretation
        """
        if target_date is None:
            target_date = date.today()

        try:
            # Step 1: Calculate natal chart (cached)
            natal_chart = self._get_or_calculate_natal_chart(user)

            # Step 2: Calculate transits for target date
            transit_data = self.calculator.calculate_transits(
                birth_date=user.birth_date,
                birth_time=user.birth_time.strftime('%H:%M') if user.birth_time else None,
                birth_location=user.birth_location,
                target_date=target_date
            )

            # Step 3: Calculate G-Code intensity score
            g_code_score = self.calculator.calculate_g_code_intensity(
                transit_data=transit_data['planets'],
                aspects=transit_data['aspects']
            )

            # Step 4: Generate AI interpretation
            user_preferences = {
                'tone': user.preferred_tone,
                'timezone': user.timezone
            }

            ai_interpretation = self.ai_client.generate_daily_gcode(
                natal_data=natal_chart,
                transit_data=transit_data,
                user_preferences=user_preferences
            )

            # Step 5: Determine intensity level
            intensity_level = self._get_intensity_level(g_code_score)

            # Step 6: Compile complete daily G-Code
            daily_gcode = {
                'user': user.username,
                'transit_date': target_date,
                'natal_chart': natal_chart,
                'transit_data': transit_data,
                'g_code_score': g_code_score,
                'intensity_level': intensity_level,
                'themes': ai_interpretation['themes'],
                'interpretation': ai_interpretation['interpretation'],
                'affirmation': ai_interpretation['affirmation'],
                'practical_guidance': ai_interpretation['practical_guidance'],
                'generated_at': timezone.now().isoformat(),
            }

            return daily_gcode

        except Exception as e:
            raise Exception(f"Error calculating daily G-Code: {str(e)}")

    def calculate_weekly_forecast(
        self,
        user,
        start_date: Optional[date] = None
    ) -> Dict:
        """
        Calculate weekly G-Code forecast.

        Args:
            user: GCodeUser instance
            start_date: Start date of forecast (defaults to today)

        Returns:
            Weekly forecast with daily G-Codes
        """
        if start_date is None:
            start_date = date.today()

        weekly_data = {
            'user': user.username,
            'start_date': start_date,
            'end_date': start_date.strftime('%Y-%m-%d'),
            'daily_gcodes': []
        }

        # Calculate for 7 days
        for i in range(7):
            target_date = start_date + timedelta(days=i)
            daily_gcode = self.calculate_daily_gcode_for_user(
                user=user,
                target_date=target_date
            )
            weekly_data['daily_gcodes'].append(daily_gcode)

        return weekly_data

    def generate_spiritual_patch_note(
        self,
        daily_gcode: Dict,
        platform: str = 'twitter',
        custom_instructions: str = ''
    ) -> Dict:
        """
        Generate social media content from daily G-Code.

        Args:
            daily_gcode: Daily G-Code data
            platform: Target platform
            custom_instructions: Additional instructions

        Returns:
            Generated content for social media
        """
        return self.ai_client.generate_spiritual_patch_note(
            daily_gcode=daily_gcode,
            platform=platform,
            custom_instructions=custom_instructions
        )

    def _get_or_calculate_natal_chart(self, user) -> Dict:
        """Get cached natal chart or calculate if not exists."""
        from api.models import NatalChart

        try:
            natal_chart = NatalChart.objects.get(user=user)
            return {
                'sun_sign': natal_chart.sun_sign,
                'moon_sign': natal_chart.moon_sign,
                'ascendant': natal_chart.ascendant,
                'dominant_elements': natal_chart.dominant_elements,
                'key_aspects': natal_chart.key_aspects,
                'chart_data': natal_chart.chart_data
            }
        except NatalChart.DoesNotExist:
            # Calculate natal chart
            natal_data = self.calculator.calculate_natal_chart(
                birth_date=user.birth_date,
                birth_time=user.birth_time.strftime('%H:%M') if user.birth_time else None,
                birth_location=user.birth_location,
                timezone=user.timezone
            )

            # Save to database
            NatalChart.objects.create(
                user=user,
                chart_data=natal_data['chart_data'],
                sun_sign=natal_data['sun_sign'],
                moon_sign=natal_data['moon_sign'],
                ascendant=natal_data['ascendant'],
                dominant_elements=natal_data['dominant_elements'],
                key_aspects=natal_data['key_aspects']
            )

            return natal_data

    def _get_intensity_level(self, score: int) -> str:
        """Convert numeric score to intensity level."""
        if score < 25:
            return 'low'
        elif score < 50:
            return 'medium'
        elif score < 75:
            return 'high'
        else:
            return 'intense'


# Singleton instance
_service_instance = None


def get_daily_gcode_service() -> DailyGCodeService:
    """Get or create the daily G-Code service instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = DailyGCodeService()
    return _service_instance
