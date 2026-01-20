"""
URL Configuration for Spiritual G-Code API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Authentication
    RegisterView,
    UserProfileView,
    # Natal Charts
    NatalChartViewSet,
    # Daily Transits
    DailyTransitViewSet,
    # Generated Content
    GeneratedContentViewSet,
    # Templates
    GCodeTemplateViewSet,
    # Annotations
    ChartAnnotationViewSet,
    # Dashboard
    DashboardOverviewView,
    DashboardChartsView,
    # Natal Wheel
    NatalWheelView,
    # Solar System
    SolarSystemTransitView,
    # Health Check
    HealthCheckView,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'natal', NatalChartViewSet, basename='natal-chart')
router.register(r'gcode', DailyTransitViewSet, basename='daily-transit')
router.register(r'content', GeneratedContentViewSet, basename='generated-content')
router.register(r'templates', GCodeTemplateViewSet, basename='gcode-template')
router.register(r'annotations', ChartAnnotationViewSet, basename='chart-annotation')

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),

    # Dashboard
    path('dashboard/overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('dashboard/charts/', DashboardChartsView.as_view(), name='dashboard-charts'),

    # Natal Wheel
    path('natal/wheel/', NatalWheelView.as_view(), name='natal-wheel'),

    # Solar System
    path('solar-system/transits/', SolarSystemTransitView.as_view(), name='solar-system-transits'),

    # ViewSet Routes
    path('', include(router.urls)),

    # Health Check
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
