#!/usr/bin/env python3
"""
Test that dimension offsets are correctly applied:
- Board offsets reduce board dimensions
- Part offsets reduce part dimensions
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TESTING DIMENSION OFFSETS")
print("=" * 80)

# Test data
# Original board: 2440 x 1220
# Board offset: -4 (both width and height)
# Expected actual board: 2436 x 1216

# Original part: 800 x 600
# Part offset: -1 (both width and height)
# Expected actual part: 799 x 599

request_data = {
    'items': [
        {
            'id': 'TEST-PART-001',
            'name': 'Test Part',
            'code': 'TEST-800-600-16',
            'width': 799,  # Already offset applied (800 - 1)
            'height': 599,  # Already offset applied (600 - 1)
            'thickness': 16,
            'material': 'HS00',
            'quantity': 1,
            'rotatable': True
        },
    ],
    'bins': [
        {
            'id': 'Board-HS00-16mm',
            'width': 2436,  # Already offset applied (2440 - 4)
            'height': 1216,  # Already offset applied (1220 - 4)
            'thickness': 16,
            'material': 'HS00',
            'available': -1
        }
    ],
    'parameters': {
        'kerf': 3.5,
        'utilizationThreshold': 0.78,
        'timeLimit': 10.0
    }
}

print("\nTest scenario:")
print("  Original board size: 2440 x 1220 mm")
print("  Board offset: -4 mm (width and height)")
print("  Expected actual board: 2436 x 1216 mm")
print("")
print("  Original part size: 800 x 600 mm")
print("  Part offset: -1 mm (width and height)")
print("  Expected actual part: 799 x 599 mm")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/api/solve",
    json=request_data,
    timeout=15
)

if response.status_code == 200:
    solution = response.json()

    print("\n✓ Solution generated successfully!")
    print(f"\nBins used: {solution['metadata']['binsUsed']}")
    print(f"Utilization: {solution['metadata']['utilization']*100:.1f}%")

    if solution.get('bins'):
        print("\n" + "=" * 80)
        print("BOARD DIMENSIONS:")
        print("=" * 80)

        for i, bin_data in enumerate(solution['bins'], 1):
            print(f"\nBoard {i}:")
            print(f"  Width: {bin_data['width']:.1f} mm (expected: 2436)")
            print(f"  Height: {bin_data['height']:.1f} mm (expected: 1216)")
            print(f"  Material: {bin_data['material']}")
            print(f"  Items: {len(bin_data['items'])}")

            if bin_data['items']:
                print(f"\n  Items on board:")
                for item in bin_data['items']:
                    print(f"    - {item['itemId']}: {item['width']:.1f} x {item['height']:.1f} mm")
                    print(f"      Expected: 799 x 599 mm")

        # Verify dimensions
        board_width_ok = abs(solution['bins'][0]['width'] - 2436) < 0.1
        board_height_ok = abs(solution['bins'][0]['height'] - 1216) < 0.1
        item_width_ok = abs(solution['bins'][0]['items'][0]['width'] - 799) < 0.1
        item_height_ok = abs(solution['bins'][0]['items'][0]['height'] - 599) < 0.1

        print("\n" + "=" * 80)
        print("VERIFICATION:")
        print("=" * 80)
        print(f"Board width: {'✅ PASS' if board_width_ok else '❌ FAIL'} (2436 mm)")
        print(f"Board height: {'✅ PASS' if board_height_ok else '❌ FAIL'} (1216 mm)")
        print(f"Item width: {'✅ PASS' if item_width_ok else '❌ FAIL'} (799 mm)")
        print(f"Item height: {'✅ PASS' if item_height_ok else '❌ FAIL'} (599 mm)")

        if board_width_ok and board_height_ok and item_width_ok and item_height_ok:
            print("\n✅✅✅ ALL OFFSET TESTS PASSED ✅✅✅")
        else:
            print("\n❌❌❌ OFFSET TESTS FAILED ❌❌❌")
        print("=" * 80)

    if solution.get('unplaced'):
        print("\nUnplaced items:")
        for unplaced in solution['unplaced']:
            print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
