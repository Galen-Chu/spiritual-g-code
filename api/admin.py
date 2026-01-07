"""
Django Admin Configuration for Spiritual G-Code API.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    GCodeUser,
    NatalChart,
    DailyTransit,
    GeneratedContent,
    GCodeTemplate,
    UserActivity,
    SystemLog,
)


@admin.register(GCodeUser)
class GCodeUserAdmin(admin.ModelAdmin):
    """Admin interface for G-Code Users."""

    list_display = ['username', 'email', 'birth_date', 'daily_gcode_enabled', 'created_at']
    list_filter = ['daily_gcode_enabled', 'preferred_tone', 'created_at']
    search_fields = ['username', 'email', 'birth_location']
    readonly_fields = ['uuid', 'created_at', 'updated_at']

    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'email', 'password')
        }),
        ('Birth Information', {
            'fields': ('birth_date', 'birth_time', 'birth_location', 'birth_lat', 'birth_lng', 'timezone')
        }),
        ('Profile', {
            'fields': ('bio', 'avatar', 'first_name', 'last_name')
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'daily_gcode_enabled', 'preferred_tone')
        }),
        ('Metadata', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NatalChart)
class NatalChartAdmin(admin.ModelAdmin):
    """Admin interface for Natal Charts."""

    list_display = ['user', 'sun_sign', 'moon_sign', 'ascendant', 'calculated_at']
    list_filter = ['sun_sign', 'moon_sign', 'ascendant', 'calculated_at']
    search_fields = ['user__username']
    readonly_fields = ['calculated_at', 'updated_at']


@admin.register(DailyTransit)
class DailyTransitAdmin(admin.ModelAdmin):
    """Admin interface for Daily Transits."""

    list_display = ['user', 'transit_date', 'g_code_score', 'intensity_level', 'created_at']
    list_filter = ['intensity_level', 'transit_date', 'created_at']
    search_fields = ['user__username', 'themes']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'transit_date', 'g_code_score', 'intensity_level')
        }),
        ('Transit Data', {
            'fields': ('transit_data', 'aspects_to_natal')
        }),
        ('Themes & Interpretation', {
            'fields': ('themes', 'interpretation', 'affirmation', 'practical_guidance')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GeneratedContent)
class GeneratedContentAdmin(admin.ModelAdmin):
    """Admin interface for Generated Content."""

    list_display = ['title', 'content_type', 'platform', 'status', 'scheduled_for', 'generated_at']
    list_filter = ['content_type', 'platform', 'status', 'generated_at']
    search_fields = ['title', 'body', 'hashtags']
    readonly_fields = ['generated_at', 'updated_at']

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'related_transit')


@admin.register(GCodeTemplate)
class GCodeTemplateAdmin(admin.ModelAdmin):
    """Admin interface for G-Code Templates."""

    list_display = ['name', 'category', 'is_active', 'version', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin interface for User Activities."""

    list_display = ['user', 'activity_type', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        """Disable manual adding of activities."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing of activities."""
        return False


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    """Admin interface for System Logs."""

    list_display = ['level', 'module', 'function', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['message', 'module', 'function']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        """Disable manual adding of logs."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing of logs."""
        return False


# Customize Admin Site
admin.site.site_header = "Spiritual G-Code Administration"
admin.site.site_title = "G-Code Admin Portal"
admin.site.index_title = "Welcome to the Spiritual G-Code Dashboard"
