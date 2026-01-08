"""
URL configuration for Spiritual G-Code project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from api.views_html import (
    dashboard_view,
    natal_view,
    content_view,
    settings_view,
    login_view,
    register_view,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Frontend Pages
    path('', dashboard_view, name='dashboard'),
    path('natal/', natal_view, name='natal'),
    path('content/', content_view, name='content'),
    path('settings/', settings_view, name='settings'),
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),

    # API
    path('api/auth/', include('rest_framework_simplejwt.urls')),
    path('api/', include('api.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Health Check
    path('api/health/', include('health_check.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin Site Configuration
admin.site.site_header = 'Spiritual G-Code Administration'
admin.site.site_title = 'G-Code Admin'
admin.site.index_title = 'Welcome to Spiritual G-Code Administration'
