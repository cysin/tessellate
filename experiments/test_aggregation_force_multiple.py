#!/usr/bin/env python3
"""Force creation of multiple boards to test aggregation."""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("FORCED MULTIPLE BOARDS AGGREGATION TEST")
print("=" * 80)

# Force 2 boards by using large parts that won't fit together
# Part is 1200x600, board is 2440x1220
# 2 parts horizontally: 1200*2 + kerf = 2403.5 (fits)
# BUT: If we have 3 parts, we need 2 boards
request_data = {
    'items': [
        {
            'id': 'LARGE-A',
            'name': 'Large Part A',
            'code': 'LARGE-A',
            'width': 1200,
            'height': 600,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 6,  # 6 parts = should need 3 boards (2 parts each)
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

print("\nScenario:")
print("  - 6x LARGE-A (1200x600)")
print("  - Board: 2440x1220")
print("  - Each board can fit 2 parts horizontally")
print("\nExpected:")
print("  - 3 boards, each with 2x LARGE-A in same positions")
print("  - Backend should aggregate to: 1 group with quantity=3")
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

    total_bins = solution['metadata']['binsUsed']
    num_groups = len(solution.get('bins', []))

    if solution.get('bins'):
        for i, bin_group in enumerate(solution['bins'], 1):
            quantity = bin_group.get('quantity', 1)
            print(f"\n{'='*80}")
            print(f"GROUP {i}:")
            print(f"{'='*80}")
            print(f"  Quantity: {quantity} board(s)")
            print(f"  Material: {bin_group.get('material')}")
            print(f"  Dimensions: {bin_group.get('height')} x {bin_group.get('width')}")
            print(f"  Utilization: {bin_group.get('utilization', 0)*100:.1f}%")
            print(f"\n  Items on each board ({len(bin_group.get('items', []))} items):")

            for item in bin_group.get('items', []):
                print(f"    - {item['itemId']} at ({item['x']}, {item['y']}) size {item['width']}x{item['height']}")

        print("\n" + "=" * 80)
        print("AGGREGATION ANALYSIS:")
        print("=" * 80)

        print(f"\n  Total physical boards: {total_bins}")
        print(f"  Number of groups returned: {num_groups}")

        if total_bins == num_groups and total_bins > 1:
            print(f"\n  ❌ FAIL: NO AGGREGATION!")
            print(f"  Problem: Each board is a separate group (1:1 mapping)")
            print(f"  Expected: {total_bins} boards grouped into fewer groups")

            # Diagnose WHY not aggregated
            if len(solution['bins']) >= 2:
                print(f"\n  Checking if boards are identical...")
                for i in range(min(3, len(solution['bins']))):
                    board = solution['bins'][i]
                    items_sig = sorted([(item['itemId'], item['x'], item['y'], item['width'], item['height'])
                                       for item in board['items']])
                    print(f"  Board {i+1} signature: {items_sig}")

        elif total_bins > num_groups:
            print(f"\n  ✅ PASS: AGGREGATION WORKING!")
            print(f"  {total_bins} physical boards → {num_groups} group(s)")

            total_boards_from_groups = sum(g.get('quantity', 1) for g in solution['bins'])
            print(f"  Verification: Sum of quantities = {total_boards_from_groups}")

            if total_boards_from_groups == total_bins:
                print(f"  ✅ Quantities add up correctly!")
            else:
                print(f"  ❌ Quantities don't match! Expected {total_bins}, got {total_boards_from_groups}")

        else:
            print(f"\n  ℹ️  Only 1 board or 1 unique configuration")

        print("=" * 80)

    if solution.get('unplaced'):
        print("\n⚠️  Unplaced items:")
        for unplaced in solution['unplaced']:
            print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
