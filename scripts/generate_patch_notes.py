"""
Content Generation Script

This script generates "Spiritual Patch Notes" for users' social media.
Triggered by Crontab at 5:00 AM daily (after G-Code calculations).
"""

import os
import sys
import django
from datetime import date

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from api.models import User, DailyTransit, GeneratedContent
from ai_engine.gemini_client import GeminiGCodeClient
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_all_patch_notes():
    """
    Generate Spiritual Patch Notes for all users with enabled auto-generation.
    """
    logger.info("Starting content generation...")

    try:
        ai_client = GeminiGCodeClient()
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {str(e)}")
        return

    # Get today's date
    today = date.today()

    # Get users who want auto-generated content
    users = User.objects.filter(
        daily_gcode_enabled=True,
        is_active=True,
        email_notifications=True
    )

    logger.info(f"Generating content for {users.count()} users...")

    success_count = 0
    error_count = 0

    for user in users:
        try:
            # Get today's G-Code
            try:
                transit = DailyTransit.objects.get(
                    user=user,
                    transit_date=today
                )
            except DailyTransit.DoesNotExist:
                logger.warning(f"No Daily G-Code found for {user.username}, skipping...")
                continue

            logger.info(f"Generating content for {user.username}...")

            # Generate Twitter patch note
            try:
                twitter_content = ai_client.generate_spiritual_patch_note(
                    daily_gcode={
                        'themes': transit.themes,
                        'g_code_score': transit.g_code_score,
                        'interpretation': transit.interpretation,
                        'transit_date': today
                    },
                    platform='twitter'
                )

                GeneratedContent.objects.create(
                    user=user,
                    related_transit=transit,
                    status='generated',
                    **twitter_content
                )

                logger.info(f"✅ Generated Twitter content for {user.username}")
                success_count += 1

            except Exception as e:
                logger.error(f"Error generating Twitter content for {user.username}: {str(e)}")
                error_count += 1

            # Generate Instagram content (optional)
            try:
                instagram_content = ai_client.generate_spiritual_patch_note(
                    daily_gcode={
                        'themes': transit.themes,
                        'g_code_score': transit.g_code_score,
                        'interpretation': transit.interpretation,
                        'transit_date': today
                    },
                    platform='instagram'
                )

                GeneratedContent.objects.create(
                    user=user,
                    related_transit=transit,
                    status='generated',
                    **instagram_content
                )

                logger.info(f"✅ Generated Instagram content for {user.username}")

            except Exception as e:
                logger.error(f"Error generating Instagram content for {user.username}: {str(e)}")

        except Exception as e:
            logger.error(f"❌ Error processing {user.username}: {str(e)}")
            error_count += 1
            continue

    # Summary
    logger.info("=" * 50)
    logger.info(f"Content generation complete!")
    logger.info(f"Success: {success_count}")
    logger.info(f"Errors: {error_count}")
    logger.info("=" * 50)


if __name__ == '__main__':
    generate_all_patch_notes()
