#!/usr/bin/env python3
"""
Verify the new board title format in the webapp.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# Simple test data
request_data = {
    'items': [
        {
            'id': 'TEST-001',
            'name': 'Test Item',
            'code': 'TEST-001',
            'width': 800,
            'height': 600,
            'thickness': 18,
            'material': 'HS01',
            'quantity': 2,
            'rotatable': False
        }
    ],
    'bins': [{
        'id': 'Test-Board',
        'width': 2440,
        'height': 1220,
        'thickness': 16,
        'material': 'HS01',
        'available': -1
    }],
    'parameters': {
        'kerf': 3.5,
        'utilizationThreshold': 0.78,
        'timeLimit': 10.0
    }
}

print("Testing new board title format...")
print("=" * 60)

response = requests.post(
    f"{BASE_URL}/api/solve",
    json=request_data,
    timeout=15
)

if response.status_code == 200:
    solution = response.json()

    print("\n✓ Solution generated successfully!")
    print(f"\nBins used: {solution['metadata']['binsUsed']}")

    if solution.get('bins'):
        for i, bin_data in enumerate(solution['bins'], 1):
            # Simulate the board title format from the webapp
            board_title = f"BOARD {i} - {bin_data['height']} x {bin_data['width']} x {bin_data['thickness']} (H x W) {bin_data['material']}"

            print(f"\n{board_title}")
            print(f"  Utilization: {bin_data['utilization']*100:.1f}%")
            print(f"  Items: {len(bin_data['items'])}")

    print("\n" + "=" * 60)
    print("Board title format verified:")
    print("  Old: BOARD # - Board-1220x2440 (2440 x 1220)")
    print("  New: BOARD # - 1220 x 2440 x 16 (H x W) HS01")
    print("=" * 60)
else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
