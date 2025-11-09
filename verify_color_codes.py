#!/usr/bin/env python3
"""
Verify that board titles show actual color codes (HS00, HS01, etc.) instead of "Standard".
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# Test data with multiple colors and thicknesses
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
            'quantity': 1,
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
            'quantity': 1,
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
            'quantity': 1,
            'rotatable': True
        },
    ],
    'bins': [
        {
            'id': 'Board-HS00-16mm',
            'width': 2440,
            'height': 1220,
            'thickness': 16,
            'material': 'HS00',
            'available': -1
        },
        {
            'id': 'Board-HS01-18mm',
            'width': 2440,
            'height': 1220,
            'thickness': 18,
            'material': 'HS01',
            'available': -1
        },
        {
            'id': 'Board-HS02-18mm',
            'width': 2440,
            'height': 1220,
            'thickness': 18,
            'material': 'HS02',
            'available': -1
        },
        {
            'id': 'Board-HS99-25mm',
            'width': 2440,
            'height': 1220,
            'thickness': 25,
            'material': 'HS99',
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

        colors_found = set()
        for bin_data in solution['bins']:
            colors_found.add(bin_data['material'])

        print(f"\nColors found in board titles: {', '.join(sorted(colors_found))}")

        if 'Standard' in colors_found:
            print("❌ FAIL: Found 'Standard' instead of actual color codes!")
        else:
            expected_colors = {'HS00', 'HS01', 'HS02', 'HS99'}
            if colors_found.issubset(expected_colors):
                print("✅ PASS: All boards show actual color codes (no 'Standard')!")
            else:
                print(f"⚠ Warning: Unexpected colors found: {colors_found - expected_colors}")

        print("\n" + "=" * 70)
        print("Format verification:")
        print("  Old: BOARD # - Board-1220x2440 (2440 x 1220)")
        print("  Old: BOARD # - 1220 x 2440 x 16 (H x W) Standard")
        print("  New: BOARD # - 1220 x 2440 x 16 (H x W x T) HS00")
        print("=" * 70)
else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
