"""
Django Signals for Spiritual G-Code API.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import NatalChart, DailyTransit

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler for User model.
    Creates user-related objects when a new user is registered.
    """
    if created:
        # Log user registration
        from .models import UserActivity
        UserActivity.objects.create(
            user=instance,
            activity_type='user_created'
        )


@receiver(post_save, sender=DailyTransit)
def generate_daily_content(sender, instance, created, **kwargs):
    """
    Automatically generate content when a new daily transit is calculated.
    """
    if created and instance.user.daily_gcode_enabled:
        # This could trigger Celery task for content generation
        pass
