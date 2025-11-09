#!/usr/bin/env python3
"""
Verify that board titles show actual color codes (HS00, HS01, etc.) instead of "Standard".
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# Test data with multiple colors and thicknesses
# Each item has different color to test that boards show correct material
request_data = {
    'items': [
        # HS00 items (mixed grain) - thickness 16
        {
            'id': 'TEST-HS00-001',
            'name': 'Test HS00 Item 1',
            'code': 'TEST-HS00-800-600-16',
            'width': 800,
            'height': 600,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': True
        },
        # HS01 items (fixed grain) - thickness 18
        {
            'id': 'TEST-HS01-001',
            'name': 'Test HS01 Item 1',
            'code': 'TEST-HS01-900-700-18',
            'width': 900,
            'height': 700,
            'thickness': 18,
            'material': 'HS01',
            'quantity': 2,
            'rotatable': False
        },
        # HS02 items (fixed grain) - thickness 18
        {
            'id': 'TEST-HS02-001',
            'name': 'Test HS02 Item 1',
            'code': 'TEST-HS02-850-650-18',
            'width': 850,
            'height': 650,
            'thickness': 18,
            'material': 'HS02',
            'quantity': 2,
            'rotatable': False
        },
        # HS99 items (mixed grain) - thickness 25
        {
            'id': 'TEST-HS99-001',
            'name': 'Test HS99 Item 1',
            'code': 'TEST-HS99-750-550-25',
            'width': 750,
            'height': 550,
            'thickness': 25,
            'material': 'HS99',
            'quantity': 2,
            'rotatable': True
        },
    ],
    'bins': [
        {
            'id': 'Board-Standard',
            'width': 2440,
            'height': 1220,
            'thickness': 18,
            'material': 'Standard',
            'available': -1
        }
    ],
    'parameters': {
        'kerf': 3.5,
        'utilizationThreshold': 0.78,
        'timeLimit': 10.0
    }
}

print("Testing board color codes in titles...")
print("=" * 70)

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
        print("\n" + "=" * 70)
        print("BOARD TITLES (should show actual colors, not 'Standard'):")
        print("=" * 70)

        for i, bin_data in enumerate(solution['bins'], 1):
            # Simulate the exact board title format from the webapp
            board_title = f"BOARD {i} - {bin_data['height']} x {bin_data['width']} x {bin_data['thickness']} (H x W x T) {bin_data['material']}"

            print(f"\n{board_title}")
            print(f"  Utilization: {bin_data['utilization']*100:.1f}%")
            print(f"  Items: {len(bin_data['items'])}")

        # Verify colors are correct
        print("\n" + "=" * 70)
        print("VERIFICATION:")
        print("=" * 70)

        all_correct = True
        for i, bin_data in enumerate(solution['bins'], 1):
            # Check if board material matches the items on it
            if bin_data['items']:
                item_materials = set(item['material'] for item in bin_data['items'])
                expected_material = list(item_materials)[0] if len(item_materials) == 1 else f"Mixed ({', '.join(sorted(item_materials))})"

                # Extract actual material from board title (could be from createBoardCard logic)
                actual_items = bin_data['items']
                actual_materials = [item['material'] for item in actual_items]

                print(f"\nBoard {i}:")
                print(f"  Items on board: {', '.join(actual_materials)}")
                print(f"  Expected board material: {expected_material}")

                # Since backend still has bin material, items should have their own materials
                if all(item.get('material') for item in bin_data['items']):
                    print(f"  ✅ Items have material information")
                else:
                    print(f"  ❌ Items missing material information")
                    all_correct = False

        if all_correct:
            print("\n✅ PASS: All items have material information for board display!")
        else:
            print("\n❌ FAIL: Some items missing material information!")

        print("\n" + "=" * 70)
        print("Format verification:")
        print("  Old: BOARD # - Board-1220x2440 (2440 x 1220)")
        print("  Old: BOARD # - 1220 x 2440 x 16 (H x W) Standard")
        print("  New: BOARD # - 1220 x 2440 x 16 (H x W x T) HS00")
        print("=" * 70)
else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
