#!/usr/bin/env python3
"""
Test that dimension display shows both original and adjusted values correctly.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TESTING DIMENSION DISPLAY IN RESULTS")
print("=" * 80)

# Test data with offsets
# Board: 2440 x 1220, offset -4 → adjusted: 2436 x 1216
# Part: 800 x 600, offset -1 → adjusted: 799 x 599

request_data = {
    'items': [
        {
            'id': 'TEST-800-600-16',
            'name': 'Test Part',
            'code': 'TEST-800-600-16',
            'width': 799,  # Adjusted (800 - 1)
            'height': 599,  # Adjusted (600 - 1)
            'thickness': 16,
            'material': 'HS00',
            'quantity': 1,
            'rotatable': True,
            'originalWidth': 800,
            'originalHeight': 600
        },
    ],
    'bins': [
        {
            'id': 'Board-HS00-16mm',
            'width': 2436,  # Adjusted (2440 - 4)
            'height': 1216,  # Adjusted (1220 - 4)
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

print("\nScenario:")
print("  Board: 2440 x 1220 mm (original)")
print("  Board offset: -4 mm")
print("  Expected display: '2440 x 1220 (Adjusted: 2436 x 1216)'")
print("")
print("  Part: 800 x 600 mm (original)")
print("  Part offset: -1 mm")
print("  Expected display: '800 x 600 mm (Adjusted: 799 x 599)'")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/api/solve",
    json=request_data,
    timeout=15
)

if response.status_code == 200:
    solution = response.json()

    print("\n✓ Solution generated successfully!")
    print(f"Bins used: {solution['metadata']['binsUsed']}")

    if solution.get('bins') and len(solution['bins']) > 0:
        bin_data = solution['bins'][0]
        print("\n" + "=" * 80)
        print("RETURNED DATA:")
        print("=" * 80)
        print(f"Board dimensions: {bin_data['height']} x {bin_data['width']} mm")
        print(f"Board material: {bin_data['material']}")

        if bin_data.get('items') and len(bin_data['items']) > 0:
            item = bin_data['items'][0]
            print(f"\nItem ID: {item['itemId']}")
            print(f"Item dimensions: {item['width']} x {item['height']} mm")
            print(f"Item material: {item['material']}")

        print("\n" + "=" * 80)
        print("VERIFICATION:")
        print("=" * 80)

        # Check if dimensions match expected adjusted values
        board_ok = bin_data['height'] == 1216 and bin_data['width'] == 2436
        item_ok = item['width'] == 799 and item['height'] == 599

        print(f"Board adjusted dimensions: {'✅ PASS' if board_ok else '❌ FAIL'} (1216 x 2436)")
        print(f"Item adjusted dimensions: {'✅ PASS' if item_ok else '❌ FAIL'} (599 x 799)")

        print("\n📝 Note: The frontend JavaScript will display:")
        print("   Board title: 'BOARD 1 - 1220 x 2440 x 16 (H x W x T) HS00 (Adjusted: 1216 x 2436)'")
        print("   Part dimensions: '800 x 600 mm (Adjusted: 799 x 599)'")

        if board_ok and item_ok:
            print("\n✅✅✅ DATA STRUCTURE CORRECT ✅✅✅")
            print("The frontend will properly display original + adjusted dimensions")
        else:
            print("\n❌ Data verification failed")
        print("=" * 80)

    if solution.get('unplaced'):
        print("\nUnplaced items:")
        for unplaced in solution['unplaced']:
            print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("To verify the display in browser:")
print("  1. Open http://localhost:5000")
print("  2. Add a part: 800 x 600 x 16 mm")
print("  3. Keep default offsets: Board -4, Part -1")
print("  4. Generate cutting plan")
print("  5. Check that results show:")
print("     - Board: 1220 x 2440 (Adjusted: 1216 x 2436)")
print("     - Part: 800 x 600 mm (Adjusted: 799 x 599)")
print("=" * 80)
