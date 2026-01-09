"""
Test script for Mock G-Code Calculator.
Run this to verify the calculator is working correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from ai_engine.mock_calculator import MockGCodeCalculator


def test_calculator():
    """Test the mock calculator with sample data."""
    print("=" * 60)
    print("Testing Mock G-Code Calculator")
    print("=" * 60)
    print()

    # Initialize calculator
    calc = MockGCodeCalculator()
    print("[OK] Calculator initialized")
    print()

    # Test 1: Calculate Natal Chart
    print("-" * 60)
    print("Test 1: Calculate Natal Chart")
    print("-" * 60)

    test_birth_date = date(1990, 1, 15)
    test_birth_time = "14:30"
    test_location = "Taipei, Taiwan"

    print(f"Birth Date: {test_birth_date}")
    print(f"Birth Time: {test_birth_time}")
    print(f"Location: {test_location}")
    print()

    try:
        natal_chart = calc.calculate_natal_chart(
            birth_date=test_birth_date,
            birth_time=test_birth_time,
            birth_location=test_location
        )

        print("[OK] Natal Chart Calculation Successful")
        print()
        print(f"   Sun Sign: {natal_chart['sun_sign']}")
        print(f"   Moon Sign: {natal_chart['moon_sign']}")
        print(f"   Ascendant: {natal_chart['ascendant']}")
        print()
        print("   Planetary Positions:")
        for planet, data in natal_chart['chart_data'].items():
            print(f"      {planet.capitalize():10} -> {data['sign']:12} ({data['degree']:5.2f}°)")

        print()
        print("   Dominant Elements:")
        for element, percentage in natal_chart['dominant_elements'].items():
            print(f"      {element.capitalize():8}: {percentage}%")

        print()
        print(f"   Key Aspects Found: {len(natal_chart['key_aspects'])}")
        for aspect in natal_chart['key_aspects'][:5]:  # Show first 5
            print(f"      - {aspect['planet1']} {aspect['aspect']} {aspect['planet2']} (orb: {aspect['orb']}°)")

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print()

    # Test 2: Calculate Transits
    print("-" * 60)
    print("Test 2: Calculate Transits for Today")
    print("-" * 60)

    target_date = date.today()
    print(f"Target Date: {target_date}")
    print()

    try:
        transits = calc.calculate_transits(
            birth_date=test_birth_date,
            birth_time=test_birth_time,
            birth_location=test_location,
            target_date=target_date
        )

        print("[OK] Transit Calculation Successful")
        print()
        print("   Current Planetary Positions:")
        for planet, data in transits['planets'].items():
            print(f"      {planet.capitalize():10} -> {data['sign']:12} ({data['degree']:5.2f}°)")

        print()
        print(f"   Transit Aspects Found: {len(transits['aspects'])}")
        for aspect in transits['aspects'][:5]:  # Show first 5
            print(f"      - Transit {aspect['transit_planet']} {aspect['aspect']} Natal {aspect['natal_planet']}")

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print()

    # Test 3: Calculate G-Code Intensity
    print("-" * 60)
    print("Test 3: Calculate G-Code Intensity Score")
    print("-" * 60)

    try:
        intensity = calc.calculate_g_code_intensity(
            transit_data=transits['planets'],
            aspects=transits['aspects']
        )

        print(f"[OK] G-Code Intensity Score: {intensity}/100")
        print()

        # Determine intensity level
        if intensity < 25:
            level = "Low"
        elif intensity < 50:
            level = "Medium"
        elif intensity < 75:
            level = "High"
        else:
            level = "Intense"

        print(f"   Intensity Level: {level}")

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print()

    # Test 4: Reproducibility Check
    print("-" * 60)
    print("Test 4: Reproducibility Check")
    print("-" * 60)
    print("Testing if same inputs produce same outputs...")
    print()

    try:
        natal_chart2 = calc.calculate_natal_chart(
            birth_date=test_birth_date,
            birth_time=test_birth_time,
            birth_location=test_location
        )

        if natal_chart['sun_sign'] == natal_chart2['sun_sign']:
            print("[OK] Results are reproducible (same sun sign)")
        else:
            print("[FAIL] Results differ - this should not happen!")
            return False

    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

    print()
    print("=" * 60)
    print("[OK] All Tests Passed!")
    print("=" * 60)
    print()
    print("The Mock G-Code Calculator is ready for use!")
    print()

    return True


if __name__ == "__main__":
    success = test_calculator()
    sys.exit(0 if success else 1)
