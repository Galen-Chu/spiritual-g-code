"""
Custom Filters for Spiritual G-Code API.
"""

from django_filters import rest_framework as filters
from .models import DailyTransit, GeneratedContent, GCodeTemplate


# Choice constants (matching model field definitions)
INTENSITY_LEVEL_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('intense', 'Intense'),
]

CONTENT_TYPE_CHOICES = [
    ('patch_note', 'Patch Note'),
    ('insight', 'Daily Insight'),
    ('affirmation', 'Affirmation'),
]

PLATFORM_CHOICES = [
    ('twitter', 'Twitter'),
    ('instagram', 'Instagram'),
    ('linkedin', 'LinkedIn'),
]

STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('generated', 'Generated'),
    ('posted', 'Posted'),
]

CATEGORY_CHOICES = [
    ('daily_gcode', 'Daily G-Code'),
    ('patch_note', 'Patch Note'),
    ('natal', 'Natal Reading'),
    ('transit', 'Transit Analysis'),
]


class DailyTransitFilter(filters.FilterSet):
    """Filter for DailyTransit model."""

    transit_date = filters.DateFilter(field_name='transit_date')
    transit_date_after = filters.DateFilter(field_name='transit_date', lookup_expr='gte')
    transit_date_before = filters.DateFilter(field_name='transit_date', lookup_expr='lte')
    g_code_score_min = filters.NumberFilter(field_name='g_code_score', lookup_expr='gte')
    g_code_score_max = filters.NumberFilter(field_name='g_code_score', lookup_expr='lte')
    intensity_level = filters.ChoiceFilter(choices=INTENSITY_LEVEL_CHOICES)

    class Meta:
        model = DailyTransit
        fields = [
            'transit_date',
            'transit_date_after',
            'transit_date_before',
            'g_code_score_min',
            'g_code_score_max',
            'intensity_level',
        ]


class GeneratedContentFilter(filters.FilterSet):
    """Filter for GeneratedContent model."""

    content_type = filters.ChoiceFilter(choices=CONTENT_TYPE_CHOICES)
    platform = filters.ChoiceFilter(choices=PLATFORM_CHOICES)
    status = filters.ChoiceFilter(choices=STATUS_CHOICES)
    generated_after = filters.DateTimeFilter(field_name='generated_at', lookup_expr='gte')
    generated_before = filters.DateTimeFilter(field_name='generated_at', lookup_expr='lte')

    class Meta:
        model = GeneratedContent
        fields = [
            'content_type',
            'platform',
            'status',
            'generated_after',
            'generated_before',
        ]


class GCodeTemplateFilter(filters.FilterSet):
    """Filter for GCodeTemplate model."""

    category = filters.ChoiceFilter(choices=CATEGORY_CHOICES)
    is_active = filters.BooleanFilter()

    class Meta:
        model = GCodeTemplate
        fields = ['category', 'is_active']
