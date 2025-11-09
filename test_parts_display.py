#!/usr/bin/env python3
"""Test that parts display shows all item names when aggregated."""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TEST: Parts Display with Aggregation")
print("=" * 80)

request_data = {
    'items': [
        {
            'id': 'CB(L)-HS00-2434-574-16',
            'name': 'CB(L)',
            'width': 2434,
            'height': 574,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': False
        },
        {
            'id': 'CB(R)-HS00-2434-574-16',
            'name': 'CB(R)',
            'width': 2434,
            'height': 574,
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

response = requests.post(f"{BASE_URL}/api/solve", json=request_data, timeout=15)

if response.status_code == 200:
    solution = response.json()

    print("\n✓ API request successful!")
    print(f"\nBoards used: {solution['metadata']['binsUsed']}")
    print(f"Board groups: {len(solution['bins'])}")

    for i, board in enumerate(solution['bins'], 1):
        print(f"\n{'='*80}")
        print(f"BOARD GROUP {i}")
        print(f"{'='*80}")
        print(f"Quantity: {board.get('quantity', 1)}")
        print(f"\nItems in group ({len(board['items'])} total):")

        # Simulate frontend aggregation logic
        from collections import defaultdict
        parts_counts = defaultdict(lambda: {'itemId': '', 'count': 0})

        for item in board['items']:
            key = f"{item['itemId']}-{item['width']}-{item['height']}-{item.get('rotated', False)}"
            if parts_counts[key]['itemId'] == '':
                parts_counts[key]['itemId'] = item['itemId']
                parts_counts[key]['width'] = item['width']
                parts_counts[key]['height'] = item['height']
                parts_counts[key]['count'] = item.get('count', board.get('quantity', 1))
            else:
                parts_counts[key]['count'] += item.get('count', board.get('quantity', 1))

        print(f"\nParts across all {board.get('quantity', 1)} board(s):")
        for part_key, part_data in sorted(parts_counts.items()):
            print(f"  - {part_data['itemId']}: {part_data['count']} pc(s)")
            print(f"    Details from backend: {[item for item in board['items'] if item['itemId'] == part_data['itemId']]}")

        print(f"\n{'='*80}")
        print("VERIFICATION:")
        print(f"{'='*80}")

        # Check if both CB(L) and CB(R) appear
        item_ids = set(item['itemId'] for item in board['items'])

        if 'CB(L)-HS00-2434-574-16' in item_ids and 'CB(R)-HS00-2434-574-16' in item_ids:
            print("✅ PASS: Both CB(L) and CB(R) appear in items list")
        else:
            print(f"❌ FAIL: Missing items. Found: {item_ids}")

        # Check counts
        cb_l_count = sum(1 for item in board['items'] if item['itemId'] == 'CB(L)-HS00-2434-574-16')
        cb_r_count = sum(1 for item in board['items'] if item['itemId'] == 'CB(R)-HS00-2434-574-16')

        print(f"\nItem occurrences in items array:")
        print(f"  CB(L): {cb_l_count} entries")
        print(f"  CB(R): {cb_r_count} entries")

        # Each part appears at 2 positions (0,0) and (0,577.5)
        # Each position has 1 instance from each of the 2 boards
        if cb_l_count == 2 and cb_r_count == 2:
            print(f"✅ PASS: Each part appears 2 times (once per position)")
        else:
            print(f"❌ FAIL: Expected 2 occurrences each")

        # Check if 'count' field is present
        has_count_field = all('count' in item for item in board['items'])
        if has_count_field:
            print(f"✅ PASS: All items have 'count' field")
            counts = [item['count'] for item in board['items']]
            print(f"  Count values: {counts}")
        else:
            print(f"❌ FAIL: Items missing 'count' field")

        print(f"{'='*80}")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
