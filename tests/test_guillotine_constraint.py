"""
Test to verify that solutions satisfy the guillotine constraint.

This test checks that all packings can be decomposed into valid
guillotine cuts forming a binary tree structure.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tessellate import solve
from tessellate.algorithms.guillotine_tree import GuillotineTreeBuilder


def test_guillotine_constraint():
    """Test that solution satisfies guillotine constraint."""

    problem_data = {
        "items": [
            {
                "id": "A",
                "width": 600,
                "height": 400,
                "thickness": 18,
                "material": "Oak",
                "quantity": 4,
                "rotatable": True
            },
            {
                "id": "B",
                "width": 500,
                "height": 300,
                "thickness": 18,
                "material": "Oak",
                "quantity": 3,
                "rotatable": True
            }
        ],
        "bins": [
            {
                "id": "STD",
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

    print("\n" + "="*70)
    print("GUILLOTINE CONSTRAINT VERIFICATION TEST")
    print("="*70)

    # Solve
    solution = solve(problem_data, time_limit=5.0)

    print(f"\nSolution:")
    print(f"  Algorithm: {solution['metadata']['algorithmName']}")
    print(f"  Bins used: {solution['metadata']['objectiveValue']}")
    print(f"  Utilization: {solution['metadata']['utilization']:.2%}")
    print(f"  All placed: {'✓' if len(solution['unplaced']) == 0 else '✗'}")

    print(f"\n{'='*70}")
    print("VERIFYING GUILLOTINE PROPERTY")
    print("="*70)

    # Check each bin
    all_guillotine_valid = True

    for bin_data in solution['bins']:
        bin_id = bin_data['binId'] + 1
        items = bin_data['items']

        print(f"\nBin {bin_id}: {len(items)} items")

        if len(items) == 0:
            print("  ⚠ Empty bin (trivially guillotine-valid)")
            continue

        if len(items) == 1:
            print("  ✓ Single item (trivially guillotine-valid)")
            continue

        # Check for guillotine validity by analyzing placement pattern
        is_valid, reason = check_guillotine_property(bin_data, problem_data['parameters']['kerf'])

        if is_valid:
            print(f"  ✓ Guillotine constraint SATISFIED")
        else:
            print(f"  ✗ Guillotine constraint VIOLATED")
            print(f"    Reason: {reason}")
            all_guillotine_valid = False

        # Show item positions for debugging
        print(f"  Items:")
        for item in items:
            rot = " [rotated]" if item['rotated'] else ""
            print(f"    - {item['itemId']}: {item['width']:.0f}x{item['height']:.0f} "
                  f"at ({item['x']:.0f}, {item['y']:.0f}){rot}")

    print(f"\n{'='*70}")
    if all_guillotine_valid:
        print("✅ ALL BINS SATISFY GUILLOTINE CONSTRAINT")
        print("="*70)
        print("\nThe algorithm correctly produces guillotine-compatible packings!")
        return True
    else:
        print("❌ SOME BINS VIOLATE GUILLOTINE CONSTRAINT")
        print("="*70)
        print("\nThe algorithm does NOT guarantee guillotine cuts!")
        return False


def check_guillotine_property(bin_data, kerf):
    """
    Check if a bin packing satisfies the guillotine property.

    A packing is guillotine-compatible if we can find a sequence of
    edge-to-edge cuts that form a binary tree isolating each item.

    Args:
        bin_data: Bin data from solution
        kerf: Kerf width

    Returns:
        Tuple of (is_valid, reason)
    """
    items = bin_data['items']

    if len(items) <= 1:
        return (True, "Trivial case")

    # Try to find guillotine cuts recursively
    # Strategy: Sort items by position and try to find separating cuts

    # Sort by y-coordinate (try horizontal cuts first)
    items_sorted_y = sorted(items, key=lambda item: item['y'])

    # Try to find a horizontal cut that cleanly separates items
    for i in range(len(items_sorted_y) - 1):
        cut_y = items_sorted_y[i]['y'] + items_sorted_y[i]['height'] + kerf

        # Check if this cut cleanly separates items
        items_below = [item for item in items if item['y'] + item['height'] + kerf <= cut_y]
        items_above = [item for item in items if item['y'] >= cut_y]

        if items_below and items_above and len(items_below) + len(items_above) == len(items):
            # Found a valid horizontal cut!
            # Recursively check both parts
            valid_below, _ = check_guillotine_property_for_items(items_below, kerf)
            valid_above, _ = check_guillotine_property_for_items(items_above, kerf)

            if valid_below and valid_above:
                return (True, f"Horizontal cut at y={cut_y:.0f}")

    # Try vertical cuts
    items_sorted_x = sorted(items, key=lambda item: item['x'])

    for i in range(len(items_sorted_x) - 1):
        cut_x = items_sorted_x[i]['x'] + items_sorted_x[i]['width'] + kerf

        # Check if this cut cleanly separates items
        items_left = [item for item in items if item['x'] + item['width'] + kerf <= cut_x]
        items_right = [item for item in items if item['x'] >= cut_x]

        if items_left and items_right and len(items_left) + len(items_right) == len(items):
            # Found a valid vertical cut!
            valid_left, _ = check_guillotine_property_for_items(items_left, kerf)
            valid_right, _ = check_guillotine_property_for_items(items_right, kerf)

            if valid_left and valid_right:
                return (True, f"Vertical cut at x={cut_x:.0f}")

    # No valid guillotine cut found
    return (False, "No valid guillotine cut separates the items")


def check_guillotine_property_for_items(items, kerf):
    """Helper to check guillotine property for a subset of items."""
    if len(items) <= 1:
        return (True, "Trivial")

    # Same logic as above, but for a subset
    # Try horizontal cuts
    items_sorted_y = sorted(items, key=lambda item: item['y'])

    for i in range(len(items_sorted_y) - 1):
        cut_y = items_sorted_y[i]['y'] + items_sorted_y[i]['height'] + kerf
        items_below = [item for item in items if item['y'] + item['height'] + kerf <= cut_y]
        items_above = [item for item in items if item['y'] >= cut_y]

        if items_below and items_above and len(items_below) + len(items_above) == len(items):
            valid_below, _ = check_guillotine_property_for_items(items_below, kerf)
            valid_above, _ = check_guillotine_property_for_items(items_above, kerf)
            if valid_below and valid_above:
                return (True, "Horizontal")

    # Try vertical cuts
    items_sorted_x = sorted(items, key=lambda item: item['x'])

    for i in range(len(items_sorted_x) - 1):
        cut_x = items_sorted_x[i]['x'] + items_sorted_x[i]['width'] + kerf
        items_left = [item for item in items if item['x'] + item['width'] + kerf <= cut_x]
        items_right = [item for item in items if item['x'] >= cut_x]

        if items_left and items_right and len(items_left) + len(items_right) == len(items):
            valid_left, _ = check_guillotine_property_for_items(items_left, kerf)
            valid_right, _ = check_guillotine_property_for_items(items_right, kerf)
            if valid_left and valid_right:
                return (True, "Vertical")

    return (False, "No valid cut")


if __name__ == "__main__":
    success = test_guillotine_constraint()
    sys.exit(0 if success else 1)
