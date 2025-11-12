#!/usr/bin/env python3
"""Detailed test of aggregation - create scenario that SHOULD produce identical boards."""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("DETAILED AGGREGATION TEST")
print("=" * 80)

# Create a scenario that MUST produce 2 identical boards:
# 2 parts, each 600x400, quantity=2 each = 4 total parts
# Each board can fit 2 parts (600x2 + kerf = ~1207, fits in 2440 width)
# So we need 2 boards, each with 2 parts in same positions
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
            'quantity': 2,  # 2 of PART-A
            'rotatable': False
        },
        {
            'id': 'PART-B',
            'name': 'Part B',
            'code': 'PART-B',
            'width': 600,
            'height': 400,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,  # 2 of PART-B
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
print("  - 2x PART-A (600x400)")
print("  - 2x PART-B (600x400)")
print("  - Total: 4 parts")
print("\nExpected:")
print("  - 2 boards, each with 1x PART-A + 1x PART-B in same positions")
print("  - Backend should aggregate to: 1 group with quantity=2")
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
            print(f"GROUP {i}:")
            print(f"{'='*80}")
            print(f"  Quantity: {quantity} {'❌ WRONG - should be aggregated' if quantity == 1 and solution['metadata']['binsUsed'] > 1 else '✅ OK'}")
            print(f"  Material: {bin_group.get('material')}")
            print(f"  Dimensions: {bin_group.get('height')} x {bin_group.get('width')}")
            print(f"  Utilization: {bin_group.get('utilization', 0)*100:.1f}%")
            print(f"\n  Items on this board ({len(bin_group.get('items', []))} items):")

            for item in bin_group.get('items', []):
                print(f"    - {item['itemId']} at ({item['x']}, {item['y']}) size {item['width']}x{item['height']}")

        print("\n" + "=" * 80)
        print("AGGREGATION VERIFICATION:")
        print("=" * 80)

        total_bins = solution['metadata']['binsUsed']
        num_groups = len(solution['bins'])

        print(f"\n  Total physical boards: {total_bins}")
        print(f"  Number of groups in response: {num_groups}")

        if total_bins > 1 and num_groups == total_bins:
            print(f"\n  ❌ FAIL: Boards NOT aggregated!")
            print(f"  Expected: Fewer groups than physical boards")
            print(f"  Got: {num_groups} groups = {total_bins} boards (1:1 mapping, no aggregation)")

            # Check if boards are actually identical
            if len(solution['bins']) >= 2:
                board1 = solution['bins'][0]
                board2 = solution['bins'][1]

                items1_sig = sorted([(i['itemId'], i['x'], i['y']) for i in board1['items']])
                items2_sig = sorted([(i['itemId'], i['x'], i['y']) for i in board2['items']])

                if items1_sig == items2_sig:
                    print(f"\n  ⚠️  Boards 1 and 2 ARE IDENTICAL but not aggregated!")
                    print(f"  Board 1 items: {items1_sig}")
                    print(f"  Board 2 items: {items2_sig}")
                else:
                    print(f"\n  ℹ️  Boards have different layouts (aggregation not applicable)")

        elif total_bins > num_groups:
            print(f"\n  ✅ PASS: Boards ARE aggregated!")
            print(f"  {total_bins} physical boards grouped into {num_groups} group(s)")

            for i, group in enumerate(solution['bins'], 1):
                qty = group.get('quantity', 1)
                if qty > 1:
                    print(f"  Group {i}: {qty} identical boards")

        else:
            print(f"\n  ✅ OK: Only 1 unique board configuration")

        print("=" * 80)

    if solution.get('unplaced'):
        print("\n⚠️  Unplaced items:")
        for unplaced in solution['unplaced']:
            print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("RAW JSON RESPONSE (bins section):")
print("=" * 80)
if response.status_code == 200:
    print(json.dumps(solution.get('bins', []), indent=2)[:1000])
