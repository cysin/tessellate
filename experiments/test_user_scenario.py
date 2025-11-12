#!/usr/bin/env python3
"""Test the exact user scenario: CB(L) x2 and CB(R) x2"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("USER SCENARIO TEST: CB(L) x2 and CB(R) x2")
print("=" * 80)

request_data = {
    'items': [
        {
            'id': 'CB(L)-HS00-2434-574-16',
            'name': 'CB(L)',
            'code': 'CB(L)-HS00-2434-574-16',
            'width': 2434,  # Corrected: width is 2434
            'height': 574,   # Corrected: height is 574
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': False
        },
        {
            'id': 'CB(R)-HS00-2434-574-16',
            'name': 'CB(R)',
            'code': 'CB(R)-HS00-2434-574-16',
            'width': 2434,  # Corrected: width is 2434
            'height': 574,   # Corrected: height is 574
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
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

print("\nInput:")
print("  - CB(L): 2434x574x16 HS00, quantity=2")
print("  - CB(R): 2434x574x16 HS00, quantity=2")
print("\nExpected:")
print("  - 2 boards, each with 1x CB(L) + 1x CB(R)")
print("  - Should aggregate to: 1 group with quantity=2")
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
    print(f"  Total bins used: {solution['metadata']['binsUsed']}")
    print(f"  Utilization: {solution['metadata']['utilization']*100:.1f}%")

    print(f"\n📊 Response contains {len(solution.get('bins', []))} group(s)")

    if solution.get('bins'):
        for i, bin_group in enumerate(solution['bins'], 1):
            quantity = bin_group.get('quantity', 1)
            print(f"\n{'='*80}")
            print(f"GROUP {i}: Quantity = {quantity}")
            print(f"{'='*80}")
            print(f"  Material: {bin_group.get('material')}")
            print(f"  Dimensions: {bin_group.get('height')} x {bin_group.get('width')}")
            print(f"  Utilization: {bin_group.get('utilization', 0)*100:.1f}%")
            print(f"\n  Items on each board ({len(bin_group.get('items', []))} items):")

            for item in bin_group.get('items', []):
                print(f"    - {item['itemId']}")
                print(f"      Position: ({item['x']}, {item['y']})")
                print(f"      Size: {item['width']}x{item['height']}")
                print(f"      Rotated: {item.get('rotated', False)}")

        print("\n" + "=" * 80)
        print("AGGREGATION ANALYSIS:")
        print("=" * 80)

        total_bins = solution['metadata']['binsUsed']
        num_groups = len(solution['bins'])

        print(f"\n  Total physical boards: {total_bins}")
        print(f"  Number of groups: {num_groups}")

        if total_bins == 2 and num_groups == 2:
            print(f"\n  ❌ PROBLEM IDENTIFIED: 2 boards NOT aggregated")
            print(f"  Expected: 1 group with quantity=2")
            print(f"  Got: 2 separate groups")

            # Check if boards are actually identical
            if len(solution['bins']) >= 2:
                board1 = solution['bins'][0]
                board2 = solution['bins'][1]

                print(f"\n  Comparing boards...")
                print(f"  Board 1 items: {len(board1['items'])}")
                print(f"  Board 2 items: {len(board2['items'])}")

                # Create signatures
                sig1 = sorted([(i['itemId'], round(i['x'], 2), round(i['y'], 2), round(i['width'], 2), round(i['height'], 2), i.get('rotated', False))
                              for i in board1['items']])
                sig2 = sorted([(i['itemId'], round(i['x'], 2), round(i['y'], 2), round(i['width'], 2), round(i['height'], 2), i.get('rotated', False))
                              for i in board2['items']])

                print(f"\n  Board 1 signature (rounded):")
                for s in sig1:
                    print(f"    {s}")

                print(f"\n  Board 2 signature (rounded):")
                for s in sig2:
                    print(f"    {s}")

                if sig1 == sig2:
                    print(f"\n  ⚠️  SIGNATURES MATCH! Boards ARE identical but not aggregated!")
                    print(f"  This is a BUG in the aggregation logic")
                else:
                    print(f"\n  ℹ️  Signatures differ - boards have different positions")
                    print(f"  Algorithm packed items in different positions on each board")

        elif total_bins == 2 and num_groups == 1:
            qty = solution['bins'][0].get('quantity', 1)
            if qty == 2:
                print(f"\n  ✅ PERFECT: 2 boards aggregated into 1 group with quantity=2")
            else:
                print(f"\n  ❌ Wrong quantity: {qty}")

        print("=" * 80)

    if solution.get('unplaced'):
        print("\n⚠️  Unplaced items:")
        for unplaced in solution['unplaced']:
            print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
