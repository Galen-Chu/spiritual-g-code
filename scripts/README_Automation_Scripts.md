# Automation Scripts Documentation

## Overview

The `scripts/` directory contains standalone Python scripts for automated background tasks, scheduled jobs, and testing utilities. These scripts are triggered by Django crontab or run manually for maintenance and testing.

**Technology:**
- Python 3.11+
- Django ORM
- Celery-compatible (for future async execution)

---

## Directory Structure

```
scripts/
├── calculate_daily_gcode.py       # Daily G-Code calculation (Crontab: 4:00 AM)
├── generate_patch_notes.py        # Content generation (Crontab: 5:00 AM)
├── cleanup_old_data.py            # Data cleanup (Crontab: Sundays 3:00 AM)
├── test_calculator.py             # Calculator testing script
├── test_daily_gcode.py            # Daily G-Code testing script
└── test_daily_gcode_standalone.py # Standalone integration test
```

---

## Scheduled Scripts

### 1. Daily G-Code Calculation

**File:** `calculate_daily_gcode.py`

**Purpose:** Calculates daily G-Code transits for all users with `daily_gcode_enabled=True`.

**Schedule:** 4:00 AM daily (via Django crontab)

**Workflow:**

```
1. Initialize calculator and AI client
2. Query all active users with daily_gcode_enabled=True
3. For each user:
   a. Get or create natal chart
   b. Calculate planetary transits for tomorrow
   c. Generate AI interpretation (if available)
   d. Determine intensity level (low/medium/high/intense)
   e. Save or update DailyTransit record
4. Log success/error counts
5. Send error summary email (if errors occurred)
```

**Key Functions:**

#### `calculate_all_daily_gcodes()`
Main entry point for the script.

**Process:**
- Gets tomorrow's date
- Filters users with `daily_gcode_enabled=True` and `is_active=True`
- For each user:
  - Validates natal chart exists
  - Calculates transits using `GCodeCalculator`
  - Generates AI interpretation using `GeminiGCodeClient`
  - Saves/updates `DailyTransit` record
  - Logs results

**Error Handling:**
- Falls back to generic interpretation if AI client unavailable
- Skips users without natal charts
- Logs errors and continues processing
- Sends admin email on errors

**Output:**
```python
{
    'success_count': 45,  # Number of successful calculations
    'error_count': 2      # Number of errors
}
```

**Usage:**

```bash
# Run manually (for testing)
python scripts/calculate_daily_gcode.py

# Check logs
tail -f /tmp/gcode_calc.log
```

---

### 2. Content Generation

**File:** `generate_patch_notes.py`

**Purpose:** Generates "Spiritual Patch Notes" (social media content) for users.

**Schedule:** 5:00 AM daily (via Django crontab, after G-Code calculation)

**Workflow:**

```
1. Initialize AI client
2. Query users with daily_gcode_enabled + email_notifications
3. For each user:
   a. Get today's DailyTransit
   b. Generate Twitter content
   c. Generate Instagram content (optional)
   d. Save GeneratedContent records
4. Log success/error counts
```

**Key Functions:**

#### `generate_all_patch_notes()`
Main entry point for the script.

**Process:**
- Gets today's date
- Filters users with:
  - `daily_gcode_enabled=True`
  - `is_active=True`
  - `email_notifications=True`
- For each user:
  - Retrieves today's `DailyTransit`
  - Generates Twitter content using AI client
  - Generates Instagram content using AI client
  - Creates `GeneratedContent` records

**Content Generated:**

**Twitter:**
- Character limit: 280
- Format: Compact with emojis
- Hashtags: #SpiritualGCode, #DailyGCode, etc.

**Instagram:**
- No character limit
- Format: Long-form with hashtags
- Visual suggestions included

**Usage:**

```bash
# Run manually
python scripts/generate_patch_notes.py

# Check logs
tail -f /tmp/patch_notes.log
```

---

### 3. Data Cleanup

**File:** `cleanup_old_data.py`

**Purpose:** Removes old data from database to maintain performance.

**Schedule:** Sundays at 3:00 AM (via Django crontab)

**Workflow:**

```
1. Clean up old DailyTransit records (> 90 days)
2. Clean up old SystemLog records (> 30 days)
3. Clean up old UserActivity records (> 90 days)
4. Log deletion counts
```

**Key Functions:**

#### `cleanup_old_transits(days_to_keep=90)`
Deletes transits older than specified days.

**Default:** 90 days retention

#### `cleanup_old_logs(days_to_keep=30)`
Deletes system logs older than specified days.

**Default:** 30 days retention

#### `cleanup_old_activities(days_to_keep=90)`
Deletes user activity logs older than specified days.

**Default:** 90 days retention

#### `run_all_cleanup()`
Runs all cleanup tasks in sequence.

**Usage:**

```bash
# Run manually
python scripts/cleanup_old_data.py

# Check logs
tail -f /tmp/cleanup.log
```

**Custom Retention:**

```python
# Modify retention periods in the script
cleanup_old_transits(days_to_keep=120)  # Keep 120 days
cleanup_old_logs(days_to_keep=60)       # Keep 60 days
cleanup_old_activities(days_to_keep=180) # Keep 180 days
```

---

## Test Scripts

### 4. Calculator Test

**File:** `test_calculator.py`

**Purpose:** Tests the G-Code calculator functionality.

**Tests:**
- Natal chart calculation
- Transit calculation
- Intensity scoring
- House calculation
- Aspect detection

**Usage:**

```bash
python scripts/test_calculator.py
```

---

### 5. Daily G-Code Test

**File:** `test_daily_gcode.py`

**Purpose:** Tests the daily G-Code calculation workflow.

**Tests:**
- User filtering
- Transit calculation
- AI interpretation
- Database record creation
- Error handling

**Usage:**

```bash
python scripts/test_daily_gcode.py
```

---

### 6. Standalone Integration Test

**File:** `test_daily_gcode_standalone.py`

**Purpose:** End-to-end integration test without Django test framework.

**Tests:**
- Complete workflow from user to DailyTransit
- Calculator integration
- AI client integration
- Database persistence

**Usage:**

```bash
python scripts/test_daily_gcode_standalone.py
```

---

## Django Crontab Configuration

Scripts are registered in `core/settings/base.py`:

```python
CRONJOBS = [
    # Calculate Daily G-Code at 4:00 AM every day
    ('0 4 * * *', 'scripts.calculate_daily_gcode.calculate_all_daily_gcodes', '>> /tmp/gcode_calc.log'),

    # Generate Spiritual Patch Notes at 5:00 AM every day
    ('0 5 * * *', 'scripts.generate_patch_notes.generate_all_patch_notes', '>> /tmp/patch_notes.log'),

    # Clean up old data on Sundays at 3:00 AM
    ('0 3 * * 0', 'scripts.cleanup_old_data.run_all_cleanup', '>> /tmp/cleanup.log'),
]
```

### Crontab Format

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
│ │ │ │ │
* * * * * command to be executed
```

### Crontab Examples

```python
# Daily at 4:00 AM
('0 4 * * *', 'my_script', '>> /tmp/log')

# Every hour
('0 * * * *', 'my_script', '>> /tmp/log')

# Every Monday at 9:00 AM
('0 9 * * 1', 'my_script', '>> /tmp/log')

# First of every month at midnight
('0 0 1 * *', 'my_script', '>> /tmp/log')

# Every 6 hours
('0 */6 * * *', 'my_script', '>> /tmp/log')
```

---

## Setting Up Crontab

### Development (Local)

For local development, scripts can be run manually or using Django management commands:

```bash
# Run script manually
python scripts/calculate_daily_gcode.py

# Or use Django management command (if implemented)
python manage.py calculate_gcode
```

### Production (Linux/Unix)

1. **Install django-crontab:**
   ```bash
   pip install django-crontab
   ```

2. **Add to `INSTALLED_APPS`:**
   ```python
   INSTALLED_APPS = [
       # ...
       'django_crontab',
   ]
   ```

3. **Add CRONJOBS to settings (already configured in `core/settings/base.py`)**

4. **Add crontab jobs:**
   ```bash
   python manage.py crontab add
   ```

5. **List crontab jobs:**
   ```bash
   python manage.py crontab show
   ```

6. **Remove crontab jobs:**
   ```bash
   python manage.py crontab remove
   ```

---

## Logging

All scheduled scripts log to files in `/tmp/` directory:

| Script | Log File |
|--------|----------|
| `calculate_daily_gcode.py` | `/tmp/gcode_calc.log` |
| `generate_patch_notes.py` | `/tmp/patch_notes.log` |
| `cleanup_old_data.py` | `/tmp/cleanup.log` |

### Viewing Logs

```bash
# View latest logs
tail -f /tmp/gcode_calc.log

# View all logs
cat /tmp/gcode_calc.log

# Search for errors
grep "ERROR" /tmp/gcode_calc.log
```

---

## Creating New Scripts

### Template

```python
"""
My Custom Script

Description of what this script does.
Schedule information if applicable.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

# Import Django models and services
from api.models import User
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def my_custom_function():
    """
    Description of what this function does.
    """
    logger.info("Starting custom task...")

    try:
        # Your logic here
        result = perform_task()
        logger.info(f"✅ Task completed successfully: {result}")
    except Exception as e:
        logger.error(f"❌ Task failed: {str(e)}")

    logger.info("Task complete!")


if __name__ == '__main__':
    my_custom_function()
```

### Adding to Crontab

1. Add the script to `scripts/`
2. Add to `CRONJOBS` in `core/settings/base.py`:
   ```python
   CRONJOBS = [
       # ... existing jobs
       ('0 6 * * *', 'scripts.my_custom_script.my_custom_function', '>> /tmp/my_custom.log'),
   ]
   ```
3. Update crontab:
   ```bash
   python manage.py crontab remove
   python manage.py crontab add
   ```

---

## Monitoring and Maintenance

### Check Script Status

```bash
# Check if crontab is running
python manage.py crontab show

# View recent logs
tail -20 /tmp/gcode_calc.log

# Check for errors
grep -i "error" /tmp/*.log
```

### Manual Execution

For testing or ad-hoc execution:

```bash
# Calculate G-Code manually
python scripts/calculate_daily_gcode.py

# Generate content manually
python scripts/generate_patch_notes.py

# Run cleanup manually
python scripts/cleanup_old_data.py
```

### Troubleshooting

#### Script Not Running
- Check crontab is registered: `python manage.py crontab show`
- Check cron service is running: `systemctl status cron` (Linux)
- Check log files for errors

#### Django Environment Issues
- Verify `DJANGO_SETTINGS_MODULE` is set correctly
- Check Python path includes project root
- Ensure all dependencies are installed

#### Database Connection Errors
- Verify database server is running
- Check database credentials in `.env`
- Test database connection: `python manage.py dbshell`

---

## Related Documentation

- [Django Core](../core/README_Django_Core.md) - Django project configuration
- [AI Engine](../ai_engine/README_AI_Engine.md) - Calculation and AI services
- [API Application](../api/README_API_Application.md) - Data models and API

---

**Last Updated:** 2026-01-15
