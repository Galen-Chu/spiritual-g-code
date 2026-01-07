"""
Daily G-Code Calculation Script

This script is triggered by Crontab at 4:00 AM daily to calculate
Daily G-Code for all users with daily_gcode_enabled=True.
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from api.models import User, DailyTransit, NatalChart
from ai_engine.calculator import GCodeCalculator
from ai_engine.gemini_client import GeminiGCodeClient
from django.core import mail
from django.conf import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def calculate_all_daily_gcodes():
    """
    Calculate G-Code for all users with daily_gcode_enabled=True.
    """
    logger.info("Starting Daily G-Code calculation...")

    calculator = GCodeCalculator()

    try:
        ai_client = GeminiGCodeClient()
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {str(e)}")
        ai_client = None

    # Get tomorrow's date (for next day's G-Code)
    tomorrow = date.today() + timedelta(days=1)

    # Get all users with daily G-Code enabled
    users = User.objects.filter(
        daily_gcode_enabled=True,
        is_active=True
    )

    logger.info(f"Processing {users.count()} users...")

    success_count = 0
    error_count = 0

    for user in users:
        try:
            logger.info(f"Processing user: {user.username}")

            # 1. Get or create natal chart
            try:
                natal_chart = user.natal_chart
            except NatalChart.DoesNotExist:
                logger.warning(f"No natal chart found for {user.username}, skipping...")
                continue

            # 2. Calculate planetary transits
            logger.info(f"Calculating transits for {user.username}...")
            transit_data = calculator.calculate_transits(
                birth_date=user.birth_date,
                birth_time=user.birth_time.strftime('%H:%M') if user.birth_time else None,
                birth_location=user.birth_location,
                target_date=tomorrow
            )

            # 3. Generate AI interpretation (if available)
            if ai_client:
                logger.info(f"Generating AI interpretation for {user.username}...")
                gcode_interpretation = ai_client.generate_daily_gcode(
                    natal_data={
                        'sun_sign': natal_chart.sun_sign,
                        'moon_sign': natal_chart.moon_sign,
                        'ascendant': natal_chart.ascendant
                    },
                    transit_data=transit_data,
                    user_preferences={
                        'tone': user.preferred_tone
                    }
                )

                interpretation = gcode_interpretation.get('interpretation', '')
                themes = gcode_interpretation.get('themes', [])
                affirmation = gcode_interpretation.get('affirmation', '')
                practical_guidance = gcode_interpretation.get('practical_guidance', [])
                g_code_score = gcode_interpretation.get('g_code_score', 50)
            else:
                # Fallback without AI
                logger.warning("Using fallback interpretation (no AI available)")
                interpretation = "Cosmic energies are shifting. Stay aligned with your intentions."
                themes = ["#SpiritualGCode", "#DailyGCode"]
                affirmation = "I am aligned with cosmic energies."
                practical_guidance = ["Stay present", "Trust the process"]
                g_code_score = 50

            # 4. Determine intensity level
            intensity_level = 'medium'
            if g_code_score >= 80:
                intensity_level = 'intense'
            elif g_code_score >= 60:
                intensity_level = 'high'
            elif g_code_score < 40:
                intensity_level = 'low'

            # 5. Save or update daily transit
            daily_transit, created = DailyTransit.objects.update_or_create(
                user=user,
                transit_date=tomorrow,
                defaults={
                    'transit_data': transit_data.get('planets', {}),
                    'aspects_to_natal': transit_data.get('aspects', []),
                    'g_code_score': g_code_score,
                    'themes': themes,
                    'intensity_level': intensity_level,
                    'interpretation': interpretation,
                    'affirmation': affirmation,
                    'practical_guidance': practical_guidance,
                }
            )

            if created:
                logger.info(f"✅ Created Daily G-Code for {user.username}")
                success_count += 1
            else:
                logger.info(f"✅ Updated Daily G-Code for {user.username}")
                success_count += 1

        except Exception as e:
            logger.error(f"❌ Error processing {user.username}: {str(e)}")
            error_count += 1
            continue

    # Summary
    logger.info("=" * 50)
    logger.info(f"Daily G-Code calculation complete!")
    logger.info(f"Success: {success_count}")
    logger.info(f"Errors: {error_count}")
    logger.info("=" * 50)

    # Send summary email if configured
    if settings.EMAIL_BACKEND and error_count > 0:
        send_error_summary(error_count)


def send_error_summary(error_count):
    """Send error summary email to admin."""
    subject = f"Daily G-Code Calculation: {error_count} Errors"
    message = f"Daily G-Code calculation completed with {error_count} errors."

    mail.send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMINS[0][1]] if settings.ADMINS else []
    )


if __name__ == '__main__':
    calculate_all_daily_gcodes()
