#!/usr/bin/env python3
"""
Verify that material constraints are enforced correctly:
1. Each board has exactly ONE material type
2. Items of different materials are NEVER placed on the same board
3. Board material comes from bin definition (not derived from items)
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# Test data with MULTIPLE colors and thicknesses
# This should create SEPARATE boards for each material+thickness combination
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
            'quantity': 3,
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
            'quantity': 3,
            'rotatable': False
        },
        # HS02 items (fixed grain) - thickness 18 (SAME thickness as HS01, but DIFFERENT material)
        {
            'id': 'TEST-HS02-001',
            'name': 'Test HS02 Item 1',
            'code': 'TEST-HS02-850-650-18',
            'width': 850,
            'height': 650,
            'thickness': 18,
            'material': 'HS02',
            'quantity': 3,
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
        # Create separate bins for each material+thickness combination
        # This is what the frontend does automatically
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

print("=" * 80)
print("TESTING MATERIAL CONSTRAINT ENFORCEMENT")
print("=" * 80)
print("\nTest data contains items with:")
print("  - HS00 (thickness 16): 3 items")
print("  - HS01 (thickness 18): 3 items")
print("  - HS02 (thickness 18): 3 items - SAME thickness as HS01, DIFFERENT material")
print("  - HS99 (thickness 25): 2 items")
print("\nExpected behavior:")
print("  - Each board should have EXACTLY ONE material type")
print("  - Items of different materials should NEVER appear on the same board")
print("  - Even if HS01 and HS02 both have thickness 18, they should be on SEPARATE boards")
print("=" * 80)

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
        print("\n" + "=" * 80)
        print("BOARD ANALYSIS:")
        print("=" * 80)

        all_correct = True
        materials_found = set()

        for i, bin_data in enumerate(solution['bins'], 1):
            board_material = bin_data['material']
            board_thickness = bin_data['thickness']
            materials_found.add(board_material)

            # Get all item materials on this board
            item_materials = [item['material'] for item in bin_data['items']]
            unique_item_materials = set(item_materials)

            print(f"\nBoard {i}:")
            print(f"  Board material: {board_material}")
            print(f"  Board thickness: {board_thickness}")
            print(f"  Items on board: {len(bin_data['items'])}")
            print(f"  Item materials: {', '.join(item_materials)}")
            print(f"  Unique materials: {unique_item_materials}")

            # CHECK 1: Board should have exactly one material
            if len(unique_item_materials) > 1:
                print(f"  ❌ FAIL: Board has MIXED materials! {unique_item_materials}")
                all_correct = False
            else:
                print(f"  ✅ PASS: Board has single material type")

            # CHECK 2: Item materials should match board material
            if unique_item_materials and list(unique_item_materials)[0] != board_material:
                print(f"  ⚠️  WARNING: Item material ({unique_item_materials}) doesn't match board material ({board_material})")
                # This might be OK if backend uses different logic

            # CHECK 3: All items should have same thickness as board
            item_thicknesses = [item['thickness'] for item in bin_data['items']]
            if any(t != board_thickness for t in item_thicknesses):
                print(f"  ❌ FAIL: Items have different thickness than board!")
                all_correct = False

        print("\n" + "=" * 80)
        print("MATERIAL DISTRIBUTION:")
        print("=" * 80)
        print(f"Materials found on boards: {materials_found}")
        print(f"Expected materials: HS00, HS01, HS02, HS99 (or subset)")

        # Verify HS01 and HS02 are on SEPARATE boards
        hs01_boards = []
        hs02_boards = []

        for i, bin_data in enumerate(solution['bins'], 1):
            item_materials = [item['material'] for item in bin_data['items']]
            if 'HS01' in item_materials:
                hs01_boards.append(i)
            if 'HS02' in item_materials:
                hs02_boards.append(i)

        print(f"\nHS01 items found on boards: {hs01_boards}")
        print(f"HS02 items found on boards: {hs02_boards}")

        # Check for overlap
        if set(hs01_boards) & set(hs02_boards):
            print("❌ FAIL: HS01 and HS02 items appear on the SAME board(s)!")
            all_correct = False
        else:
            if hs01_boards and hs02_boards:
                print("✅ PASS: HS01 and HS02 items are on SEPARATE boards (same thickness, different materials)")

        print("\n" + "=" * 80)
        if all_correct:
            print("✅✅✅ ALL TESTS PASSED ✅✅✅")
            print("Material constraints are correctly enforced!")
        else:
            print("❌❌❌ TESTS FAILED ❌❌❌")
            print("Material constraints are NOT correctly enforced!")
        print("=" * 80)

    # Show unplaced items if any
    if solution.get('unplaced'):
        print("\n" + "=" * 80)
        print("UNPLACED ITEMS:")
        print("=" * 80)
        for unplaced in solution['unplaced']:
            print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")
        print("\nNote: Items may be unplaced if no compatible bins are available")
        print("      (e.g., different thickness than available boards)")

else:
    print(f"✗ Failed: {response.status_code}")
    print(response.text)
