# DEBUG_2026-01-23_Authentication_Session_Fix

**Date:** 2026-01-23
**Session:** First Debugging Session with User
**Project:** Spiritual G-Code
**Tester:** Claude Code Assistant
**Python Version:** 3.11+
**Django Version:** 5.0.1

---

## 📋 Issue Description

**Problem Statement:**
Users could not login to the Spiritual G-Code application. The login page appeared to work (returned JWT tokens), but users were immediately redirected back to the login page when trying to access the dashboard. Registration was also broken.

**Reported By:** User
**Severity:** Critical (application completely unusable)
**Affected Components:**
- Authentication system
- Login page (`/auth/login/`)
- Registration page (`/auth/register/`)
- Dashboard (`/`)

---

## 🔍 Investigation Process

### Step 1: Initial Assessment

**Actions Taken:**
- ✅ Checked server logs via background task output
- ✅ Verified database state (found 3 users: admin, testuser, testuser2)
- ✅ Reviewed HTTP requests in server logs
- ✅ Examined authentication flow

**Findings:**
```
Server logs showed:
1. POST /api/auth/login/ returned 200 OK (JWT tokens issued)
2. GET / returned 302 (redirect to login)
3. GET /auth/login/ returned 200 (user not authenticated in session)

Key observation: Login API succeeded but dashboard still redirected to login.
```

### Step 2: Root Cause Analysis

**Hypothesis:** JWT tokens were being issued but Django session was not being created.

**Investigation Steps:**

1. **Reviewed authentication architecture**
   - Finding: Application uses **mixed authentication**
     - Frontend: JWT tokens (stored in localStorage)
     - Backend HTML views: Django session auth (`@login_required` decorator)

2. **Examined login flow**
   - Login form sends POST to `/api/auth/login/`
   - Uses `TokenObtainPairView` from `rest_framework_simplejwt`
   - Returns JWT tokens but **does not create Django session**

3. **Examined dashboard access**
   - Dashboard view uses `@login_required` decorator
   - This decorator checks for Django session, not JWT tokens
   - No session = redirect to login

4. **Tested registration**
   - Registration form sends POST to `/api/auth/register/`
   - Similar issue: creates user but no session

**Root Cause Identified:**
```
The application has a mixed authentication architecture:
1. JWT authentication for API calls (tokens in localStorage)
2. Session authentication for HTML views (@login_required decorator)

The login endpoint only created JWT tokens but did NOT create a Django session.
Therefore, after login:
- API calls would work (JWT tokens present)
- HTML pages would fail (no session cookie)

The @login_required decorator on dashboard_view checks for session auth,
not JWT tokens, causing the redirect loop.
```

### Step 3: Solution Design

**Approach:** Create a custom login view that handles BOTH JWT tokens AND Django session authentication.

**Alternatives Considered:**
1. **Option A: Use only JWT authentication**
   - Pros: Single auth method, stateless
   - Cons: Requires rewriting all HTML views, complex middleware
   - ❌ Rejected: Too invasive

2. **Option B: Use only session authentication**
   - Pros: Simple, works with existing @login_required
   - Cons: Breaks API clients that expect JWT
   - ❌ Rejected: Breaks existing API contract

3. **Option C: Hybrid approach (SELECTED)**
   - Pros: Works for both HTML views and API calls, minimal changes
   - Cons: Maintains two auth systems
   - ✅ Selected: Best balance of compatibility and effort

**Selected Solution:** Create `CustomLoginView` that:
1. Authenticates user credentials
2. Creates Django session (for HTML views)
3. Generates JWT tokens (for API calls)
4. Returns both to the client

---

## 🛠️ Implementation

### Changes Made

| File | Line(s) | Change Description |
|------|---------|-------------------|
| `api/views.py` | 45-83 | Added `CustomLoginView` class |
| `api/views.py` | 85-110 | Updated `RegisterView` to create session |
| `core/urls.py` | 18 | Imported `CustomLoginView` |
| `core/urls.py` | 51 | Updated URL to use `CustomLoginView` |
| `api/urls.py` | 46 | Renamed API URL from `'register'` to `'api-register'` |

### Code Changes Details

**File: `api/views.py` (Added CustomLoginView)**
```python
class CustomLoginView(APIView):
    """Custom login view that creates both JWT token and Django session."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle login - returns JWT tokens and creates Django session."""
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Create Django session
            auth_login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='user_logged_in',
                metadata={'ip_address': self.get_client_ip(request)}
            )

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })

        return Response(
            {'detail': 'No active account found with the given credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
```

**File: `api/views.py` (Updated RegisterView)**
```python
def post(self, request):
    """Register a new user and create session."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Create Django session for new user
        auth_login(request, user)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # ... rest of implementation
```

**File: `api/urls.py` (Fixed URL conflict)**
```python
# Before:
path('auth/register/', RegisterView.as_view(), name='register'),

# After:
path('auth/register/', RegisterView.as_view(), name='api-register'),
```

---

## ✅ Verification

### Test Cases Executed

| Test Case | Expected Result | Actual Result | Status |
|-----------|----------------|---------------|--------|
| Admin login (admin/admin123) | Session created, JWT tokens returned, dashboard accessible | ✅ Passed | ✅ |
| Test user registration (testuser999) | User created, session created, auto-login | ✅ Passed | ✅ |
| Session cookie verification | `sessionid` and `csrftoken` cookies set | ✅ Passed | ✅ |
| Dashboard access after login | HTTP 200 (not 302 redirect) | ✅ Passed | ✅ |
| URL name conflict | `{% url 'register' %}` resolves to HTML page | ✅ Passed | ✅ |

### Manual Testing

**Test Commands Used:**
```bash
# Test login and session creation
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  -c /tmp/cookies.txt

# Verify session cookies were created
cat /tmp/cookies.txt
# Output showed: sessionid and csrftoken cookies present ✅

# Test dashboard access with session
curl -i http://127.0.0.1:8000/ -b /tmp/cookies.txt
# Output showed: HTTP/1.1 200 OK (not 302 redirect) ✅

# Test registration
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser999","email":"test999@example.com",...}'
# Output showed: User registered successfully, tokens returned ✅

# Verify user in database
python manage.py shell -c "from api.models import GCodeUser; print(GCodeUser.objects.all().values_list('username', 'is_active'))"
# Output showed: testuser999 created ✅
```

### URL Resolution Testing
```bash
python manage.py shell -c "from django.urls import reverse; print(reverse('register'))"
# Output: /auth/register/ ✅ (not /api/auth/register/)

python manage.py shell -c "from django.urls import reverse; print(reverse('api-register'))"
# Output: /api/auth/register/ ✅
```

---

## 📚 Documentation Updates

### Created Files
- ✅ `tests/reports/DEBUG_Template.md` - Template for future debugging sessions
- ✅ `tests/reports/DEBUG_2026-01-23_Authentication_Session_Fix.md` - This report

### Updated Files
- `README_Testing.md` - Should be updated to include debugging reports section

### New Knowledge Created
- Understanding of hybrid authentication (JWT + Session) in Django
- URL name conflicts between HTML and API routes
- Debugging procedure for authentication issues

---

## 🎯 Lessons Learned

### What Went Well
1. **Systematic investigation approach** - Checked logs → database → code flow
2. **Identified root cause clearly** - Understood the mixed authentication architecture
3. **Minimal, targeted changes** - Only modified necessary files
4. **Comprehensive testing** - Verified all aspects of the fix

### What Could Be Improved
1. **Prevention**: Could have integration tests that verify login → dashboard flow
2. **Documentation**: Authentication architecture should be clearly documented
3. **URL naming**: API routes should use `api-` prefix to avoid conflicts (e.g., `api-login`, `api-register`)

### Prevention Strategies

**For Future Development:**
1. **URL Naming Convention**:
   - HTML view URLs: `name` (e.g., `'register'`, `'login'`)
   - API view URLs: `api-name` (e.g., `'api-register'`, `'api-login'`)

2. **Integration Tests**:
   - Add test for login → redirect → dashboard flow
   - Add test for registration → auto-login → dashboard flow

3. **Authentication Documentation**:
   - Document hybrid authentication approach
   - Explain when to use JWT vs Session
   - Create troubleshooting guide for auth issues

**Suggested Test Additions:**
```python
# tests/integration/test_auth_flow.py
def test_login_creates_session_and_jwt(client):
    """Test that login creates both session and JWT tokens."""
    response = client.post('/api/auth/login/', {
        'username': 'admin',
        'password': 'admin123'
    })

    # Check JWT tokens returned
    assert 'access' in response.json()
    assert 'refresh' in response.json()

    # Check session created
    assert 'sessionid' in client.cookies

    # Check dashboard accessible
    response = client.get('/')
    assert response.status_code == 200  # Not 302
```

---

## 📊 Session Statistics

| Metric | Value |
|--------|-------|
| Duration | ~45 minutes |
| Files Modified | 3 |
| Lines Changed | ~80 |
| Bugs Fixed | 2 (login session, URL conflict) |
| Tests Verified | 5 |
| New Documentation | 2 files |

---

## 🔗 Related Resources

**Code Files:**
- `api/views.py:45-110` - CustomLoginView and updated RegisterView
- `core/urls.py:18,51` - URL configuration updates
- `api/urls.py:46` - URL name conflict fix

**Documentation:**
- [Django Authentication Docs](https://docs.djangoproject.com/en/5.0/topics/auth/)
- [DRF SimpleJWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)

**Similar Issues:**
- N/A (First documented debugging session)

---

## ✍️ Session Notes

This was our first collaborative debugging session. The user provided clear feedback about what was broken, and we followed a systematic approach:

1. **Server log analysis** - Identified the redirect loop
2. **Database verification** - Confirmed users existed
3. **Code flow tracing** - Found the mixed authentication issue
4. **Solution design** - Chose hybrid approach for compatibility
5. **Implementation** - Minimal changes, no breaking changes
6. **Verification** - Comprehensive testing of all scenarios

**Key Insight:** The application was designed with JWT for APIs and session for HTML views, but the login endpoint only handled JWT. This caused a disconnect where API login succeeded but HTML pages couldn't verify authentication.

**User Feedback:** The user noticed the navigation link was pointing to the wrong URL (API endpoint instead of HTML page), which led to discovering the URL name conflict.

---

**Status:** ✅ Resolved
**Next Review Date:** N/A (one-time fix)
**Report Generated:** 2026-01-23 08:45 UTC
