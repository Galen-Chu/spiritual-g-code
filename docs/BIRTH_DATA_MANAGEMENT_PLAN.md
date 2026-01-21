# 📝 Birth Data Management Plan - Edit, Delete & Export

**Created**: 2025-01-20
**Target Implementation**: 2025-01-21
**Priority**: High
**Status**: Planning Phase

---

## 🎯 Overview

Comprehensive birth data management system with three main features:
1. **Edit Birth Data** - Update birth information with automatic natal chart recalculation
2. **Delete Natal Chart** - Remove calculated chart while keeping account
3. **Export Data** - Download all data (GDPR compliance)
4. **Delete Account** - Full account deletion with data cleanup

---

## 📊 Current State Analysis

### ✅ What Already Exists

| Feature | Status | Details |
|---------|--------|---------|
| **Database Models** | ✅ Complete | All models have CASCADE delete |
| **User Profile API** | ✅ Complete | GET/PATCH at `/api/auth/profile/` |
| **Delete Pattern** | ✅ Complete | `perform_destroy()` exists in ChartAnnotationViewSet |
| **Activity Logging** | ✅ Complete | UserActivity model tracks actions |
| **Display UI** | ✅ Complete | Settings page shows birth data (read-only) |

### ❌ What Needs to Be Built

| Feature | Status | Priority |
|---------|--------|----------|
| **Edit Birth Data UI** | ❌ Missing | High |
| **Natal Chart Delete** | ❌ Missing | High |
| **Data Export** | ❌ Missing | Medium |
| **Account Delete** | ❌ Missing | Medium |

---

## 🗂️ Database Relationships (CASCADE Behavior)

### Current CASCADE Setup
```python
# When GCodeUser is deleted:
├─ NatalChart (OneToOne) → CASCADE ✓
├─ DailyTransit (ForeignKey) → CASCADE ✓
├─ GeneratedContent (ForeignKey) → CASCADE ✓
├─ UserActivity (ForeignKey) → CASCADE ✓
└─ ChartAnnotation (ForeignKey) → CASCADE ✓
```

**Important**: Deleting a user will automatically delete ALL their data!

---

## 📋 Implementation Plan

### Feature 1: Edit Birth Data (Primary Goal)

#### Backend Changes

**File: `api/serializers.py`**

Add validation methods to `UserSerializer` class:
```python
def validate_birth_date(self, value):
    """Ensure birth date is not in the future."""
    from datetime import date
    if value > date.today():
        raise serializers.ValidationError(
            "Birth date cannot be in the future."
        )
    return value

def validate_birth_location(self, value):
    """Ensure birth location is provided."""
    if not value or not value.strip():
        raise serializers.ValidationError(
            "Birth location is required."
        )
    return value
```

Add custom update method:
```python
def update(self, instance, validated_data):
    """Update user and recalculate natal chart if birth data changed."""
    from .models import NatalChart, UserActivity
    import logging

    # Check if birth data changed
    birth_data_changed = (
        ('birth_date' in validated_data and validated_data['birth_date'] != instance.birth_date) or
        ('birth_time' in validated_data and validated_data['birth_time'] != instance.birth_time) or
        ('birth_location' in validated_data and validated_data['birth_location'] != instance.birth_location) or
        ('timezone' in validated_data and validated_data['timezone'] != instance.timezone)
    )

    # Store old data for logging
    old_data = {
        'birth_date': str(instance.birth_date),
        'birth_time': str(instance.birth_time) if instance.birth_time else None,
        'birth_location': instance.birth_location,
        'timezone': instance.timezone
    }

    # Update user instance
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()

    # Recalculate natal chart if birth data changed
    if birth_data_changed:
        try:
            from ai_engine.mock_calculator import MockGCodeCalculator
            calculator = MockGCodeCalculator()

            new_chart_data = calculator.calculate_natal_chart(
                birth_date=instance.birth_date,
                birth_time=instance.birth_time.strftime('%H:%M') if instance.birth_time else None,
                birth_location=instance.birth_location,
                timezone=instance.timezone
            )

            # Update or create natal chart
            NatalChart.objects.update_or_create(
                user=instance,
                defaults=new_chart_data
            )

            # Log activity
            UserActivity.objects.create(
                user=instance,
                activity_type='birth_data_updated',
                metadata={
                    'old_data': old_data,
                    'new_data': {
                        'birth_date': str(instance.birth_date),
                        'birth_location': instance.birth_location
                    }
                }
            )

        except Exception as e:
            logging.getLogger(__name__).error(
                f"Failed to recalculate natal chart: {str(e)}"
            )

    return instance
```

#### Frontend Changes

**File: `templates/settings/index.html`**

Replace birth information section (lines 99-132):

```html
<!-- Birth Information -->
<div class="card">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold text-white flex items-center">
            <i data-lucide="calendar" class="w-5 h-5 mr-2 terminal-text"></i>
            Birth Information
        </h2>
        <div class="flex gap-2">
            <button id="export-data-btn"
                    onclick="exportUserData()"
                    class="text-blue-400 hover:text-blue-300 text-sm font-medium">
                <i data-lucide="download" class="w-4 h-4 inline mr-1"></i>
                Export Data
            </button>
            <button id="edit-birth-data-btn"
                    onclick="showBirthDataEditForm()"
                    class="text-gcode-green hover:text-gcode-greenDim text-sm font-medium">
                <i data-lucide="edit-2" class="w-4 h-4 inline mr-1"></i>
                Edit
            </button>
        </div>
    </div>

    <!-- Display Mode -->
    <div id="birth-data-display" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <p class="text-sm text-gray-400">Birth Date</p>
                <p class="text-white font-medium">{{ user.birth_date|date:"F d, Y" }}</p>
            </div>
            <div>
                <p class="text-sm text-gray-400">Birth Time</p>
                <p class="text-white font-medium">{{ user.birth_time|time:"H:i"|default:"Not specified" }}</p>
            </div>
            <div>
                <p class="text-sm text-gray-400">Birth Location</p>
                <p class="text-white font-medium">{{ user.birth_location }}</p>
            </div>
            <div>
                <p class="text-sm text-gray-400">Timezone</p>
                <p class="text-white font-medium">{{ user.timezone }}</p>
            </div>
        </div>
    </div>

    <!-- Edit Mode -->
    <form id="birth-data-form" class="hidden space-y-6 mt-6">
        <!-- Warning Box -->
        <div class="p-4 bg-yellow-900/20 border border-yellow-600 rounded-lg mb-4">
            <div class="flex items-start">
                <i data-lucide="alert-triangle" class="w-5 h-5 text-yellow-500 mr-2 mt-0.5"></i>
                <div class="text-sm">
                    <p class="text-yellow-500 font-medium mb-1">Important: Birth Data Change</p>
                    <p class="text-yellow-200/80">
                        Updating your birth data will automatically recalculate your natal chart.
                        Your previous chart data will be replaced. This action cannot be undone.
                    </p>
                </div>
            </div>
        </div>

        <!-- Form Fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-medium text-gray-400 mb-2">
                    Birth Date <span class="text-red-500">*</span>
                </label>
                <input type="date" name="birth_date" required
                       value="{{ user.birth_date|date:'Y-m-d' }}"
                       class="w-full bg-gcode-bg border border-gcode-border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-gcode-green transition-colors">
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-400 mb-2">Birth Time</label>
                <input type="time" name="birth_time"
                       value="{% if user.birth_time %}{{ user.birth_time|time:'H:i' }}{% endif %}"
                       class="w-full bg-gcode-bg border border-gcode-border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-gcode-green transition-colors">
                <p class="text-xs text-gray-500 mt-1">Optional but recommended</p>
            </div>
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">
                Birth Location <span class="text-red-500">*</span>
            </label>
            <input type="text" name="birth_location" required
                   value="{{ user.birth_location }}"
                   class="w-full bg-gcode-bg border border-gcode-border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-gcode-green transition-colors"
                   placeholder="e.g., Taipei, Taiwan">
        </div>

        <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">
                Timezone <span class="text-red-500">*</span>
            </label>
            <select name="timezone"
                    class="w-full bg-gcode-bg border border-gcode-border rounded-lg px-4 py-3 text-white focus:outline-none focus:border-gcode-green transition-colors">
                <option value="UTC" {% if user.timezone == 'UTC' %}selected{% endif %}>UTC</option>
                <option value="Asia/Taipei" {% if user.timezone == 'Asia/Taipei' %}selected{% endif %}>Asia/Taipei (UTC+8)</option>
                <option value="Asia/Hong_Kong" {% if user.timezone == 'Asia/Hong_Kong' %}selected{% endif %}>Asia/Hong_Kong (UTC+8)</option>
                <option value="Asia/Singapore" {% if user.timezone == 'Asia/Singapore' %}selected{% endif %}>Asia/Singapore (UTC+8)</option>
                <option value="Asia/Shanghai" {% if user.timezone == 'Asia/Shanghai' %}selected{% endif %}>Asia/Shanghai (UTC+8)</option>
                <option value="Asia/Tokyo" {% if user.timezone == 'Asia/Tokyo' %}selected{% endif %}>Asia/Tokyo (UTC+9)</option>
                <option value="America/New_York" {% if user.timezone == 'America/New_York' %}selected{% endif %}>America/New_York (UTC-5)</option>
                <option value="America/Los_Angeles" {% if user.timezone == 'America/Los_Angeles' %}selected{% endif %}>America/Los_Angeles (UTC-8)</option>
                <option value="America/Chicago" {% if user.timezone == 'America/Chicago' %}selected{% endif %}>America/Chicago (UTC-6)</option>
                <option value="Europe/London" {% if user.timezone == 'Europe/London' %}selected{% endif %}>Europe/London (UTC+0)</option>
                <option value="Europe/Paris" {% if user.timezone == 'Europe/Paris' %}selected{% endif %}>Europe/Paris (UTC+1)</option>
                <option value="Europe/Berlin" {% if user.timezone == 'Europe/Berlin' %}selected{% endif %}>Europe/Berlin (UTC+1)</option>
                <option value="Australia/Sydney" {% if user.timezone == 'Australia/Sydney' %}selected{% endif %}>Australia/Sydney (UTC+10)</option>
            </select>
        </div>

        <div class="flex gap-3">
            <button type="submit"
                    class="bg-gcode-green text-gcode-bg font-bold px-6 py-2 rounded-lg hover:bg-gcode-greenDim transition-colors">
                Save Changes
            </button>
            <button type="button"
                    onclick="cancelBirthDataEdit()"
                    class="bg-gray-700 text-white font-bold px-6 py-2 rounded-lg hover:bg-gray-600 transition-colors">
                Cancel
            </button>
        </div>
    </form>
</div>
```

**Add JavaScript functions** (in `{% block extra_js %}` section):

```javascript
// Birth Data Edit Functions
function showBirthDataEditForm() {
    const confirmed = confirm(
        '⚠️ Editing your birth data will recalculate your natal chart.\n\n' +
        'Your current natal chart will be replaced.\n\n' +
        'Do you want to continue?'
    );

    if (confirmed) {
        document.getElementById('birth-data-display').classList.add('hidden');
        document.getElementById('birth-data-form').classList.remove('hidden');
        document.getElementById('edit-birth-data-btn').classList.add('hidden');
        lucide.createIcons();
    }
}

function cancelBirthDataEdit() {
    document.getElementById('birth-data-form').classList.add('hidden');
    document.getElementById('birth-data-display').classList.remove('hidden');
    document.getElementById('edit-birth-data-btn').classList.remove('hidden');
    document.getElementById('birth-data-form').reset();
}

// Birth Data Form Submit
document.getElementById('birth-data-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    // Validate
    const birthDate = new Date(data.birth_date);
    if (birthDate > new Date()) {
        showToast('Birth date cannot be in the future', 'error');
        return;
    }

    if (!data.birth_location?.trim()) {
        showToast('Birth location is required', 'error');
        return;
    }

    try {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.textContent = 'Saving...';
        submitBtn.disabled = true;

        const response = await fetch('/api/auth/profile/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            showToast('Birth data updated! Natal chart recalculated.', 'success');
            setTimeout(() => window.location.reload(), 2000);
        } else {
            const error = await response.json();
            const errorMsg = error.birth_date?.[0] || error.birth_location?.[0] || error.detail || 'Update failed';
            showToast(errorMsg, 'error');
        }
    } catch (error) {
        showToast('An error occurred', 'error');
    } finally {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.textContent = 'Save Changes';
        submitBtn.disabled = false;
    }
});
```

---

### Feature 2: Delete Natal Chart

#### Backend Changes

**File: `api/views.py`**

Add new endpoint to UserProfileView:
```python
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

    def delete(self, request):
        """Delete user's natal chart (not the account)."""
        from .models import NatalChart

        try:
            # Check if natal chart exists
            natal_chart = NatalChart.objects.filter(user=request.user).first()

            if not natal_chart:
                return Response(
                    {'detail': 'No natal chart found for this user.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Store chart data for logging before deletion
            chart_summary = {
                'sun_sign': natal_chart.sun_sign,
                'moon_sign': natal_chart.moon_sign,
                'ascendant': natal_chart.ascendant,
                'calculated_at': natal_chart.calculated_at.isoformat()
            }

            # Delete the natal chart
            natal_chart.delete()

            # Log activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='natal_chart_deleted',
                metadata=chart_summary
            )

            return Response(
                {
                    'message': 'Natal chart deleted successfully.',
                    'deleted_chart': chart_summary
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'detail': f'Error deleting natal chart: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

#### Frontend Changes

Add to settings page - new card for data management:

```html
<!-- Data Management -->
<div class="card">
    <h2 class="text-xl font-bold text-white mb-6 flex items-center">
        <i data-lucide="database" class="w-5 h-5 mr-2 terminal-text"></i>
        Data Management
    </h2>

    <div class="space-y-4">
        <!-- Delete Natal Chart -->
        <div class="p-4 bg-gcode-bg border border-gcode-border rounded-lg">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="text-white font-medium mb-1">Delete Natal Chart</h3>
                    <p class="text-sm text-gray-400">
                        Remove your calculated natal chart. Your birth data will be kept.
                        You can calculate a new chart anytime.
                    </p>
                </div>
                <button onclick="deleteNatalChart()"
                        class="bg-red-600 hover:bg-red-700 text-white font-medium px-4 py-2 rounded-lg transition-colors">
                    <i data-lucide="trash-2" class="w-4 h-4 inline mr-1"></i>
                    Delete
                </button>
            </div>
        </div>

        <!-- Account Actions -->
        <div class="p-4 bg-red-900/10 border border-red-600 rounded-lg">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="text-red-400 font-medium mb-1">Delete Account</h3>
                    <p class="text-sm text-gray-400">
                        Permanently delete your account and all data. This cannot be undone.
                    </p>
                </div>
                <button onclick="showDeleteAccountDialog()"
                        class="bg-red-600 hover:bg-red-700 text-white font-medium px-4 py-2 rounded-lg transition-colors">
                    <i data-lucide="user-x" class="w-4 h-4 inline mr-1"></i>
                    Delete Account
                </button>
            </div>
        </div>
    </div>
</div>
```

**Add JavaScript functions**:

```javascript
// Delete Natal Chart
async function deleteNatalChart() {
    const confirmed = confirm(
        '⚠️ Delete your natal chart?\n\n' +
        'This will remove your calculated natal chart data.\n' +
        'Your birth information will be kept.\n\n' +
        'You can calculate a new chart anytime.\n\n' +
        'Do you want to continue?'
    );

    if (!confirmed) return;

    try {
        const response = await fetch('/api/auth/profile/', {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (response.ok) {
            const result = await response.json();
            showToast('Natal chart deleted successfully', 'success');
            setTimeout(() => window.location.reload(), 2000);
        } else {
            const error = await response.json();
            showToast(error.detail || 'Failed to delete natal chart', 'error');
        }
    } catch (error) {
        showToast('An error occurred', 'error');
    }
}
```

---

### Feature 3: Export User Data (GDPR Compliance)

#### Backend Changes

**File: `api/views.py`**

Add new action to UserProfileView:
```python
@action(detail=False, methods=['get'])
def export_data(self, request):
    """Export all user data as JSON (GDPR compliance)."""
    from .models import NatalChart, DailyTransit, GeneratedContent, UserActivity
    import json
    from datetime import datetime

    # Collect all user data
    export_data = {
        'export_date': datetime.now().isoformat(),
        'user_profile': {
            'username': request.user.username,
            'email': request.user.email,
            'birth_date': str(request.user.birth_date),
            'birth_time': str(request.user.birth_time) if request.user.birth_time else None,
            'birth_location': request.user.birth_location,
            'timezone': request.user.timezone,
            'preferred_tone': request.user.preferred_tone,
            'created_at': request.user.created_at.isoformat(),
        },
        'natal_chart': None,
        'daily_transits': [],
        'generated_content': [],
        'activities': [],
    }

    # Get natal chart
    try:
        natal_chart = NatalChart.objects.get(user=request.user)
        export_data['natal_chart'] = {
            'sun_sign': natal_chart.sun_sign,
            'moon_sign': natal_chart.moon_sign,
            'ascendant': natal_chart.ascendant,
            'dominant_elements': natal_chart.dominant_elements,
            'key_aspects': natal_chart.key_aspects,
            'calculated_at': natal_chart.calculated_at.isoformat(),
        }
    except NatalChart.DoesNotExist:
        pass

    # Get recent daily transits (last 30)
    recent_transits = DailyTransit.objects.filter(
        user=request.user
    ).order_by('-transit_date')[:30]

    export_data['daily_transits'] = [
        {
            'date': str(transit.transit_date),
            'g_code_score': transit.g_code_score,
            'intensity_level': transit.intensity_level,
            'themes': transit.themes,
            'calculated_at': transit.created_at.isoformat(),
        }
        for transit in recent_transits
    ]

    # Get generated content
    content = GeneratedContent.objects.filter(user=request.user)[:10]
    export_data['generated_content'] = [
        {
            'content_type': item.content_type,
            'title': item.title,
            'status': item.status,
            'created_at': item.generated_at.isoformat(),
        }
        for item in content
    ]

    # Get recent activity
    activities = UserActivity.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]

    export_data['activities'] = [
        {
            'activity_type': activity.activity_type,
            'metadata': activity.metadata,
            'timestamp': activity.created_at.isoformat(),
        }
        for activity in activities
    ]

    # Create response
    response = Response(
        json.dumps(export_data, indent=2),
        content_type='application/json',
        headers={
            'Content-Disposition': f'attachment; filename="spiritual_gcode_data_{request.user.username}_{datetime.now().strftime("%Y%m%d")}.json"'
        }
    )

    # Log export
    UserActivity.objects.create(
        user=request.user,
        activity_type='data_exported',
        metadata={'export_type': 'full_user_data'}
    )

    return response
```

**Update URL routing** (`api/urls.py`):
```python
from .views import UserProfileView

# Add to urlpatterns
path('profile/', UserProfileView.as_view(), name='user-profile'),
path('profile/export/', UserProfileView.as_view({'get': 'export_data'}), name='user-export-data'),
```

#### Frontend JavaScript

```javascript
// Export User Data
async function exportUserData() {
    try {
        const response = await fetch('/api/profile/export/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (response.ok) {
            // Get filename from Content-Disposition header
            const contentDisposition = response.headers.get('Content-Disposition');
            const filenameMatch = contentDisposition && contentDisposition.match(/filename="(.+)"/);
            const filename = filenameMatch ? filenameMatch[1] : 'spiritual_gcode_data.json';

            // Download file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showToast('Data exported successfully!', 'success');
        } else {
            showToast('Failed to export data', 'error');
        }
    } catch (error) {
        showToast('An error occurred', 'error');
    }
}
```

---

### Feature 4: Delete Account (Full Deletion)

#### Backend Changes

**File: `api/views.py`**

Add new view:
```python
class AccountDeletionView(APIView):
    """Handle account deletion requests."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete user account and all associated data."""
        from django.contrib.auth import logout
        from .models import UserActivity

        username = request.user.username
        email = request.user.email

        # Log deletion before deleting user
        try:
            UserActivity.objects.create(
                user=request.user,
                activity_type='account_deleted',
                metadata={
                    'username': username,
                    'email': email,
                    'deleted_at': timezone.now().isoformat()
                }
            )
        except:
            pass  # Proceed even if logging fails

        # Delete user (CASCADE will delete all related data)
        request.user.delete()

        # Logout user
        logout(request)

        return Response(
            {
                'message': f'Account for {username} has been permanently deleted.',
                'deleted_at': timezone.now().isoformat()
            },
            status=status.HTTP_200_OK
        )
```

**Update URL routing** (`api/urls.py`):
```python
from .views import AccountDeletionView

path('account/delete/', AccountDeletionView.as_view(), name='account-delete'),
```

#### Frontend Changes

```html
<!-- Delete Account Dialog -->
<div id="delete-account-modal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-gcode-bg border border-gcode-border rounded-lg p-6 max-w-md w-full mx-4">
        <h2 class="text-xl font-bold text-white mb-4 flex items-center">
            <i data-lucide="alert-triangle" class="w-6 h-6 text-red-500 mr-2"></i>
            Delete Account
        </h2>

        <div class="space-y-4 mb-6">
            <p class="text-gray-300">
                This action <span class="text-red-400 font-bold">cannot be undone</span>.
            </p>

            <div class="p-4 bg-red-900/20 border border-red-600 rounded-lg">
                <h3 class="text-red-400 font-medium mb-2">This will permanently delete:</h3>
                <ul class="text-sm text-gray-300 space-y-1">
                    <li>• Your profile and birth data</li>
                    <li>• Your natal chart</li>
                    <li>• All daily transit calculations</li>
                    <li>• Generated content and notes</li>
                    <li>• Activity history</li>
                </ul>
            </div>

            <div class="p-4 bg-blue-900/20 border border-blue-600 rounded-lg">
                <h3 class="text-blue-400 font-medium mb-2">Before deleting:</h3>
                <ul class="text-sm text-gray-300 space-y-1">
                    <li>• Export your data (click "Export Data" above)</li>
                    <li>• Save any important information</li>
                </ul>
            </div>

            <div class="flex items-start">
                <input type="checkbox" id="delete-confirmation" class="mt-1 mr-2">
                <label for="delete-confirmation" class="text-sm text-gray-400">
                    I understand that this action cannot be undone and want to delete my account
                </label>
            </div>
        </div>

        <div class="flex gap-3">
            <button onclick="confirmAccountDeletion()"
                    id="confirm-delete-btn"
                    disabled
                    class="bg-red-600 hover:bg-red-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-bold px-6 py-2 rounded-lg transition-colors">
                Yes, Delete My Account
            </button>
            <button onclick="closeDeleteAccountDialog()"
                    class="bg-gray-700 hover:bg-gray-600 text-white font-bold px-6 py-2 rounded-lg transition-colors">
                Cancel
            </button>
        </div>
    </div>
</div>

<script>
// Account Deletion
function showDeleteAccountDialog() {
    document.getElementById('delete-account-modal').classList.remove('hidden');
    lucide.createIcons();
}

function closeDeleteAccountDialog() {
    document.getElementById('delete-account-modal').classList.add('hidden');
    document.getElementById('delete-confirmation').checked = false;
    document.getElementById('confirm-delete-btn').disabled = true;
}

// Enable/disable delete button based on checkbox
document.getElementById('delete-confirmation')?.addEventListener('change', function() {
    document.getElementById('confirm-delete-btn').disabled = !this.checked;
});

async function confirmAccountDeletion() {
    const confirmed = confirm(
        '⚠️ FINAL CONFIRMATION ⚠️\n\n' +
        'Are you ABSOLUTELY sure you want to delete your account?\n\n' +
        'All data will be permanently lost.\n\n' +
        'Type "DELETE" to confirm.'
    );

    if (!confirmed) return;

    try {
        const response = await fetch('/api/account/delete/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (response.ok) {
            // Clear local storage
            localStorage.clear();

            // Redirect to home
            window.location.href = '/';
        } else {
            const error = await response.json();
            showToast(error.detail || 'Failed to delete account', 'error');
        }
    } catch (error) {
        showToast('An error occurred', 'error');
    }
}
</script>
```

---

## 📅 Implementation Timeline

| Phase | Tasks | Duration | Priority |
|-------|-------|----------|----------|
| **Phase 1** | Edit Birth Data (Backend) | 25 min | High |
| **Phase 2** | Edit Birth Data (Frontend) | 30 min | High |
| **Phase 3** | Delete Natal Chart | 25 min | High |
| **Phase 4** | Export Data | 20 min | Medium |
| **Phase 5** | Delete Account | 25 min | Medium |
| **Phase 6** | Testing | 30 min | High |
| **Total** | All Features | **~155 min** | - |

---

## ✅ Acceptance Criteria

### Edit Birth Data
- [ ] Users can view birth data in settings
- [ ] "Edit" button shows confirmation dialog
- [ ] Form pre-fills with current values
- [ ] Validation prevents future dates
- [ ] Validation requires location
- [ ] Natal chart recalculates on save
- [ ] UserActivity log created
- [ ] Success message appears

### Delete Natal Chart
- [ ] "Delete" button in Data Management section
- [ ] Confirmation dialog warns user
- [ ] Chart deleted but birth data kept
- [ ] User can calculate new chart
- [ ] Activity logged

### Export Data
- [ ] "Export Data" button downloads JSON
- [ ] File includes all user data
- [ ] Filename includes username and date
- [ ] Activity logged

### Delete Account
- [ ] Multi-step confirmation process
- [ ] Warning shows what will be deleted
- [ ] Suggests exporting data first
- [ ] Checkbox confirmation required
- [ ] Final confirmation dialog
- [ ] Account and all data deleted
- [ ] User logged out and redirected

---

## 🔒 Security & Privacy

### Data Deletion (GDPR Compliance)
- **Right to Erasure**: Users can delete all their data
- **Data Export**: Users can download data before deletion
- **Clear Confirmation**: Multiple steps prevent accidental deletion
- **Audit Trail**: All deletions logged before deletion

### Data Retention
- **Activity Logs**: Kept for security even after account deletion
- **Cascade Delete**: All user data removed when account deleted
- **Soft Delete Consideration**: Could mark as deleted instead of removing

---

## 📊 Testing Checklist

### Backend Tests
```bash
# Test Edit Birth Data
curl -X PATCH http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"birth_date": "1995-12-25", "birth_location": "Tokyo"}'

# Test Delete Natal Chart
curl -X DELETE http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer <token>"

# Test Export Data
curl -X GET http://localhost:8000/api/profile/export/ \
  -H "Authorization: Bearer <token>" \
  -o user_data.json

# Test Delete Account
curl -X POST http://localhost:8000/api/account/delete/ \
  -H "Authorization: Bearer <token>"
```

### Frontend Tests
- [ ] All buttons trigger correct actions
- [ ] Confirmation dialogs appear
- [ ] Form validation works
- [ ] Loading states display
- [ ] Success/error messages show
- [ ] Data exports correctly
- [ ] Account deletion logs out user

---

## 🎯 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Edit Success Rate** | >95% | Users successfully update birth data |
| **Validation Accuracy** | 100% | All invalid inputs rejected |
| **Export Success** | 100% | All exports complete successfully |
| **Deletion Safety** | 0 accidental | No accidental deletions |
| **User Understanding** | >90% | Users understand warnings |

---

**Document Version**: 2.0
**Last Updated**: 2025-01-20
**Status**: Ready for Implementation
**Features**: Edit, Delete, Export, Account Deletion
**Estimated Time**: 155 minutes (2.5 hours)
