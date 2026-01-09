"""
Standalone test script for Daily G-Code Service.
Tests without requiring Django models.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from ai_engine.mock_calculator import MockGCodeCalculator
from ai_engine.mock_gemini_client import MockGeminiGCodeClient


def test_daily_gcode_flow():
    """Test the daily G-Code flow without Django."""
    print("=" * 70)
    print("Testing Daily G-Code (Standalone)")
    print("=" * 70)
    print()

    # User data
    user_data = {
        'username': 'test_user',
        'birth_date': date(1990, 1, 15),
        'birth_time': '14:30',
        'birth_location': 'Taipei, Taiwan',
        'timezone': 'Asia/Taipei',
        'preferred_tone': 'inspiring'
    }

    print("-" * 70)
    print("Test 1: Calculate Natal Chart")
    print("-" * 70)
    print()

    try:
        calculator = MockGCodeCalculator()
        print("[OK] Calculator initialized")

        # Calculate natal chart
        natal_chart = calculator.calculate_natal_chart(
            birth_date=user_data['birth_date'],
            birth_time=user_data['birth_time'],
            birth_location=user_data['birth_location'],
            timezone=user_data['timezone']
        )

        print("[OK] Natal chart calculated")
        print()
        print(f"  Sun Sign: {natal_chart['sun_sign']}")
        print(f"  Moon Sign: {natal_chart['moon_sign']}")
        print(f"  Ascendant: {natal_chart['ascendant']}")
        print()

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print("-" * 70)
    print("Test 2: Calculate Transits")
    print("-" * 70)
    print()

    try:
        target_date = date.today()
        transits = calculator.calculate_transits(
            birth_date=user_data['birth_date'],
            birth_time=user_data['birth_time'],
            birth_location=user_data['birth_location'],
            target_date=target_date
        )

        print("[OK] Transits calculated")
        print()
        print(f"  Target Date: {target_date}")
        print(f"  Transit Aspects: {len(transits['aspects'])}")
        print()

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print("-" * 70)
    print("Test 3: Generate AI Interpretation")
    print("-" * 70)
    print()

    try:
        ai_client = MockGeminiGCodeClient()
        print("[OK] AI client initialized")

        # Generate interpretation
        interpretation = ai_client.generate_daily_gcode(
            natal_data=natal_chart,
            transit_data=transits,
            user_preferences={'tone': 'inspiring'}
        )

        print("[OK] AI interpretation generated")
        print()
        print(f"  G-Code Score: {interpretation['g_code_score']}/100")
        print()
        print("  Themes:")
        for theme in interpretation['themes']:
            print(f"    - {theme}")
        print()
        print("  Affirmation:")
        print(f"    {interpretation['affirmation']}")
        print()
        print("  Practical Guidance:")
        for i, guidance in enumerate(interpretation['practical_guidance'], 1):
            print(f"    {i}. {guidance}")
        print()

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("-" * 70)
    print("Test 4: Generate Social Media Content")
    print("-" * 70)
    print()

    try:
        daily_gcode = {
            'transit_date': target_date,
            'g_code_score': interpretation['g_code_score'],
            'themes': interpretation['themes'],
            'interpretation': interpretation['interpretation']
        }

        # Twitter content
        twitter_content = ai_client.generate_spiritual_patch_note(
            daily_gcode=daily_gcode,
            platform='twitter'
        )

        print("[OK] Twitter content generated")
        print()
        print("  Content:")
        for line in twitter_content['body'].split('\n'):
            print(f"    {line}")
        print()

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print()
    print("=" * 70)
    print("[OK] All Tests Passed!")
    print("=" * 70)
    print()
    print("The complete G-Code flow is working!")
    print("  Calculator -> Transits -> AI -> Content")
    print()

    return True


if __name__ == "__main__":
    success = test_daily_gcode_flow()
    sys.exit(0 if success else 1)
