#!/usr/bin/env python3
"""Test the aggregation logic with a simple case."""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TESTING AGGREGATION LOGIC")
print("=" * 80)

# Simple test: 4 identical items that should fit on 2 identical boards
request_data = {
    'items': [
        {
            'id': 'PART-A',
            'name': 'Part A',
            'code': 'PART-A',
            'width': 600,
            'height': 400,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 4,  # 4 identical parts
            'rotatable': False
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
        }
    ],
    'parameters': {
        'kerf': 3.5,
        'utilizationThreshold': 0.78,
        'timeLimit': 10.0
    }
}

print("\nTest: 4 identical 600x400 parts")
print("Expected: 2 boards with 2 parts each (identical layout)")
print("Expected aggregation: 1 group with quantity=2")
print("=" * 80)

response = requests.post(
    f"{BASE_URL}/api/solve",
    json=request_data,
    timeout=15
)

if response.status_code == 200:
    solution = response.json()

    print("\n✓ API request successful!")
    print(f"\nMetadata:")
    print(f"  Bins used: {solution['metadata']['binsUsed']}")
    print(f"  Utilization: {solution['metadata']['utilization']*100:.1f}%")

    print(f"\nBins in response: {len(solution.get('bins', []))}")

    if solution.get('bins'):
        for i, bin_group in enumerate(solution['bins'], 1):
            print(f"\nGroup {i}:")
            print(f"  Quantity: {bin_group.get('quantity', '?')}")
            print(f"  Material: {bin_group.get('material')}")
            print(f"  Dimensions: {bin_group.get('height')} x {bin_group.get('width')}")
            print(f"  Items on board: {len(bin_group.get('items', []))}")
            print(f"  Utilization: {bin_group.get('utilization', 0)*100:.1f}%")

            if bin_group.get('items'):
                print(f"  Parts:")
                for item in bin_group['items']:
                    print(f"    - {item['itemId']} at ({item['x']}, {item['y']})")

        print("\n" + "=" * 80)
        print("VERIFICATION:")
        print("=" * 80)

        # Check if we got the expected aggregation
        if len(solution['bins']) == 1:
            group = solution['bins'][0]
            if group.get('quantity') == 2:
                print("✅ PASS: Got 1 group with quantity=2 (2 identical boards)")
            else:
                print(f"❌ FAIL: Expected quantity=2, got {group.get('quantity')}")
        else:
            print(f"❌ FAIL: Expected 1 aggregated group, got {len(solution['bins'])} groups")

        print("=" * 80)

    if solution.get('unplaced'):
        print("\nUnplaced items:")
        for unplaced in solution['unplaced']:
            print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
