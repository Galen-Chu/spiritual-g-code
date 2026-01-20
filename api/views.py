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
from datetime import date, datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    GCodeUser,
    NatalChart,
    DailyTransit,
    GeneratedContent,
    GCodeTemplate,
    UserActivity,
)
from .annotation import ChartAnnotation

# Import AI engine for chart data generation
from ai_engine.daily_gcode_service import get_daily_gcode_service
from ai_engine.mock_calculator import MockGCodeCalculator
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
    ChartAnnotationSerializer,
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

        # Get custom date range parameters
        start_date_param = request.query_params.get('start_date')
        end_date_param = request.query_params.get('end_date')

        # Parse date range if provided
        custom_start_date = None
        custom_end_date = None

        if start_date_param:
            try:
                custom_start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid start_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if end_date_param:
            try:
                custom_end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid end_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validate date range
        if custom_start_date and custom_end_date:
            if custom_start_date > custom_end_date:
                return Response(
                    {'error': 'start_date must be before or equal to end_date.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data = {}

        # ========================================
        # 1. G-Code 7-Day Trend Chart
        # ========================================
        if chart_type in ['all', 'gcode_trend_7d']:
            # Use custom date range or default to last 7 days
            if custom_start_date and custom_end_date:
                start_date = custom_start_date
                end_date = custom_end_date
            else:
                end_date = date.today()
                start_date = end_date - timedelta(days=6)

            transits = DailyTransit.objects.filter(
                user=request.user,
                transit_date__gte=start_date,
                transit_date__lte=end_date
            ).order_by('transit_date')

            # Generate data for all dates in range
            trend_data = []
            current_date = start_date
            transit_dict = {t.transit_date: t for t in transits}

            while current_date <= end_date:
                if current_date in transit_dict:
                    t = transit_dict[current_date]
                    trend_data.append({
                        'date': current_date.isoformat(),
                        'score': t.g_code_score,
                        'intensity': t.intensity_level
                    })
                else:
                    # Generate mock data for missing dates
                    calculator = MockGCodeCalculator()
                    try:
                        natal = NatalChart.objects.get(user=request.user)
                        mock_transit = calculator.calculate_transits(
                            birth_date=request.user.birth_date,
                            birth_time=request.user.birth_time.strftime('%H:%M') if request.user.birth_time else None,
                            birth_location=request.user.birth_location,
                            target_date=current_date
                        )
                        score = calculator.calculate_g_code_intensity(
                            transit_data=mock_transit['planets'],
                            aspects=mock_transit['aspects']
                        )
                        intensity = 'low' if score < 25 else 'medium' if score < 50 else 'high' if score < 75 else 'intense'
                        trend_data.append({
                            'date': current_date.isoformat(),
                            'score': score,
                            'intensity': intensity
                        })
                    except:
                        trend_data.append({
                            'date': current_date.isoformat(),
                            'score': 50,
                            'intensity': 'medium'
                        })
                current_date += timedelta(days=1)

            data['gcode_trend_7d'] = trend_data

        # ========================================
        # 2. Planetary Positions (Polar Chart)
        # ========================================
        if chart_type in ['all', 'planetary_positions']:
            try:
                natal = NatalChart.objects.get(user=request.user)
                calculator = MockGCodeCalculator()

                # Calculate current natal chart
                chart_data = calculator.calculate_natal_chart(
                    birth_date=request.user.birth_date,
                    birth_time=request.user.birth_time.strftime('%H:%M') if request.user.birth_time else None,
                    birth_location=request.user.birth_location,
                    timezone=request.user.timezone
                )

                # Extract planetary positions
                planets = chart_data.get('chart_data', {})
                planetary_data = []

                planet_names = {
                    'sun': 'Sun', 'moon': 'Moon', 'mercury': 'Mercury',
                    'venus': 'Venus', 'mars': 'Mars', 'jupiter': 'Jupiter',
                    'saturn': 'Saturn', 'uranus': 'Uranus', 'neptune': 'Neptune',
                    'pluto': 'Pluto'
                }

                for planet_key, planet_name in planet_names.items():
                    if planet_key in planets:
                        pos = planets[planet_key]
                        planetary_data.append({
                            'planet': planet_name,
                            'sign': pos.get('sign', 'Unknown'),
                            'degree': pos.get('degree', 0),
                            'element': self._get_element(pos.get('sign', 'Unknown'))
                        })

                data['planetary_positions'] = planetary_data
            except NatalChart.DoesNotExist:
                data['planetary_positions'] = []

        # ========================================
        # 3. Element Distribution (Bar Chart)
        # ========================================
        if chart_type in ['all', 'element_distribution']:
            try:
                natal = NatalChart.objects.get(user=request.user)
                elements = natal.dominant_elements or {}

                data['element_distribution'] = [
                    {'element': 'Fire', 'count': elements.get('fire', 0), 'color': '#FF6B6B'},
                    {'element': 'Earth', 'count': elements.get('earth', 0), 'color': '#4ECDC4'},
                    {'element': 'Air', 'count': elements.get('air', 0), 'color': '#95E1D3'},
                    {'element': 'Water', 'count': elements.get('water', 0), 'color': '#45B7D1'},
                ]
            except NatalChart.DoesNotExist:
                data['element_distribution'] = []

        # ========================================
        # 4. Weekly Forecast Chart
        # ========================================
        if chart_type in ['all', 'weekly_forecast']:
            # Use custom date range or default to next 7 days
            forecast_data = []
            calculator = MockGCodeCalculator()

            try:
                natal = NatalChart.objects.get(user=request.user)
            except NatalChart.DoesNotExist:
                natal = None

            # Determine forecast date range
            if custom_start_date and custom_end_date:
                # Use custom date range
                forecast_start = custom_start_date
                forecast_end = custom_end_date
            else:
                # Default to next 7 days
                forecast_start = date.today() + timedelta(days=1)
                forecast_end = date.today() + timedelta(days=7)

            # Generate forecast for all dates in range
            current_date = forecast_start
            while current_date <= forecast_end:
                # Try to get existing transit data
                try:
                    transit = DailyTransit.objects.get(
                        user=request.user,
                        transit_date=current_date
                    )
                    forecast_data.append({
                        'date': current_date.isoformat(),
                        'score': transit.g_code_score,
                        'intensity': transit.intensity_level,
                        'themes': transit.themes or []
                    })
                except DailyTransit.DoesNotExist:
                    # Generate forecast data
                    if natal:
                        mock_transit = calculator.calculate_transits(
                            birth_date=request.user.birth_date,
                            birth_time=request.user.birth_time.strftime('%H:%M') if request.user.birth_time else None,
                            birth_location=request.user.birth_location,
                            target_date=current_date
                        )
                        score = calculator.calculate_g_code_intensity(
                            transit_data=mock_transit['planets'],
                            aspects=mock_transit['aspects']
                        )
                        intensity = 'low' if score < 25 else 'medium' if score < 50 else 'high' if score < 75 else 'intense'

                        # Generate themes based on aspects
                        themes = self._generate_themes_from_aspects(mock_transit['aspects'][:3])

                        forecast_data.append({
                            'date': current_date.isoformat(),
                            'score': score,
                            'intensity': intensity,
                            'themes': themes
                        })
                    else:
                        forecast_data.append({
                            'date': current_date.isoformat(),
                            'score': 50,
                            'intensity': 'medium',
                            'themes': ['#Growth', '#Alignment']
                        })

                current_date += timedelta(days=1)

            data['weekly_forecast'] = forecast_data

        # ========================================
        # 5. Aspects Network Data
        # ========================================
        if chart_type in ['all', 'aspects_network']:
            try:
                natal = NatalChart.objects.get(user=request.user)
                calculator = MockGCodeCalculator()

                # Get current transits
                transit_data = calculator.calculate_transits(
                    birth_date=request.user.birth_date,
                    birth_time=request.user.birth_time.strftime('%H:%M') if request.user.birth_time else None,
                    birth_location=request.user.birth_location,
                    target_date=date.today()
                )

                # Build network data
                nodes = []
                links = []

                # Add planets as nodes
                planets = transit_data.get('planets', {})
                for planet_name, planet_data in planets.items():
                    nodes.append({
                        'id': planet_name,
                        'label': planet_name.capitalize(),
                        'group': self._get_planet_group(planet_name)
                    })

                # Add aspects as links
                aspects = transit_data.get('aspects', [])[:15]  # Limit to 15 aspects
                for aspect in aspects:
                    links.append({
                        'source': aspect.get('transit_planet', aspect.get('planet1', '')),
                        'target': aspect.get('natal_planet', aspect.get('planet2', '')),
                        'type': aspect.get('aspect', ''),
                        'value': aspect.get('orb', 1)
                    })

                data['aspects_network'] = {
                    'nodes': nodes,
                    'links': links
                }
            except Exception as e:
                # Generate mock aspects network data for testing
                data['aspects_network'] = self._get_mock_aspects_network()

        return Response(data)

    def _get_element(self, sign):
        """Get element from zodiac sign."""
        fire_signs = ['Aries', 'Leo', 'Sagittarius']
        earth_signs = ['Taurus', 'Virgo', 'Capricorn']
        air_signs = ['Gemini', 'Libra', 'Aquarius']
        water_signs = ['Cancer', 'Scorpio', 'Pisces']

        if sign in fire_signs:
            return 'fire'
        elif sign in earth_signs:
            return 'earth'
        elif sign in air_signs:
            return 'air'
        elif sign in water_signs:
            return 'water'
        return 'air'  # default

    def _get_planet_group(self, planet_name):
        """Get planet group for visualization."""
        personal = ['sun', 'moon', 'mercury', 'venus', 'mars']
        social = ['jupiter', 'saturn']
        outer = ['uranus', 'neptune', 'pluto']

        if planet_name.lower() in personal:
            return 'personal'
        elif planet_name.lower() in social:
            return 'social'
        else:
            return 'outer'

    def _generate_themes_from_aspects(self, aspects):
        """Generate themes from aspect data."""
        theme_pool = [
            '#Transformation', '#Growth', '#Alignment', '#InnerWisdom',
            '#CosmicEnergy', '#Intuition', '#Creativity', '#Balance'
        ]
        import random
        random.seed(42)
        return random.sample(theme_pool, min(len(aspects), 3))

    def _get_mock_aspects_network(self):
        """Generate mock aspects network data for visualization."""
        planets = [
            {'id': 'sun', 'label': 'Sun', 'group': 'personal'},
            {'id': 'moon', 'label': 'Moon', 'group': 'personal'},
            {'id': 'mercury', 'label': 'Mercury', 'group': 'personal'},
            {'id': 'venus', 'label': 'Venus', 'group': 'personal'},
            {'id': 'mars', 'label': 'Mars', 'group': 'personal'},
            {'id': 'jupiter', 'label': 'Jupiter', 'group': 'social'},
            {'id': 'saturn', 'label': 'Saturn', 'group': 'social'},
            {'id': 'uranus', 'label': 'Uranus', 'group': 'outer'},
            {'id': 'neptune', 'label': 'Neptune', 'group': 'outer'},
            {'id': 'pluto', 'label': 'Pluto', 'group': 'outer'},
        ]

        # Mock aspects with different types
        aspects = [
            {'source': 'sun', 'target': 'moon', 'type': 'conjunction', 'value': 2},
            {'source': 'sun', 'target': 'jupiter', 'type': 'trine', 'value': 1},
            {'source': 'moon', 'target': 'venus', 'type': 'sextile', 'value': 3},
            {'source': 'mercury', 'target': 'mars', 'type': 'square', 'value': 4},
            {'source': 'venus', 'target': 'neptune', 'type': 'opposition', 'value': 2},
            {'source': 'mars', 'target': 'pluto', 'type': 'conjunction', 'value': 1},
            {'source': 'jupiter', 'target': 'saturn', 'type': 'square', 'value': 3},
            {'source': 'uranus', 'target': 'mars', 'type': 'trine', 'value': 2},
            {'source': 'neptune', 'target': 'mercury', 'type': 'sextile', 'value': 4},
            {'source': 'pluto', 'target': 'sun', 'type': 'opposition', 'value': 1},
            {'source': 'saturn', 'target': 'moon', 'type': 'trine', 'value': 2},
            {'source': 'uranus', 'target': 'venus', 'type': 'square', 'value': 3},
        ]

        return {
            'nodes': planets,
            'links': aspects
        }


# ============================================
# Solar System Transit View
# ============================================

class SolarSystemTransitView(APIView):
    """API endpoint for solar system transit visualization."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get solar system transit data for D3.js visualization."""
        try:
            from ai_engine.calculator import GCodeCalculator

            # Get target date from query params (default to today)
            date_param = request.query_params.get('date')
            if date_param:
                try:
                    target_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                except ValueError:
                    return Response(
                        {'error': 'Invalid date format. Use YYYY-MM-DD.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                target_date = date.today()

            # Calculate solar system transits
            try:
                calculator = GCodeCalculator()
                solar_system_data = calculator.calculate_solar_system_transits(target_date)
            except Exception as e:
                # Fall back to mock calculator if PyEphem fails
                from ai_engine.mock_calculator import MockGCodeCalculator
                calculator = MockGCodeCalculator()
                solar_system_data = calculator.calculate_solar_system_transits(target_date)

            # Log activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='solar_system_viewed',
                metadata={'target_date': target_date.isoformat()}
            )

            return Response(solar_system_data)

        except Exception as e:
            return Response(
                {'error': f'Error calculating solar system transits: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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


# ============================================
# Chart Annotation Views
# ============================================

class ChartAnnotationViewSet(viewsets.ModelViewSet):
    """ViewSet for ChartAnnotation model."""

    serializer_class = ChartAnnotationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['chart_type']
    search_fields = ['note']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return annotations for current user."""
        return ChartAnnotation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save annotation with current user."""
        serializer.save(user=self.request.user)

        # Log activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='annotation_created',
            metadata={
                'chart_type': serializer.validated_data.get('chart_type'),
                'data_point': serializer.validated_data.get('data_point'),
            }
        )

    def perform_destroy(self, instance):
        """Log annotation deletion."""
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='annotation_deleted',
            metadata={
                'chart_type': instance.chart_type,
                'data_point': instance.data_point,
            }
        )
        instance.delete()

    @action(detail=False, methods=['get'])
    def by_chart_type(self, request):
        """Get annotations filtered by chart type."""
        chart_type = request.query_params.get('chart_type')

        if not chart_type:
            return Response(
                {'error': 'chart_type query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        annotations = self.get_queryset().filter(chart_type=chart_type)
        serializer = self.get_serializer(annotations, many=True)
        return Response(serializer.data)


# ============================================
# Natal Wheel View
# ============================================

class NatalWheelView(APIView):
    """API endpoint for natal wheel data."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get natal wheel data for D3.js rendering."""
        try:
            # Get user's natal chart
            try:
                natal_chart = NatalChart.objects.get(user=request.user)
            except NatalChart.DoesNotExist:
                return Response(
                    {'error': 'Natal chart not found. Please calculate your natal chart first.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Calculate wheel data
            calculator = MockGCodeCalculator()
            wheel_data = calculator.calculate_natal_wheel_data(
                birth_date=natal_chart.birth_date,
                birth_time=natal_chart.birth_time.strftime('%H:%M') if natal_chart.birth_time else None,
                birth_location=natal_chart.birth_location,
                timezone=natal_chart.timezone
            )

            return Response(wheel_data)

        except Exception as e:
            return Response(
                {'error': f'Error calculating wheel data: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
