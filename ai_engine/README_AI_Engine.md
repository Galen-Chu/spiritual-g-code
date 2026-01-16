# AI Engine Documentation

## Overview

The `ai_engine/` directory contains all astrological calculation services and AI content generation logic for the Spiritual G-Code platform. It provides both production implementations (using PyEphem and Google Gemini) and deterministic mock implementations for development.

**Technology Stack:**
- PyEphem (astronomical calculations)
- Google Generative AI (Gemini API)
- Custom deterministic mocks

---

## Directory Structure

```
ai_engine/
├── __init__.py
├── calculator.py              # PyEphem-based calculator (requires C++ compiler)
├── mock_calculator.py         # Deterministic mock calculator (583 lines)
├── gemini_client.py           # Google Gemini AI client
├── mock_gemini_client.py      # Mock AI client for development
├── daily_gcode_service.py     # Orchestration service (212 lines)
└── prompts/                   # AI prompt templates
    ├── daily_gcode.txt        # Daily G-Code interpretation prompt
    ├── spiritual_patch_note.txt  # Social media content prompt
    └── weekly_forecast.txt    # Weekly forecast prompt
```

---

## Core Components

### 1. Calculator Services

#### Production Calculator (`calculator.py`)
**Uses PyEphem library for astronomical calculations.**

**Requirements:**
- C++ compiler
- PyEphem package
- Ephemeris data

**Note:** Requires compilation and external dependencies. For development, use `mock_calculator.py`.

#### Mock Calculator (`mock_calculator.py`)
**Deterministic mock implementation for development.**

**Purpose:**
- Full-featured replacement for production calculator
- No external dependencies
- Deterministic output (same input = same output)
- 583 lines of comprehensive logic

**Key Functions:**

##### `calculate_natal_chart(birth_data)`
Calculates complete natal chart from birth information.

**Parameters:**
- `birth_data` (dict):
  - `date` - Birth date (YYYY-MM-DD)
  - `time` - Birth time (HH:MM)
  - `latitude` - Birth latitude (float)
  - `longitude` - Birth longitude (float)
  - `timezone` - Timezone string

**Returns:**
```python
{
    "planets": {
        "sun": {"sign": "Leo", "degree": 15.5, "house": 5},
        "moon": {"sign": "Pisces", "degree": 22.3, "house": 8},
        "mercury": {"sign": "Virgo", "degree": 3.1, "house": 6},
        # ... all 10 planets
    },
    "houses": {
        "1": {"sign": "Scorpio", "cusp": 215.5},
        "2": {"sign": "Sagittarius", "cusp": 245.2},
        # ... all 12 houses
    },
    "aspects": [
        {"planet1": "sun", "planet2": "moon", "type": "trine", "degree": 120},
        # ... aspect calculations
    ],
    "ascendant": {"sign": "Scorpio", "degree": 15.2},
    "midheaven": {"sign": "Leo", "degree": 180.5},
    "dominant_element": "fire"
}
```

##### `calculate_transits(natal_chart, target_date)`
Calculates planetary transits for a specific date.

**Parameters:**
- `natal_chart` - Natal chart data from `calculate_natal_chart()`
- `target_date` - Date to calculate transits for (YYYY-MM-DD)

**Returns:**
```python
{
    "transits": {
        "sun": {"sign": "Capricorn", "degree": 10.5, "house": 3},
        "moon": {"sign": "Taurus", "degree": 18.2, "house": 6},
        # ... all 10 planets in transit positions
    },
    "aspects_to_natal": [
        {
            "transit_planet": "jupiter",
            "natal_planet": "sun",
            "type": "conjunction",
            "degree": 0.5,
            "orb": 3
        },
        # ... all aspects
    ],
    "moon_phase": "waxing_gibbous",
    "moon_phase_degree": 135.5
}
```

##### `calculate_g_code_intensity(transit_data)`
Calculates G-Code intensity score (1-100).

**Algorithm:**
1. Count major aspects (conjunction, opposition, trine, square)
2. Apply weights:
   - Conjunction: 1.5x
   - Opposition: 1.3x
   - Square: 1.2x
   - Trine: 1.0x
   - Sextile: 0.7x
3. Consider outer planet involvement (Saturn, Uranus, Neptune, Pluto)
4. Calculate moon phase intensity
5. Return score 1-100

**Returns:**
```python
{
    "score": 78,
    "intensity_level": "high",  # low/medium/high/intense
    "major_aspects_count": 5,
    "outer_planet_aspects": 2
}
```

##### `calculate_placidus_houses(birth_data, ascendant_degree)`
Calculates Placidus house system.

**Parameters:**
- `birth_data` - Birth information
- `ascendant_degree` - Ascendant degree

**Returns:**
```python
{
    "1": {"sign": "Aries", "cusp": 0.0},
    "2": {"sign": "Taurus", "cusp": 30.5},
    # ... all 12 houses
}
```

##### `calculate_natal_wheel_data(natal_chart)`
Calculates data structure for D3.js natal wheel visualization.

**Returns:**
```python
{
    "planets": [
        {"name": "Sun", "sign": "Leo", "degree": 135.5, "color": "#FFD700"},
        # ... all planets
    ],
    "houses": [
        {"number": 1, "cusp": 215.5, "sign": "Scorpio"},
        # ... all 12 houses
    ],
    "aspects": [
        {"from": "sun", "to": "moon", "type": "trine", "color": "#00FF00"},
        # ... all aspects
    ]
}
```

---

### 2. AI Client Services

#### Production Gemini Client (`gemini_client.py`)
**Uses Google Generative AI API.**

**Requirements:**
- Valid Google API key
- `google-generativeai` package
- Internet connection

#### Mock Gemini Client (`mock_gemini_client.py`)
**Deterministic mock for development.**

**Purpose:**
- Full-featured replacement for Gemini API
- No API key required
- Deterministic, context-aware responses
- Template-based generation

**Key Functions:**

##### `generate_daily_gcode(transit_data, natal_chart, user_preferences)`
Generates AI interpretation of daily G-Code.

**Parameters:**
- `transit_data` - Transit calculation result
- `natal_chart` - User's natal chart
- `user_preferences` - User's tone preference (witty, mystical, practical)

**Returns:**
```python
{
    "themes": ["creativity", "emotional_depth", "spiritual_growth"],
    "interpretation": "Today brings a harmonious trine between...",
    "affirmation": "I embrace my creative power and trust my intuition.",
    "guidance": "Focus on artistic pursuits and emotional expression...",
    "keywords": ["transformation", "intuition", "creativity"]
}
```

##### `generate_spiritual_patch_note(gcode_data, platform, tone)`
Generates social media content.

**Parameters:**
- `gcode_data` - G-Code calculation and interpretation
- `platform` - Target platform (twitter, instagram, linkedin)
- `tone` - Content tone

**Returns:**
```python
{
    "title": "Today's Cosmic Weather",
    "body": "🌙 Moon in Taurus + Sun in Capricorn = Practical Magic ✨\n\nToday's G-Code...",
    "hashtags": ["#SpiritualGCode", "#Astrology", "#DailyGuidance"],
    "character_count": 280,
    "emoji_suggestions": ["🌙", "✨", "🔮"]
}
```

---

### 3. Orchestration Service

#### Daily G-Code Service (`daily_gcode_service.py`)
**High-level orchestration of calculations and AI generation.**

**Purpose:**
- Coordinates calculator and AI client
- Provides complete daily G-Code workflow
- Handles errors gracefully

**Key Functions:**

##### `calculate_daily_gcode_for_user(user, target_date=None)`
Calculates complete daily G-Code for a user.

**Workflow:**
1. Fetch user's natal chart
2. Calculate transits for target date
3. Calculate G-Code intensity score
4. Generate AI interpretation
5. Package complete result

**Returns:**
```python
{
    "date": "2026-01-15",
    "g_code_score": 78,
    "intensity_level": "high",
    "themes": ["creativity", "transformation"],
    "natal_data": {...},
    "transit_data": {...},
    "interpretation": {...},
    "generated_at": "2026-01-15T10:30:00Z"
}
```

##### `calculate_weekly_forecast(user, start_date)`
Calculates 7-day forecast.

**Returns:**
```python
{
    "week_start": "2026-01-15",
    "week_end": "2026-01-21",
    "daily_forecasts": [
        {"date": "2026-01-15", "g_code_score": 78, ...},
        # ... 7 days
    ],
    "weekly_theme": "Transformation and Growth",
    "peak_day": "2026-01-18"
}
```

##### `generate_spiritual_patch_note(user, platform, tone)`
Generates social media content.

**Returns:**
```python
{
    "content": {...},
    "scheduled_for": "2026-01-15T09:00:00Z",
    "platform": platform,
    "status": "draft"
}
```

---

## Prompt Templates

### Daily G-Code Prompt (`prompts/daily_gcode.txt`)
Template for daily G-Code interpretation.

**Variables:**
- `{user_sun_sign}` - User's sun sign
- `{transit_planets}` - Current transit positions
- `{aspects}` - Major aspects
- `{intensity_level}` - Calculated intensity
- `{moon_phase}` - Current moon phase

### Spiritual Patch Note Prompt (`prompts/spiritual_patch_note.txt`)
Template for social media content generation.

**Variables:**
- `{platform}` - Target platform
- `{character_limit}` - Platform character limit
- `{themes}` - Daily themes
- `{interpretation}` - AI interpretation
- `{hashtags}` - Suggested hashtags

### Weekly Forecast Prompt (`prompts/weekly_forecast.txt`)
Template for weekly forecast generation.

**Variables:**
- `{week_start}` - Week start date
- `{week_end}` - Week end date
- `{daily_themes}` - Array of daily themes
- `{peak_intensity}` - Highest intensity day

---

## Configuration

### Environment Variables

Set in `.env` file:

```bash
# AI Configuration
AI_ENGINE=mock  # Options: mock, production
GEMINI_API_KEY=your_gemini_api_key  # Required for production

# Calculator Configuration
CALCULATOR_MODE=mock  # Options: mock, production
EPHEMERIS_PATH=/path/to/ephemeris  # Required for production
```

---

## Usage Examples

### Calculate Daily G-Code

```python
from ai_engine.daily_gcode_service import calculate_daily_gcode_for_user
from api.models import GCodeUser

user = GCodeUser.objects.get(pk=1)
result = calculate_daily_gcode_for_user(user, target_date="2026-01-15")

print(f"G-Code Score: {result['g_code_score']}")
print(f"Intensity: {result['intensity_level']}")
print(f"Themes: {', '.join(result['themes'])}")
```

### Generate Social Media Content

```python
from ai_engine.daily_gcode_service import generate_spiritual_patch_note

content = generate_spiritual_patch_note(
    user=user,
    platform="twitter",
    tone="witty"
)

print(f"Title: {content['content']['title']}")
print(f"Body: {content['content']['body']}")
print(f"Hashtags: {content['content']['hashtags']}")
```

### Calculate Weekly Forecast

```python
from ai_engine.daily_gcode_service import calculate_weekly_forecast

forecast = calculate_weekly_forecast(user, start_date="2026-01-15")

print(f"Weekly Theme: {forecast['weekly_theme']}")
print(f"Peak Day: {forecast['peak_day']}")

for day in forecast['daily_forecasts']:
    print(f"{day['date']}: Score {day['g_code_score']}")
```

---

## Development Workflow

### Using Mock Engine (Default)

```python
# Set in settings.py or environment
CALCULATOR_MODE = "mock"
AI_ENGINE = "mock"

# No additional setup required
# Works offline with deterministic results
```

### Using Production Engine

```python
# Set in settings.py or environment
CALCULATOR_MODE = "production"
AI_ENGINE = "production"

# Requires:
# 1. PyEphem installation (C++ compiler)
# 2. Valid Gemini API key
# 3. Internet connection for API calls
```

---

## Testing

Calculator tests are in `tests/test_calculator.py`.

```bash
# Run calculator tests
pytest tests/test_calculator.py -v

# Test mock calculator
pytest tests/test_calculator.py -k "mock" -v

# Test production calculator (requires dependencies)
pytest tests/test_calculator.py -k "production" -v
```

---

## Performance Considerations

### Mock Calculator
- **Speed:** Instant (< 10ms per calculation)
- **Memory:** Minimal
- **Network:** None required
- **Best for:** Development, testing, offline operation

### Production Calculator
- **Speed:** Fast (~100-500ms per calculation)
- **Memory:** Moderate
- **Network:** Required for AI API calls
- **Best for:** Production, accuracy required

---

## Error Handling

### Calculator Errors
```python
try:
    natal_chart = calculate_natal_chart(birth_data)
except InvalidBirthDataError as e:
    # Handle invalid birth data
    pass
except CalculationError as e:
    # Handle calculation failures
    pass
```

### AI Client Errors
```python
try:
    interpretation = generate_daily_gcode(transit_data, natal_chart)
except APIKeyError:
    # Handle missing API key
    pass
except RateLimitError:
    # Handle API rate limits
    pass
except ContentGenerationError:
    # Handle generation failures
    pass
```

---

## Future Enhancements

1. **Additional House Systems:** Koch, Porphyry, Whole Sign
2. **Asteroid Calculations:** Chiron, Ceres, Pallas, Juno, Vesta
3. **Lunar Nodes:** North and South node calculations
4. **Planetary Hours:** Exact planetary hour timing
5. **Eclipse Detection:** Solar and lunar eclipse calculations
6. **Retrograde Calculations:** Mercury and other planetary retrogrades
7. **Progressed Charts:** Secondary progressed chart calculations
8. **Solar Return:** Annual solar return calculations
9. **Synastry:** Relationship compatibility calculations
10. **Composite Charts:** Relationship composite charts

---

## Related Documentation

- [API Application](../api/README_API_Application.md) - API endpoints that use AI Engine
- [Technical Architecture](../docs/TECHNICAL_ARCHITECTURE.md) - System architecture
- [Scripts](../scripts/README_Scripts.md) - Automated calculation scripts

---

**Last Updated:** 2026-01-15
