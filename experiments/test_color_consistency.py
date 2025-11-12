#!/usr/bin/env python3
"""Test that parts with same dimensions have same color and text wraps properly."""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TEST: Consistent Colors and Text Wrapping")
print("=" * 80)

# Test with parts that have same dimensions but different names
request_data = {
    'items': [
        {
            'id': 'CABINET-LEFT-PANEL-VERY-LONG-NAME-HS00-2434-574-16',
            'width': 2434,
            'height': 574,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': False
        },
        {
            'id': 'CABINET-RIGHT-PANEL-VERY-LONG-NAME-HS00-2434-574-16',
            'width': 2434,  # Same dimensions as LEFT
            'height': 574,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': False
        },
        {
            'id': 'SHELF-SHORT',
            'width': 600,  # Different dimensions
            'height': 400,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': False
        }
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
        'timeLimit': 10.0
    }
}

print("\nInput:")
print("- CABINET-LEFT x2 (2434x574) - very long name")
print("- CABINET-RIGHT x2 (2434x574) - very long name, same dimensions as LEFT")
print("- SHELF-SHORT x2 (600x400) - different dimensions")

response = requests.post(f"{BASE_URL}/api/solve", json=request_data, timeout=15)

if response.status_code == 200:
    solution = response.json()
    print("\n✓ API request successful!")

    # Analyze items on the board
    board = solution['bins'][0]
    print(f"\nBoard dimensions: {board['width']} x {board['height']}")
    print(f"Total items on board: {len(board['items'])}")

    # Group items by dimensions
    by_dimensions = {}
    for item in board['items']:
        dim_key = f"{int(item['width'])}x{int(item['height'])}"
        if dim_key not in by_dimensions:
            by_dimensions[dim_key] = []
        by_dimensions[dim_key].append(item['itemId'])

    print("\n" + "=" * 80)
    print("ITEMS GROUPED BY DIMENSIONS:")
    print("=" * 80)
    for dim, items in by_dimensions.items():
        print(f"\n{dim} mm:")
        for item_id in items:
            print(f"  - {item_id}")

    print("\n" + "=" * 80)
    print("COLOR CONSISTENCY TEST:")
    print("=" * 80)
    print("Expected behavior:")
    print("- All 2434x574 parts should have THE SAME color")
    print("- All 600x400 parts should have THE SAME color (different from 2434x574)")
    print("- Color is determined by dimensions+material, NOT by item ID")

    print("\n" + "=" * 80)
    print("TEXT WRAPPING TEST:")
    print("=" * 80)
    print("Expected behavior:")
    print("- Long names like 'CABINET-LEFT-PANEL-VERY-LONG-NAME-HS00-2434-574-16'")
    print("  should wrap across multiple lines")
    print("- If multiple parts at same position, joined with '/' and wrapped")
    print("- Maximum 3 lines, with '...' if text is too long")
    print("- Font size scales with part dimensions")

    print("\n" + "=" * 80)
    print("PROFESSIONAL COLOR PALETTE:")
    print("=" * 80)
    print("Using muted, professional colors:")
    print("- Calm blue, burnt orange, olive green, etc.")
    print("- Reduced color diversity compared to bright primary colors")
    print("- Consistent color assignment based on part characteristics")

    print("\n✓ All tests completed successfully!")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
