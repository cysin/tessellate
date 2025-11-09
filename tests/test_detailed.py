"""Detailed test to inspect solution."""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tessellate import solve


def test_detailed():
    """Test with detailed output."""
    problem_data = {
        "items": [
            {
                "id": "I001",
                "width": 2000,
                "height": 600,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": False
            },
            {
                "id": "I002",
                "width": 900,
                "height": 600,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": True
            },
            {
                "id": "I003",
                "width": 880,
                "height": 580,
                "thickness": 18,
                "material": "Oak",
                "quantity": 3,
                "rotatable": True
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
            "utilizationThreshold": 0.78,
            "timeLimit": 5.0
        }
    }

    print("\nProblem:")
    print(f"  I001: 2000x600 x2 (non-rotatable)")
    print(f"  I002: 900x600 x2 (rotatable)")
    print(f"  I003: 880x580 x3 (rotatable)")
    print(f"  Total: 7 items")

    # Solve
    solution = solve(problem_data, time_limit=5.0)

    print(f"\nSolution:")
    print(f"  Bins used: {solution['metadata']['objectiveValue']}")
    print(f"  Utilization: {solution['metadata']['utilization']:.2%}")

    # Count placed items
    total_placed = 0
    for bin_data in solution['bins']:
        print(f"\n  Bin {bin_data['binId'] + 1} ({bin_data['binType']}):")
        print(f"    Size: {bin_data['width']}x{bin_data['height']}")
        print(f"    Utilization: {bin_data['utilization']:.2%}")
        print(f"    Items:")
        for item in bin_data['items']:
            print(f"      - {item['itemId']}: {item['width']}x{item['height']} at ({item['x']}, {item['y']}) {'[rotated]' if item['rotated'] else ''}")
            total_placed += 1

    print(f"\n  Total items placed: {total_placed}")
    print(f"  Items unplaced: {len(solution['unplaced'])}")

    if solution['unplaced']:
        print(f"  Unplaced items:")
        for unplaced in solution['unplaced']:
            print(f"    - {unplaced['itemId']}: {unplaced['quantity']} units")

    return True


if __name__ == "__main__":
    test_detailed()
