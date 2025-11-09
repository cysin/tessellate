"""Test with realistic cabinet example."""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tessellate import solve


def test_realistic():
    """Test with realistic cabinet problem where all items fit."""
    problem_data = {
        "items": [
            {
                "id": "DOOR_001",
                "width": 600,
                "height": 2000,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": False,  # Grain must be vertical
                "description": "Cabinet doors"
            },
            {
                "id": "TOP_001",
                "width": 900,
                "height": 600,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": True,
                "description": "Top panels"
            },
            {
                "id": "SHELF_001",
                "width": 880,
                "height": 580,
                "thickness": 18,
                "material": "Oak",
                "quantity": 4,
                "rotatable": True,
                "description": "Shelves"
            },
            {
                "id": "BACK_001",
                "width": 1200,
                "height": 800,
                "thickness": 18,
                "material": "Oak",
                "quantity": 1,
                "rotatable": True,
                "description": "Back panel"
            }
        ],
        "bins": [
            {
                "id": "STD-1220x2440",
                "width": 1220,
                "height": 2440,
                "thickness": 18,
                "material": "Oak",
                "available": -1
            }
        ],
        "parameters": {
            "kerf": 3.0,
            "utilizationThreshold": 0.75,
            "timeLimit": 5.0
        }
    }

    print("\n" + "="*60)
    print("Realistic Cabinet Manufacturing Example")
    print("="*60)
    print("\nItems:")
    total_area = 0
    for item in problem_data['items']:
        area = item['width'] * item['height'] * item['quantity']
        total_area += area
        rot_str = "(grain vertical)" if not item['rotatable'] else "(rotatable)"
        print(f"  {item['id']}: {item['width']}x{item['height']} x{item['quantity']} {rot_str}")

    bin_area = problem_data['bins'][0]['width'] * problem_data['bins'][0]['height']
    theoretical_bins = total_area / bin_area
    print(f"\nTotal item area: {total_area:,.0f} mm²")
    print(f"Bin area: {bin_area:,.0f} mm²")
    print(f"Theoretical minimum bins: {theoretical_bins:.2f}")

    # Solve
    print("\nSolving...")
    solution = solve(problem_data, time_limit=5.0)

    print(f"\n{'='*60}")
    print("SOLUTION")
    print(f"{'='*60}")
    print(f"Bins used: {solution['metadata']['objectiveValue']}")
    print(f"Utilization: {solution['metadata']['utilization']:.2%}")
    print(f"Execution time: {solution['metadata']['executionTime']:.3f}s")
    print(f"Algorithm: {solution['metadata']['algorithmName']}")

    # Count placed items by type
    placed_counts = {}
    for bin_data in solution['bins']:
        for item in bin_data['items']:
            item_id = item['itemId']
            placed_counts[item_id] = placed_counts.get(item_id, 0) + 1

    print(f"\nPlacement Summary:")
    for item in problem_data['items']:
        placed = placed_counts.get(item['id'], 0)
        status = "✓" if placed == item['quantity'] else "✗"
        print(f"  {status} {item['id']}: {placed}/{item['quantity']} placed")

    # Show bin details
    print(f"\nBin Details:")
    for bin_data in solution['bins']:
        print(f"\n  Bin {bin_data['binId'] + 1}:")
        print(f"    Utilization: {bin_data['utilization']:.2%}")
        print(f"    Items: {len(bin_data['items'])}")
        for item in bin_data['items']:
            rot = " [rotated]" if item['rotated'] else ""
            print(f"      - {item['itemId']}: {item['width']:.0f}x{item['height']:.0f}{rot}")

    if solution['unplaced']:
        print(f"\n⚠ WARNING: {len(solution['unplaced'])} item types could not be placed")
        for item_id, qty in solution['unplaced']:
            print(f"    - {item_id}: {qty} units")

    # Performance metrics
    if 'gap_percent' in solution['metadata']:
        print(f"\nPerformance:")
        print(f"  Gap to lower bound: {solution['metadata']['gap_percent']:.1f}%")

    # Validation
    all_placed = len(solution['unplaced']) == 0
    good_util = solution['metadata']['utilization'] >= 0.75
    fast_enough = solution['metadata']['executionTime'] < 5.0

    print(f"\nQuality Checks:")
    print(f"  {'✓' if all_placed else '✗'} All items placed")
    print(f"  {'✓' if good_util else '✗'} Utilization >= 75%")
    print(f"  {'✓' if fast_enough else '✗'} Time < 5s")

    if all_placed and good_util and fast_enough:
        print(f"\n{'='*60}")
        print("✓ TEST PASSED - World-class solution!")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("⚠ Test completed with warnings")
        print(f"{'='*60}")

    return all_placed


if __name__ == "__main__":
    test_realistic()
