#!/usr/bin/env python3
"""
Test solving the template data to verify material/thickness matching works.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# This mimics what the frontend now does - creates bins for each material+thickness combo
def test_template_data():
    """Test with the exact template data."""
    print("Testing template data with correct bin configuration...")
    print("=" * 60)

    # Template products
    products = [
        {
            "id": "CAB-001",
            "name": "Cabinet Door",
            "code": "CAB-001",
            "width": 800,
            "height": 600,
            "thickness": 18,
            "material": "Oak",
            "quantity": 4,
            "rotatable": False  # vertical grain
        },
        {
            "id": "SHF-001",
            "name": "Shelf Board",
            "code": "SHF-001",
            "width": 1200,
            "height": 400,
            "thickness": 18,
            "material": "Oak",
            "quantity": 3,
            "rotatable": True  # mixed grain
        },
        {
            "id": "TBL-001",
            "name": "Table Top",
            "code": "TBL-001",
            "width": 1800,
            "height": 900,
            "thickness": 25,
            "material": "Walnut",
            "quantity": 1,
            "rotatable": False  # horizontal grain
        }
    ]

    # Board size: 1220 x 2440 (height x width)
    board_height = 1220
    board_width = 2440

    # Create bins for each unique material+thickness combination
    bins = [
        {
            "id": "Board-Oak-18mm",
            "width": board_width,   # 2440
            "height": board_height, # 1220
            "thickness": 18,
            "material": "Oak",
            "available": -1
        },
        {
            "id": "Board-Walnut-25mm",
            "width": board_width,   # 2440
            "height": board_height, # 1220
            "thickness": 25,
            "material": "Walnut",
            "available": -1
        }
    ]

    request_data = {
        "items": products,
        "bins": bins,
        "parameters": {
            "kerf": 3.5,
            "utilizationThreshold": 0.78,
            "timeLimit": 10.0
        }
    }

    print("\nRequest summary:")
    print(f"  Products: {len(products)}")
    for p in products:
        print(f"    - {p['name']}: {p['width']}x{p['height']}x{p['thickness']}mm, {p['material']}, qty={p['quantity']}")
    print(f"\n  Bins: {len(bins)}")
    for b in bins:
        print(f"    - {b['id']}: {b['width']}x{b['height']}x{b['thickness']}mm, {b['material']}")

    try:
        response = requests.post(
            f"{BASE_URL}/api/solve",
            json=request_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )

        if response.status_code == 200:
            solution = response.json()
            print("\n" + "=" * 60)
            print("✓ SUCCESS!")
            print("=" * 60)
            print(f"\nResults:")
            print(f"  Bins used: {solution['metadata']['binsUsed']}")
            print(f"  Utilization: {solution['metadata']['utilization']*100:.1f}%")
            print(f"  Execution time: {solution['metadata']['executionTime']:.2f}s")
            print(f"  Algorithm: {solution['metadata']['algorithmName']}")
            print(f"  All placed: {'YES ✓' if solution['metadata']['isComplete'] else 'NO ✗'}")

            if solution.get('bins'):
                print(f"\n  Boards used:")
                for i, bin_data in enumerate(solution['bins'], 1):
                    print(f"    {i}. {bin_data['binType']}: {len(bin_data['items'])} items, {bin_data['utilization']*100:.1f}% utilized")

            if solution.get('unplaced'):
                print(f"\n⚠ Warning: {len(solution['unplaced'])} items unplaced:")
                for item in solution['unplaced']:
                    print(f"    - {item['itemId']}: {item['quantity']} pieces")
                return False
            else:
                print("\n🎉 All items placed successfully!")
                return True
        else:
            print(f"\n✗ FAILED!")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


if __name__ == "__main__":
    import time
    print("\nWaiting for server to start...")
    time.sleep(2)

    success = test_template_data()
    exit(0 if success else 1)
