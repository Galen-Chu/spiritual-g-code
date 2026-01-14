"""
Database Models for Spiritual G-Code API.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

# Import annotation model
from .annotation import ChartAnnotation



class GCodeUser(AbstractUser):
    """
    Custom User Model for Spiritual G-Code.
    Extends Django's AbstractUser with spiritual/astronomical fields.
    """

    # Birth Information for Natal Chart
    birth_date = models.DateField(help_text="User's birth date")
    birth_time = models.TimeField(
        null=True,
        blank=True,
        help_text="User's birth time (optional but recommended)"
    )
    birth_location = models.CharField(
        max_length=255,
        help_text="Birth location (City, Country or Lat/Long)"
    )
    birth_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude of birth location"
    )
    birth_lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude of birth location"
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="User's timezone"
    )

    # Profile Information
    bio = models.TextField(blank=True, help_text="User's bio or spiritual journey")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Preferences
    email_notifications = models.BooleanField(default=True)
    daily_gcode_enabled = models.BooleanField(
        default=True,
        help_text="Enable automatic Daily G-Code calculations"
    )
    preferred_tone = models.CharField(
        max_length=20,
        choices=[
            ('inspiring', 'Inspiring'),
            ('practical', 'Practical'),
            ('poetic', 'Poetic'),
            ('technical', 'Technical'),
        ],
        default='inspiring',
        help_text="Preferred tone for AI-generated content"
    )

    # Metadata
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gcode_users'
        verbose_name = 'G-Code User'
        verbose_name_plural = 'G-Code Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"@{self.username}"


class NatalChart(models.Model):
    """
    Stores the complete natal chart calculation for a user.
    """

    user = models.OneToOneField(
        GCodeUser,
        on_delete=models.CASCADE,
        related_name='natal_chart'
    )

    # Chart Data (JSON format for flexibility)
    chart_data = models.JSONField(
        help_text="Complete natal chart data including planetary positions"
    )

    # Key Placements
    sun_sign = models.CharField(max_length=20, help_text="Sun sign (e.g., 'Aries')")
    moon_sign = models.CharField(max_length=20, help_text="Moon sign")
    ascendant = models.CharField(
        max_length=20,
        help_text="Rising sign"
    )

    # Dominant Elements
    dominant_elements = models.JSONField(
        help_text="Element distribution (fire, earth, air, water)"
    )

    # Aspects
    key_aspects = models.JSONField(
        help_text="Major planetary aspects"
    )

    # Metadata
    calculated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'natal_charts'
        verbose_name = 'Natal Chart'
        verbose_name_plural = 'Natal Charts'

    def __str__(self):
        return f"Natal Chart for @{self.user.username}"


class DailyTransit(models.Model):
    """
    Daily transit calculations and interpretations.
    Generated automatically at 4:00 AM every day.
    """

    user = models.ForeignKey(
        GCodeUser,
        on_delete=models.CASCADE,
        related_name='daily_transits'
    )

    # Date
    transit_date = models.DateField(help_text="Date of the transit")

    # Transit Data
    transit_data = models.JSONField(
        help_text="Current planetary positions"
    )

    # Aspects to Natal
    aspects_to_natal = models.JSONField(
        help_text="Aspects between current transits and natal chart"
    )

    # G-Code Score (1-100)
    g_code_score = models.IntegerField(
        help_text="Daily G-Code intensity score (1-100)"
    )

    # Themes & Interpretation
    themes = models.JSONField(
        help_text="Key themes for the day (as array of hashtags)"
    )

    intensity_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('intense', 'Intense'),
        ],
        help_text="Intensity level of the day"
    )

    # AI Interpretation
    interpretation = models.TextField(
        help_text="AI-generated interpretation of the day's transits"
    )

    affirmation = models.TextField(
        help_text="Daily affirmation generated by AI"
    )

    practical_guidance = models.JSONField(
        help_text="Array of practical guidance tips"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_transits'
        verbose_name = 'Daily Transit'
        verbose_name_plural = 'Daily Transits'
        unique_together = ['user', 'transit_date']
        ordering = ['-transit_date']

    def __str__(self):
        return f"{self.user.username}'s G-Code for {self.transit_date}"


class GeneratedContent(models.Model):
    """
    AI-generated content for social media and other platforms.
    """

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('posted', 'Posted'),
        ('scheduled', 'Scheduled'),
        ('failed', 'Failed'),
    ]

    PLATFORM_CHOICES = [
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('facebook', 'Facebook'),
        ('blog', 'Blog'),
        ('email', 'Email Newsletter'),
    ]

    CONTENT_TYPE_CHOICES = [
        ('patch_note', 'Spiritual Patch Note'),
        ('insight', 'Daily Insight'),
        ('horoscope', 'Horoscope'),
        ('educational', 'Educational Content'),
        ('affirmation', 'Affirmation'),
        ('retrograde', 'Retrograde Alert'),
    ]

    user = models.ForeignKey(
        GCodeUser,
        on_delete=models.CASCADE,
        related_name='generated_content',
        null=True,
        blank=True
    )

    # Content Information
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        help_text="Type of generated content"
    )

    title = models.CharField(max_length=200)
    body = models.TextField(help_text="Generated content body")

    # Social Media Specific
    hashtags = models.JSONField(
        help_text="Array of hashtags",
        null=True,
        blank=True
    )

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        help_text="Target platform"
    )

    # Status & Scheduling
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    scheduled_for = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Scheduled posting time"
    )

    posted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Actual posting time"
    )

    # Related Data
    related_transit = models.ForeignKey(
        DailyTransit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_content'
    )

    # Metadata
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'generated_content'
        verbose_name = 'Generated Content'
        verbose_name_plural = 'Generated Content'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.content_type}: {self.title}"


class GCodeTemplate(models.Model):
    """
    Prompt templates for AI content generation.
    """

    CATEGORY_CHOICES = [
        ('daily', 'Daily G-Code'),
        ('weekly', 'Weekly Forecast'),
        ('monthly', 'Monthly Forecast'),
        ('retrograde', 'Retrograde'),
        ('eclipse', 'Eclipse'),
        ('full_moon', 'Full Moon'),
        ('new_moon', 'New Moon'),
        ('educational', 'Educational'),
    ]

    # Template Information
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    # Template Content
    prompt_template = models.TextField(
        help_text="Prompt template with {variable} placeholders"
    )

    variables = models.JSONField(
        help_text="Array of variables used in the template",
        null=True,
        blank=True
    )

    # Example Output (for documentation)
    example_output = models.TextField(
        blank=True,
        help_text="Example of generated output"
    )

    # Status
    is_active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gcode_templates'
        verbose_name = 'G-Code Template'
        verbose_name_plural = 'G-Code Templates'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category}: {self.name}"


class UserActivity(models.Model):
    """
    Track user activity for analytics and personalization.
    """

    user = models.ForeignKey(
        GCodeUser,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    # Activity Information
    activity_type = models.CharField(
        max_length=50,
        help_text="Type of activity (e.g., 'login', 'view_dashboard', 'generate_content')"
    )

    metadata = models.JSONField(
        help_text="Additional activity data",
        null=True,
        blank=True
    )

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activities'
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.activity_type} at {self.created_at}"


class SystemLog(models.Model):
    """
    System-level logging for monitoring and debugging.
    """

    LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    message = models.TextField()
    module = models.CharField(max_length=100, help_text="Python module that generated the log")
    function = models.CharField(max_length=100, help_text="Function that generated the log")

    # Additional Data
    extra_data = models.JSONField(null=True, blank=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_logs'
        verbose_name = 'System Log'
        verbose_name_plural = 'System Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.level}] {self.module}.{self.function}: {self.message[:50]}"
