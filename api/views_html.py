"""
HTML Template Views for Spiritual G-Code.
These views render the frontend pages.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.utils import timezone
from datetime import date
from django.http import HttpResponse


@login_required
def dashboard_view(request):
    """Render dashboard page."""
    return render(request, 'dashboard/index.html')


@login_required
def natal_view(request):
    """Render natal chart page."""
    return render(request, 'natal/index.html')


@login_required
def wheel_view(request):
    """Render natal wheel page."""
    return render(request, 'natal/wheel.html')


@login_required
def solar_system_view(request):
    """Render solar system transit visualization page."""
    return render(request, 'solar-system/index.html')


@login_required
def content_view(request):
    """Render content page."""
    return render(request, 'content/index.html')


@login_required
def settings_view(request):
    """Render settings page."""
    return render(request, 'settings/index.html')


def login_view(request):
    """Render login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'auth/login.html')


def logout_view(request):
    """Logout user and redirect to login."""
    logout(request)
    return redirect('login')


def register_view(request):
    """Render registration page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'auth/register.html')


def test_login_view(request):
    """Test login endpoint for development - automatically logs in admin user."""
    user = authenticate(username='admin', password='admin123')
    if user:
        auth_login(request, user)
        return redirect('dashboard')
    return HttpResponse("Failed to authenticate", status=400)
