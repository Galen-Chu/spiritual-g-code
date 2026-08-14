"""
Data Cleanup Script

This script removes old transits and logs to keep the database lean.
Runs weekly on Sundays at 3:00 AM.
"""

import os
import sys
from datetime import date, timedelta

import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

import logging

from api.models import DailyTransit, SystemLog, UserActivity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def cleanup_old_transits(days_to_keep=90):
    """
    Delete old daily transits beyond the retention period.

    Args:
        days_to_keep: Number of days to retain (default: 90)
    """
    logger.info(f"Cleaning up transits older than {days_to_keep} days...")

    cutoff_date = date.today() - timedelta(days=days_to_keep)

    deleted_count = DailyTransit.objects.filter(
        transit_date__lt=cutoff_date
    ).delete()[0]

    logger.info(f"✅ Deleted {deleted_count} old transit records")


def cleanup_old_logs(days_to_keep=30):
    """
    Delete old system logs.

    Args:
        days_to_keep: Number of days to retain (default: 30)
    """
    logger.info(f"Cleaning up logs older than {days_to_keep} days...")

    cutoff_date = date.today() - timedelta(days=days_to_keep)

    deleted_count = SystemLog.objects.filter(
        created_at__lt=cutoff_date
    ).delete()[0]

    logger.info(f"✅ Deleted {deleted_count} old log records")


def cleanup_old_activities(days_to_keep=90):
    """
    Delete old user activity logs.

    Args:
        days_to_keep: Number of days to retain (default: 90)
    """
    logger.info(f"Cleaning up activities older than {days_to_keep} days...")

    cutoff_date = date.today() - timedelta(days=days_to_keep)

    deleted_count = UserActivity.objects.filter(
        created_at__lt=cutoff_date
    ).delete()[0]

    logger.info(f"✅ Deleted {deleted_count} old activity records")


def run_all_cleanup():
    """Run all cleanup tasks."""
    logger.info("Starting data cleanup...")

    cleanup_old_transits(days_to_keep=90)
    cleanup_old_logs(days_to_keep=30)
    cleanup_old_activities(days_to_keep=90)

    logger.info("=" * 50)
    logger.info("Data cleanup complete!")
    logger.info("=" * 50)


if __name__ == '__main__':
    run_all_cleanup()
