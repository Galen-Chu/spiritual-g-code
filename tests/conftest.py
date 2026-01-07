"""
Pytest Configuration for Spiritual G-Code.
"""

import pytest
from datetime import date
from django.utils import timezone
from api.models import GCodeUser, DailyTransit, NatalChart


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = GCodeUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        birth_date=date(1990, 6, 15),
        birth_time='14:30',
        birth_location='Taipei, Taiwan',
        timezone='Asia/Taipei'
    )
    return user


@pytest.fixture
def test_natal_chart(test_user):
    """Create a test natal chart."""
    natal_chart = NatalChart.objects.create(
        user=test_user,
        chart_data={
            'sun': {'sign': 'Gemini', 'degree': 15.5},
            'moon': {'sign': 'Cancer', 'degree': 8.2},
        },
        sun_sign='Gemini',
        moon_sign='Cancer',
        ascendant='Leo',
        dominant_elements={'fire': 2, 'earth': 3, 'air': 4, 'water': 1},
        key_aspects=[]
    )
    return natal_chart


@pytest.fixture
def test_daily_transit(test_user, test_natal_chart):
    """Create a test daily transit."""
    transit = DailyTransit.objects.create(
        user=test_user,
        transit_date=date.today(),
        transit_data={'sun': {'sign': 'Capricorn'}},
        aspects_to_natal=[],
        g_code_score=75,
        themes=['#Transformation', '#Growth'],
        intensity_level='high',
        interpretation='A day of transformation and growth.',
        affirmation='I embrace change with an open heart.',
        practical_guidance=['Stay flexible', 'Trust the process']
    )
    return transit


@pytest.fixture
def authenticated_client(client, test_user):
    """Return an authenticated client."""
    client.force_login(test_user)
    return client
