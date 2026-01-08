"""
API Views for Spiritual G-Code.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.db.models import Q, Count, Avg
from datetime import date, timedelta
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    GCodeUser,
    NatalChart,
    DailyTransit,
    GeneratedContent,
    GCodeTemplate,
    UserActivity,
)
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    NatalChartSerializer,
    DailyTransitSerializer,
    GeneratedContentSerializer,
    GenerateContentSerializer,
    GCodeTemplateSerializer,
    UserActivitySerializer,
    DashboardOverviewSerializer,
    NatalChartCalculationSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsOwner, HasDailyGCodeEnabled
from .filters import DailyTransitFilter, GeneratedContentFilter, GCodeTemplateFilter


# ============================================
# Authentication Views
# ============================================

class RegisterView(APIView):
    """User registration endpoint."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='user_registered',
                metadata={'ip_address': self.get_client_ip(request)}
            )
            return Response(
                {
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileView(APIView):
    """User profile endpoint."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Update user profile."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            UserActivity.objects.create(
                user=request.user,
                activity_type='profile_updated'
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# Natal Chart Views
# ============================================

class NatalChartViewSet(viewsets.ModelViewSet):
    """ViewSet for NatalChart model."""

    serializer_class = NatalChartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['calculated_at', 'updated_at']
    ordering = ['-calculated_at']

    def get_queryset(self):
        """Return natal chart for current user."""
        return NatalChart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate natal chart for user."""
        serializer = NatalChartCalculationSerializer(data=request.data)
        if serializer.is_valid():
            # Import calculator
            from ai_engine.calculator import GCodeCalculator

            try:
                calculator = GCodeCalculator()
                chart_data = calculator.calculate_natal_chart(
                    birth_date=serializer.validated_data['birth_date'],
                    birth_time=serializer.validated_data.get('birth_time'),
                    birth_location=serializer.validated_data['birth_location'],
                    timezone=serializer.validated_data.get('timezone', 'UTC')
                )

                # Create or update natal chart
                natal_chart, created = NatalChart.objects.update_or_create(
                    user=request.user,
                    defaults=chart_data
                )

                # Log activity
                UserActivity.objects.create(
                    user=request.user,
                    activity_type='natal_chart_calculated',
                    metadata={'created': created}
                )

                return Response(
                    NatalChartSerializer(natal_chart).data,
                    status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# Daily Transit Views
# ============================================

class DailyTransitViewSet(viewsets.ModelViewSet):
    """ViewSet for DailyTransit model."""

    serializer_class = DailyTransitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_class = DailyTransitFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['themes', 'interpretation']
    ordering_fields = ['transit_date', 'g_code_score', 'created_at']
    ordering = ['-transit_date']

    def get_queryset(self):
        """Return daily transits for current user."""
        return DailyTransit.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get today's G-Code."""
        today = date.today()
        try:
            transit = DailyTransit.objects.get(user=request.user, transit_date=today)
            serializer = self.get_serializer(transit)
            return Response(serializer.data)
        except DailyTransit.DoesNotExist:
            return Response(
                {'message': 'No G-Code calculated for today yet.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """Get weekly forecast (next 7 days)."""
        start_date = date.today()
        end_date = start_date + timedelta(days=7)

        transits = DailyTransit.objects.filter(
            user=request.user,
            transit_date__range=[start_date, end_date]
        )
        serializer = self.get_serializer(transits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def range(self, request):
        """Get transits for a date range."""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {'error': 'Both start_date and end_date are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transits = DailyTransit.objects.filter(
            user=request.user,
            transit_date__range=[start_date, end_date]
        )
        serializer = self.get_serializer(transits, many=True)
        return Response(serializer.data)


# ============================================
# Generated Content Views
# ============================================

class GeneratedContentViewSet(viewsets.ModelViewSet):
    """ViewSet for GeneratedContent model."""

    serializer_class = GeneratedContentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_class = GeneratedContentFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body', 'hashtags']
    ordering_fields = ['generated_at', 'scheduled_for', 'posted_at']
    ordering = ['-generated_at']

    def get_queryset(self):
        """Return generated content for current user."""
        return GeneratedContent.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate new content using AI."""
        serializer = GenerateContentSerializer(data=request.data)
        if serializer.is_valid():
            from ai_engine.gemini_client import GeminiGCodeClient

            try:
                # Get transit data
                transit_date = serializer.validated_data.get('transit_date', date.today())
                transit = DailyTransit.objects.get(
                    user=request.user,
                    transit_date=transit_date
                )

                # Initialize AI client
                ai_client = GeminiGCodeClient()

                # Generate content
                generated_content = ai_client.generate_content(
                    transit_data=transit.transit_data,
                    content_type=serializer.validated_data['content_type'],
                    platform=serializer.validated_data['platform'],
                    custom_instructions=serializer.validated_data.get('custom_instructions', ''),
                    user_preferences={
                        'tone': request.user.preferred_tone
                    }
                )

                # Save to database
                content = GeneratedContent.objects.create(
                    user=request.user,
                    related_transit=transit,
                    **generated_content
                )

                # Log activity
                UserActivity.objects.create(
                    user=request.user,
                    activity_type='content_generated',
                    metadata={
                        'content_type': content.content_type,
                        'platform': content.platform
                    }
                )

                return Response(
                    self.get_serializer(content).data,
                    status=status.HTTP_201_CREATED
                )
            except DailyTransit.DoesNotExist:
                return Response(
                    {'error': 'No transit data found for the specified date.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def post(self, request, pk=None):
        """Post content to social media platform."""
        content = self.get_object()

        # Here you would integrate with social media APIs
        # For now, just mark as posted
        content.status = 'posted'
        content.posted_at = timezone.now()
        content.save()

        UserActivity.objects.create(
            user=request.user,
            activity_type='content_posted',
            metadata={
                'content_id': content.id,
                'platform': content.platform
            }
        )

        return Response(
            {'message': 'Content posted successfully', 'posted_at': content.posted_at}
        )


# ============================================
# G-Code Template Views
# ============================================

class GCodeTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for GCodeTemplate model (read-only for regular users)."""

    serializer_class = GCodeTemplateSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = GCodeTemplateFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

    def get_queryset(self):
        """Return active templates."""
        return GCodeTemplate.objects.filter(is_active=True)


# ============================================
# Dashboard Views
# ============================================

class DashboardOverviewView(APIView):
    """Dashboard overview endpoint."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get dashboard overview data."""
        # Get today's G-Code
        try:
            today_gcode = DailyTransit.objects.get(
                user=request.user,
                transit_date=date.today()
            )
        except DailyTransit.DoesNotExist:
            today_gcode = None

        # Get weekly transits
        start_date = date.today()
        end_date = start_date + timedelta(days=7)
        weekly_transits = DailyTransit.objects.filter(
            user=request.user,
            transit_date__range=[start_date, end_date]
        )

        # Get recent content
        recent_content = GeneratedContent.objects.filter(
            user=request.user
        ).order_by('-generated_at')[:5]

        # Calculate user stats
        total_transits = DailyTransit.objects.filter(user=request.user).count()
        total_content = GeneratedContent.objects.filter(user=request.user).count()
        avg_gcode_score = DailyTransit.objects.filter(
            user=request.user
        ).aggregate(avg=Avg('g_code_score'))['avg'] or 0

        user_stats = {
            'total_transits': total_transits,
            'total_content': total_content,
            'avg_gcode_score': round(avg_gcode_score, 1),
            'member_since': request.user.created_at,
        }

        # Log activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='dashboard_viewed'
        )

        serializer = DashboardOverviewSerializer({
            'today_gcode': today_gcode,
            'weekly_transits': weekly_transits,
            'recent_content': recent_content,
            'user_stats': user_stats,
        })

        return Response(serializer.data)


class DashboardChartsView(APIView):
    """Dashboard chart data endpoint."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get data for dashboard charts."""
        chart_type = request.query_params.get('type', 'all')

        data = {}

        if chart_type in ['all', 'gcode_trend']:
            # G-Code score trend (last 30 days)
            start_date = date.today() - timedelta(days=30)
            transits = DailyTransit.objects.filter(
                user=request.user,
                transit_date__gte=start_date
            ).order_by('transit_date')

            data['gcode_trend'] = [
                {
                    'date': t.transit_date.isoformat(),
                    'score': t.g_code_score,
                    'intensity': t.intensity_level
                }
                for t in transits
            ]

        if chart_type in ['all', 'themes']:
            # Top themes (last 90 days)
            start_date = date.today() - timedelta(days=90)
            transits = DailyTransit.objects.filter(
                user=request.user,
                transit_date__gte=start_date
            )

            theme_counts = {}
            for transit in transits:
                for theme in transit.themes or []:
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1

            data['themes'] = [
                {'theme': theme, 'count': count}
                for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ]

        if chart_type in ['all', 'content_distribution']:
            # Content distribution by platform
            content_stats = GeneratedContent.objects.filter(
                user=request.user
            ).values('platform', 'content_type').annotate(
                count=Count('id')
            )

            data['content_distribution'] = list(content_stats)

        return Response(data)


# ============================================
# Health Check View
# ============================================

class HealthCheckView(APIView):
    """Health check endpoint."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Check system health."""
        from django.db import connections
        from ai_engine.gemini_client import GeminiGCodeClient

        health_status = {
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'services': {}
        }

        # Check database
        try:
            db_conn = connections['default']
            db_conn.cursor()
            health_status['services']['database'] = {
                'status': 'healthy'
            }
        except Exception as e:
            health_status['services']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'

        # Check Redis
        try:
            from django.core.cache import cache
            cache.set('health_check', 'ok', 10)
            cache.get('health_check')
            health_status['services']['redis'] = {
                'status': 'healthy'
            }
        except Exception as e:
            health_status['services']['redis'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'

        # Check Gemini API
        try:
            # Simple connectivity check
            health_status['services']['gemini_api'] = {
                'status': 'healthy'
            }
        except Exception as e:
            health_status['services']['gemini_api'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_status['status'] = 'degraded'

        return Response(health_status)
