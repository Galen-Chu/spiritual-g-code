"""
HTML Template Views for Spiritual G-Code.
These views render the frontend pages.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date


@login_required
def dashboard_view(request):
    """Render dashboard page."""
    return render(request, 'dashboard/index.html')


@login_required
def natal_view(request):
    """Render natal chart page."""
    return render(request, 'natal/index.html')


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


def register_view(request):
    """Render registration page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'auth/register.html')
