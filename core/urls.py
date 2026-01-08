"""
URL configuration for Spiritual G-Code project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
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

    # API - JWT Authentication
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API Routes
    path('api/', include('api.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin Site Configuration
admin.site.site_header = 'Spiritual G-Code Administration'
admin.site.site_title = 'G-Code Admin'
admin.site.index_title = 'Welcome to Spiritual G-Code Administration'
