"""
Chart Annotation Model
Allows users to add notes to specific chart data points.
"""

from django.db import models
from django.conf import settings

class ChartAnnotation(models.Model):
    """
    User annotations on chart data points.

    Allows users to add insights, notes, and markers
    to specific points on their G-Code charts.
    """

    # Chart type choices
    CHART_TREND = 'gcode_trend'
    CHART_PLANETARY = 'planetary'
    CHART_ELEMENT = 'element'
    CHART_FORECAST = 'forecast'
    CHART_NETWORK = 'network'

    CHART_TYPE_CHOICES = [
        (CHART_TREND, 'G-Code Trend'),
        (CHART_PLANETARY, 'Planetary Positions'),
        (CHART_ELEMENT, 'Element Distribution'),
        (CHART_FORECAST, 'Weekly Forecast'),
        (CHART_NETWORK, 'Aspects Network'),
    ]

    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='annotations'
    )

    # Target identification
    chart_type = models.CharField(
        max_length=50,
        choices=CHART_TYPE_CHOICES,
        help_text="Type of chart this annotation belongs to"
    )

    data_point = models.JSONField(
        help_text="Data point being annotated (e.g., {'date': '2024-01-15', 'value': 75})"
    )

    # Annotation content
    note = models.TextField(
        help_text="User's note or insight"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chart_annotations'
        verbose_name = 'Chart Annotation'
        verbose_name_plural = 'Chart Annotations'
        # Prevent duplicate annotations for same data point
        unique_together = ['user', 'chart_type', 'data_point']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.chart_type} - {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def data_point_display(self):
        """Human-readable representation of data point"""
        if self.chart_type == self.CHART_TREND:
            date = self.data_point.get('date', 'Unknown')
            value = self.data_point.get('value', 'N/A')
            return f"{date}: G-Code {value}"

        elif self.chart_type == self.CHART_PLANETARY:
            planet = self.data_point.get('planet', 'Unknown')
            sign = self.data_point.get('sign', 'N/A')
            return f"{planet} in {sign}"

        elif self.chart_type == self.CHART_ELEMENT:
            element = self.data_point.get('element', 'Unknown')
            value = self.data_point.get('value', 'N/A')
            return f"{element}: {value}"

        elif self.chart_type == self.CHART_FORECAST:
            date = self.data_point.get('date', 'Unknown')
            value = self.data_point.get('value', 'N/A')
            return f"{date}: Forecast {value}"

        elif self.chart_type == self.CHART_NETWORK:
            planet1 = self.data_point.get('planet1', 'Unknown')
            planet2 = self.data_point.get('planet2', 'Unknown')
            return f"{planet1} aspect {planet2}"

        return str(self.data_point)
