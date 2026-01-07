"""
API Tests for Spiritual G-Code.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from api.models import GCodeUser, DailyTransit, GeneratedContent


@pytest.mark.django_db
class TestAuthentication:
    """Test authentication endpoints."""

    def test_user_registration(self, client):
        """Test user registration."""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'birth_date': '1990-06-15',
            'birth_time': '14:30',
            'birth_location': 'Taipei, Taiwan',
            'timezone': 'Asia/Taipei'
        }

        response = client.post(url, data, content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['username'] == 'newuser'

    def test_user_registration_password_mismatch(self, client):
        """Test registration with mismatched passwords."""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
            'birth_date': '1990-06-15',
            'birth_location': 'Taipei, Taiwan'
        }

        response = client.post(url, data, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_profile_get(self, authenticated_client):
        """Test getting user profile."""
        url = reverse('profile')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'username' in response.data


@pytest.mark.django_db
class TestDailyTransits:
    """Test daily transit endpoints."""

    def test_get_current_gcode(self, authenticated_client, test_daily_transit):
        """Test getting today's G-Code."""
        url = reverse('daily-transit-current')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['g_code_score'] == 75

    def test_get_weekly_transits(self, authenticated_client, test_daily_transit):
        """Test getting weekly forecast."""
        url = reverse('daily-transit-weekly')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)


@pytest.mark.django_db
class TestGeneratedContent:
    """Test generated content endpoints."""

    def test_list_content(self, authenticated_client):
        """Test listing generated content."""
        url = reverse('generated-content-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDashboard:
    """Test dashboard endpoints."""

    def test_dashboard_overview(self, authenticated_client, test_daily_transit):
        """Test dashboard overview endpoint."""
        url = reverse('dashboard-overview')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'user_stats' in response.data

    def test_dashboard_charts(self, authenticated_client):
        """Test dashboard charts endpoint."""
        url = reverse('dashboard-charts')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
