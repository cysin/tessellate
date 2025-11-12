#!/usr/bin/env python3
"""Test that SVG diagram shows correct part names without duplicates."""

import requests
import json
import re

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TEST: SVG Diagram Display with Same Dimensions Different Names")
print("=" * 80)

request_data = {
    'items': [
        {
            'id': 'CB(L)-HS00-2434-574-16',
            'name': 'Cabinet Left',
            'width': 2434,
            'height': 574,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': False
        },
        {
            'id': 'CB(R)-HS00-2434-574-16',
            'name': 'Cabinet Right',
            'width': 2434,  # Same dimensions
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

print("\nInput: CB(L) x2 and CB(R) x2 (same dimensions, different IDs)")

response = requests.post(f"{BASE_URL}/api/solve", json=request_data, timeout=15)

if response.status_code == 200:
    solution = response.json()

    print(f"\n✓ API request successful!")
    print(f"Boards used: {solution['metadata']['binsUsed']}")
    print(f"Board groups: {len(solution['bins'])}")

    for i, board in enumerate(solution['bins'], 1):
        print(f"\n{'='*80}")
        print(f"BOARD GROUP {i}")
        print(f"{'='*80}")
        print(f"Quantity: {board.get('quantity', 1)}")
        print(f"Items in backend response: {len(board['items'])}")

        # Check for position duplicates
        positions = {}
        for item in board['items']:
            pos_key = f"({item['x']}, {item['y']})"
            if pos_key not in positions:
                positions[pos_key] = []
            positions[pos_key].append(item['itemId'])

        print(f"\nItems by position:")
        for pos, item_ids in positions.items():
            print(f"  Position {pos}: {item_ids}")
            if len(item_ids) > 1:
                print(f"    → Multiple items at same position (will be displayed as: {'/'.join(sorted(set(item_ids)))})")

        print(f"\n{'='*80}")
        print("EXPECTED SVG DISPLAY:")
        print(f"{'='*80}")

        # Simulate frontend SVG label generation
        for pos, item_ids in positions.items():
            unique_ids = sorted(set(item_ids))
            label = '/'.join(unique_ids)
            print(f"  Position {pos}: {label}")

        print(f"\n{'='*80}")
        print("VERIFICATION:")
        print(f"{'='*80}")

        # Check if both CB(L) and CB(R) appear
        all_item_ids = set(item['itemId'] for item in board['items'])

        if 'CB(L)-HS00-2434-574-16' in all_item_ids and 'CB(R)-HS00-2434-574-16' in all_item_ids:
            print("✅ PASS: Both CB(L) and CB(R) are in backend response")
        else:
            print(f"❌ FAIL: Missing items. Found: {all_item_ids}")

        # Check that positions have multiple items
        has_merged_positions = any(len(ids) > 1 for ids in positions.values())
        if has_merged_positions:
            print("✅ PASS: Multiple items exist at same position (will be merged in SVG)")
        else:
            print("❌ FAIL: No merged positions found")

        # Expected behavior
        print(f"\n{'='*80}")
        print("EXPECTED FRONTEND BEHAVIOR:")
        print(f"{'='*80}")
        print("1. Backend returns all unique item IDs across aggregated boards")
        print("2. Frontend groups items by position (x, y, width, height, rotated)")
        print("3. SVG draws ONE rectangle per unique position")
        print("4. Label shows all item IDs at that position joined by '/'")
        print("5. Example: 'CB(L)-HS00-2434-574-16/CB(R)-HS00-2434-574-16'")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
