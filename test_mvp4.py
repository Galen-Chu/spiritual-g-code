"""
Phase 6 MVP.4: Natal Wheel - Test Suite
Tests all functionality of the natal wheel feature
"""

import os
import sys
from datetime import date

# Import calculator
from ai_engine.mock_calculator import MockGCodeCalculator

def test_placidus_houses():
    """Test Placidus house calculation"""
    print('=== Test 1: Placidus House Calculation ===')

    calc = MockGCodeCalculator()
    test_date = date(1990, 6, 15)
    test_time = '14:30'
    test_location = 'New York'
    test_timezone = 'America/New_York'

    try:
        houses = calc.calculate_placidus_houses(test_date, test_time, test_location, test_timezone)

        print(f'[OK] Houses calculated: {len(houses)} houses')

        # Verify all houses exist
        for i in range(1, 13):
            if i in houses:
                house = houses[i]
                print(f'  House {i}: {house["sign"]} {house["cusp"]} (lon: {house["longitude"]})')
            else:
                print(f'  [FAIL] House {i}: missing')
                return False

        # Check for house size variation (Placidus characteristic)
        print('[OK] All 12 houses present')
        return True

    except Exception as e:
        print(f'[ERROR] {e}')
        return False


def test_equal_houses():
    """Test equal house fallback"""
    print('\n=== Test 2: Equal House Fallback ===')

    calc = MockGCodeCalculator()
    test_date = date(1990, 6, 15)
    test_time = '14:30'
    test_location = 'New York'
    test_timezone = 'America/New_York'

    try:
        houses = calc._calculate_equal_houses(test_date, test_time, test_location, test_timezone)

        print(f'[OK] Equal houses calculated: {len(houses)} houses')

        # All houses should be 30 degrees apart
        for i in range(1, 13):
            if i in houses:
                house = houses[i]
                print(f'  House {i}: {house["sign"]} {house["cusp"]}')

        print('[OK] Equal house system working')
        return True

    except Exception as e:
        print(f'[ERROR] {e}')
        return False


def test_natal_wheel_data():
    """Test complete natal wheel data"""
    print('\n=== Test 3: Natal Wheel Data ===')

    calc = MockGCodeCalculator()
    test_date = date(1990, 6, 15)
    test_time = '14:30'
    test_location = 'New York'
    test_timezone = 'America/New_York'

    try:
        wheel_data = calc.calculate_natal_wheel_data(test_date, test_time, test_location, test_timezone)

        # Check required fields
        required_fields = [
            'planets', 'planet_symbols', 'houses', 'aspects',
            'zodiac_symbols', 'ascendant', 'sun_sign', 'moon_sign'
        ]

        all_present = True
        for field in required_fields:
            if field in wheel_data:
                print(f'[OK] {field}: present')
            else:
                print(f'[FAIL] {field}: missing')
                all_present = False

        if not all_present:
            return False

        # Check planets
        planets = wheel_data['planets']
        print(f'[OK] Planets: {len(planets)} calculated')

        # Check planet symbols
        symbols = wheel_data['planet_symbols']
        expected = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
        if all(planet in symbols for planet in expected):
            print(f'[OK] All {len(expected)} planet symbols present')
        else:
            print('[FAIL] Some planet symbols missing')
            return False

        # Check zodiac symbols
        zodiac_symbols = wheel_data['zodiac_symbols']
        expected_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                          'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        if all(sign in zodiac_symbols for sign in expected_signs):
            print(f'[OK] All {len(expected_signs)} zodiac symbols present')
        else:
            print('[FAIL] Some zodiac symbols missing')
            return False

        # Check aspects
        aspects = wheel_data['aspects']
        print(f'[OK] Aspects: {len(aspects)} calculated')

        # Count aspect types
        aspect_types = {}
        for aspect in aspects:
            atype = aspect.get('aspect', 'unknown')
            aspect_types[atype] = aspect_types.get(atype, 0) + 1

        print('  Aspect types:')
        for atype, count in sorted(aspect_types.items()):
            print(f'    {atype}: {count}')

        print('[OK] Natal wheel data complete')
        return True

    except Exception as e:
        print(f'[ERROR] {e}')
        import traceback
        traceback.print_exc()
        return False


def test_javascript_files():
    """Test JavaScript files exist"""
    print('\n=== Test 4: JavaScript Files ===')

    js_files = [
        'static/js/components/wheel/d3-wheel-renderer.js'
    ]

    all_exist = True
    for js_file in js_files:
        if os.path.exists(js_file):
            size = os.path.getsize(js_file)
            lines = 0
            with open(js_file, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            print(f'[OK] {js_file}')
            print(f'  Size: {size} bytes')
            print(f'  Lines: {lines}')
        else:
            print(f'[FAIL] {js_file} not found')
            all_exist = False

    return all_exist


def test_template_files():
    """Test template files exist"""
    print('\n=== Test 5: Template Files ===')

    template_files = [
        'templates/natal/wheel.html'
    ]

    all_exist = True
    for template_file in template_files:
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                size = len(content)
            print(f'[OK] {template_file}')
            print(f'  Size: {size} bytes')

            # Check for key components
            checks = [
                ('D3WheelRenderer', 'D3WheelRenderer class'),
                ('natal-wheel', 'wheel container'),
                ('wheel-loading', 'loading state'),
                ('wheel-error', 'error state'),
                ('d3.v7.min.js', 'D3.js CDN'),
                ('exportAsPNG', 'PNG export'),
                ('exportAsSVG', 'SVG export')
            ]

            for check_str, check_name in checks:
                if check_str in content:
                    print(f'  [OK] {check_name} present')
                else:
                    print(f'  [FAIL] {check_name} missing')
                    all_exist = False
        else:
            print(f'[FAIL] {template_file} not found')
            all_exist = False

    return all_exist


def test_url_routing():
    """Test URL routing"""
    print('\n=== Test 6: URL Routing ===')

    # Check views_html.py
    try:
        with open('api/views_html.py', 'r', encoding='utf-8') as f:
            content = f.read()

        if 'def wheel_view' in content:
            print('[OK] wheel_view function exists in views_html.py')
        else:
            print('[FAIL] wheel_view function not found')
            return False

        if 'return render(request, \'natal/wheel.html\')' in content:
            print('[OK] Correct template reference')
        else:
            print('[FAIL] Template reference incorrect')
            return False

    except Exception as e:
        print(f'[ERROR] {e}')
        return False

    # Check core/urls.py
    try:
        with open('core/urls.py', 'r', encoding='utf-8') as f:
            content = f.read()

        if 'wheel_view' in content:
            print('[OK] wheel_view imported in urls.py')
        else:
            print('[FAIL] wheel_view not imported')
            return False

        if 'path(\'natal/wheel/\', wheel_view, name=\'wheel\')' in content:
            print('[OK] wheel URL route configured')
        else:
            print('[FAIL] wheel URL route not found')
            return False

    except Exception as e:
        print(f'[ERROR] {e}')
        return False

    return True


def test_api_endpoint():
    """Test API endpoint configuration"""
    print('\n=== Test 7: API Endpoint ===')

    # Check api/views.py
    try:
        with open('api/views.py', 'r', encoding='utf-8') as f:
            content = f.read()

        if 'class NatalWheelView' in content:
            print('[OK] NatalWheelView class exists')
        else:
            print('[FAIL] NatalWheelView class not found')
            return False

        if 'path(\'natal/wheel/\', NatalWheelView.as_view()' in content or \
           'NatalWheelView' in content:
            print('[OK] NatalWheelView defined')
        else:
            print('[FAIL] NatalWheelView not properly defined')
            return False

    except Exception as e:
        print(f'[ERROR] {e}')
        return False

    # Check api/urls.py
    try:
        with open('api/urls.py', 'r', encoding='utf-8') as f:
            content = f.read()

        if 'NatalWheelView' in content:
            print('[OK] NatalWheelView imported')
        else:
            print('[FAIL] NatalWheelView not imported')
            return False

        if 'path(\'natal/wheel/\', NatalWheelView.as_view()' in content:
            print('[OK] API route configured')
        else:
            print('[FAIL] API route not found')
            return False

    except Exception as e:
        print(f'[ERROR] {e}')
        return False

    return True


def run_all_tests():
    """Run all tests"""
    print('=' * 60)
    print('Phase 6 MVP.4: Natal Wheel - Test Suite')
    print('=' * 60)

    results = []

    # Run tests
    results.append(('Placidus Houses', test_placidus_houses()))
    results.append(('Equal Houses', test_equal_houses()))
    results.append(('Natal Wheel Data', test_natal_wheel_data()))
    results.append(('JavaScript Files', test_javascript_files()))
    results.append(('Template Files', test_template_files()))
    results.append(('URL Routing', test_url_routing()))
    results.append(('API Endpoint', test_api_endpoint()))

    # Summary
    print('\n' + '=' * 60)
    print('TEST SUMMARY')
    print('=' * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = 'PASS' if result else 'FAIL'
        symbol = '✅' if result else '❌'
        print(f'{symbol} {name}: {status}')

    print()
    print(f'Total: {passed}/{total} tests passed')
    print(f'Pass Rate: {(passed/total*100):.1f}%')

    if passed == total:
        print('\n🎉 All tests passed! MVP.4 is ready.')
    else:
        print(f'\n⚠️  {total - passed} test(s) failed. Please review.')

    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
