"""
Test script for Daily G-Code Service.
Tests the complete flow: calculator -> AI client -> service
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from ai_engine.daily_gcode_service import get_daily_gcode_service


def test_daily_gcode_service():
    """Test the complete daily G-Code service."""
    print("=" * 70)
    print("Testing Daily G-Code Service")
    print("=" * 70)
    print()

    # Create a mock user object
    class MockUser:
        def __init__(self):
            self.username = "test_user"
            self.birth_date = date(1990, 1, 15)
            self.birth_time = "14:30"
            self.birth_location = "Taipei, Taiwan"
            self.timezone = "Asia/Taipei"
            self.preferred_tone = "inspiring"

    user = MockUser()

    print("-" * 70)
    print("Test 1: Calculate Daily G-Code")
    print("-" * 70)
    print()
    print(f"User: {user.username}")
    print(f"Birth Date: {user.birth_date}")
    print(f"Birth Location: {user.birth_location}")
    print()

    try:
        # Get service
        service = get_daily_gcode_service()
        print("[OK] Service initialized")
        print()

        # Calculate daily G-Code
        daily_gcode = service.calculate_daily_gcode_for_user(user=user)

        print("[OK] Daily G-Code calculated successfully")
        print()
        print(f"  Date: {daily_gcode['transit_date']}")
        print(f"  G-Code Score: {daily_gcode['g_code_score']}/100")
        print(f"  Intensity Level: {daily_gcode['intensity_level'].title()}")
        print()
        print("  Natal Configuration:")
        print(f"    Sun Sign: {daily_gcode['natal_chart']['sun_sign']}")
        print(f"    Moon Sign: {daily_gcode['natal_chart']['moon_sign']}")
        print(f"    Ascendant: {daily_gcode['natal_chart']['ascendant']}")
        print()
        print("  Themes:")
        for theme in daily_gcode['themes']:
            print(f"    - {theme}")
        print()
        print("  Interpretation (first 200 chars):")
        interpretation = daily_gcode['interpretation']
        print(f"    {interpretation[:200]}...")
        print()
        print("  Affirmation:")
        print(f"    {daily_gcode['affirmation']}")
        print()
        print("  Practical Guidance:")
        for i, guidance in enumerate(daily_gcode['practical_guidance'], 1):
            print(f"    {i}. {guidance}")

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    print()
    print("-" * 70)
    print("Test 2: Generate Social Media Content")
    print("-" * 70)
    print()

    try:
        # Generate Twitter content
        twitter_content = service.generate_spiritual_patch_note(
            daily_gcode=daily_gcode,
            platform='twitter'
        )

        print("[OK] Twitter content generated")
        print()
        print(f"  Title: {twitter_content['title']}")
        print(f"  Platform: {twitter_content['platform']}")
        print()
        print("  Content:")
        print("  " + "-" * 66)
        for line in twitter_content['body'].split('\n'):
            print(f"  {line}")
        print("  " + "-" * 66)
        print()

        # Generate Instagram content
        instagram_content = service.generate_spiritual_patch_note(
            daily_gcode=daily_gcode,
            platform='instagram'
        )

        print("[OK] Instagram content generated")
        print()
        print(f"  Content length: {len(instagram_content['body'])} chars")
        print()

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print()
    print("=" * 70)
    print("[OK] All Tests Passed!")
    print("=" * 70)
    print()
    print("The Daily G-Code Service is ready for integration!")
    print()

    return True


if __name__ == "__main__":
    success = test_daily_gcode_service()
    sys.exit(0 if success else 1)
