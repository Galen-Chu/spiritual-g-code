"""
Django REST Framework Serializers for Spiritual G-Code API.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    NatalChart,
    DailyTransit,
    GeneratedContent,
    GCodeTemplate,
    UserActivity,
)
from .annotation import ChartAnnotation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for GCodeUser model."""

    full_name = serializers.SerializerMethodField()
    natal_chart_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'uuid',
            'username',
            'email',
            'full_name',
            'birth_date',
            'birth_time',
            'birth_location',
            'timezone',
            'bio',
            'avatar',
            'email_notifications',
            'daily_gcode_enabled',
            'preferred_tone',
            'natal_chart_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'uuid', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_full_name(self, obj):
        """Get user's full name."""
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_natal_chart_url(self, obj):
        """Get URL to user's natal chart if exists."""
        try:
            return obj.natal_chart.get_absolute_url()
        except:
            return None

    def validate_birth_date(self, value):
        """Ensure birth date is not in the future."""
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError(
                "Birth date cannot be in the future."
            )
        return value

    def validate_birth_location(self, value):
        """Ensure birth location is provided."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Birth location is required."
            )
        return value

    def update(self, instance, validated_data):
        """Update user and recalculate natal chart if birth data changed."""
        from .models import NatalChart, UserActivity
        import logging

        # Check if birth data changed
        birth_data_changed = (
            ('birth_date' in validated_data and validated_data['birth_date'] != instance.birth_date) or
            ('birth_time' in validated_data and validated_data['birth_time'] != instance.birth_time) or
            ('birth_location' in validated_data and validated_data['birth_location'] != instance.birth_location) or
            ('timezone' in validated_data and validated_data['timezone'] != instance.timezone)
        )

        # Store old data for logging
        old_data = {
            'birth_date': str(instance.birth_date),
            'birth_time': str(instance.birth_time) if instance.birth_time else None,
            'birth_location': instance.birth_location,
            'timezone': instance.timezone
        }

        # Update user instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Recalculate natal chart if birth data changed
        if birth_data_changed:
            try:
                from ai_engine.mock_calculator import MockGCodeCalculator
                calculator = MockGCodeCalculator()

                new_chart_data = calculator.calculate_natal_chart(
                    birth_date=instance.birth_date,
                    birth_time=instance.birth_time.strftime('%H:%M') if instance.birth_time else None,
                    birth_location=instance.birth_location,
                    timezone=instance.timezone
                )

                # Update or create natal chart
                NatalChart.objects.update_or_create(
                    user=instance,
                    defaults=new_chart_data
                )

                # Log activity
                UserActivity.objects.create(
                    user=instance,
                    activity_type='birth_data_updated',
                    metadata={
                        'old_data': old_data,
                        'new_data': {
                            'birth_date': str(instance.birth_date),
                            'birth_location': instance.birth_location
                        }
                    }
                )

            except Exception as e:
                logging.getLogger(__name__).error(
                    f"Failed to recalculate natal chart: {str(e)}"
                )

        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'birth_date',
            'birth_time',
            'birth_location',
            'timezone',
            'preferred_tone',
        ]

    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """Create new user."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user


class NatalChartSerializer(serializers.ModelSerializer):
    """Serializer for NatalChart model."""

    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = NatalChart
        fields = [
            'id',
            'user',
            'user_username',
            'chart_data',
            'sun_sign',
            'moon_sign',
            'ascendant',
            'dominant_elements',
            'key_aspects',
            'calculated_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'calculated_at', 'updated_at']


class DailyTransitSerializer(serializers.ModelSerializer):
    """Serializer for DailyTransit model."""

    user_username = serializers.CharField(source='user.username', read_only=True)
    themes_formatted = serializers.SerializerMethodField()

    class Meta:
        model = DailyTransit
        fields = [
            'id',
            'user',
            'user_username',
            'transit_date',
            'transit_data',
            'aspects_to_natal',
            'g_code_score',
            'themes',
            'themes_formatted',
            'intensity_level',
            'interpretation',
            'affirmation',
            'practical_guidance',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_themes_formatted(self, obj):
        """Format themes as string."""
        return ' '.join(obj.themes) if obj.themes else ''


class GeneratedContentSerializer(serializers.ModelSerializer):
    """Serializer for GeneratedContent model."""

    user_username = serializers.CharField(source='user.username', read_only=True)
    hashtags_formatted = serializers.SerializerMethodField()

    class Meta:
        model = GeneratedContent
        fields = [
            'id',
            'user',
            'user_username',
            'content_type',
            'title',
            'body',
            'hashtags',
            'hashtags_formatted',
            'platform',
            'status',
            'scheduled_for',
            'posted_at',
            'related_transit',
            'generated_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'generated_at', 'updated_at']

    def get_hashtags_formatted(self, obj):
        """Format hashtags as string."""
        return ' '.join(obj.hashtags) if obj.hashtags else ''


class GenerateContentSerializer(serializers.Serializer):
    """Serializer for content generation requests."""

    content_type = serializers.ChoiceField(choices=GeneratedContent.CONTENT_TYPE_CHOICES)
    platform = serializers.ChoiceField(choices=GeneratedContent.PLATFORM_CHOICES)
    transit_date = serializers.DateField(required=False)
    custom_instructions = serializers.CharField(required=False, allow_blank=True)

    def validate_transit_date(self, value):
        """Validate transit date is not in the future (for most content types)."""
        from django.utils import timezone
        from datetime import date

        if value and value > date.today():
            raise serializers.ValidationError(
                "Transit date cannot be in the future for most content types."
            )
        return value


class GCodeTemplateSerializer(serializers.ModelSerializer):
    """Serializer for GCodeTemplate model."""

    class Meta:
        model = GCodeTemplate
        fields = [
            'id',
            'name',
            'category',
            'description',
            'prompt_template',
            'variables',
            'example_output',
            'is_active',
            'version',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for UserActivity model."""

    class Meta:
        model = UserActivity
        fields = [
            'id',
            'user',
            'activity_type',
            'metadata',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DashboardOverviewSerializer(serializers.Serializer):
    """Serializer for dashboard overview data."""

    today_gcode = DailyTransitSerializer(read_only=True)
    weekly_transits = DailyTransitSerializer(many=True, read_only=True)
    recent_content = GeneratedContentSerializer(many=True, read_only=True)
    user_stats = serializers.DictField(read_only=True)


class NatalChartCalculationSerializer(serializers.Serializer):
    """Serializer for natal chart calculation requests."""

    birth_date = serializers.DateField()
    birth_time = serializers.TimeField(required=False, allow_null=True)
    birth_location = serializers.CharField(max_length=255)
    timezone = serializers.CharField(max_length=50, default='UTC')


class ChartAnnotationSerializer(serializers.ModelSerializer):
    """Serializer for ChartAnnotation model."""

    username = serializers.CharField(source='user.username', read_only=True)
    data_point_display = serializers.ReadOnlyField()
    chart_type_display = serializers.CharField(source='get_chart_type_display', read_only=True)

    class Meta:
        model = ChartAnnotation
        fields = [
            'id',
            'user',
            'username',
            'chart_type',
            'chart_type_display',
            'data_point',
            'data_point_display',
            'note',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
