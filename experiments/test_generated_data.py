#!/usr/bin/env python3
"""
Test that generated Excel files work with the webapp.
"""

import requests
import time
from pathlib import Path

BASE_URL = "http://localhost:5000"


def test_upload_generated_file(filepath):
    """Test uploading a generated file."""
    print(f"\nTesting: {filepath.name}")
    print("=" * 60)

    with open(filepath, 'rb') as f:
        files = {'file': (filepath.name, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

        response = requests.post(
            f"{BASE_URL}/api/upload-excel",
            files=files,
            timeout=10
        )

    if response.status_code == 200:
        data = response.json()
        print("✓ Upload successful!")
        print(f"  Products parsed: {data.get('count', 0)}")

        if data.get('warnings'):
            print(f"  ⚠ Warnings: {len(data['warnings'])}")
            for warning in data['warnings'][:3]:  # Show first 3
                print(f"    - {warning}")

        if data.get('products'):
            print(f"\n  Sample products:")
            for i, product in enumerate(data['products'][:5], 1):  # Show first 5
                print(f"    {i}. {product['name'][:30]:<30} | {product['width']}x{product['height']}x{product['thickness']}mm | Qty:{product['qty']} | {product['grain']}")

        return True
    else:
        print(f"✗ Upload failed!")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")
        return False


def test_solve_with_generated_data(filepath):
    """Test solving with generated data."""
    print(f"\nSolving cutting plan for: {filepath.name}")
    print("=" * 60)

    # First upload to get products
    with open(filepath, 'rb') as f:
        files = {'file': (filepath.name, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        upload_response = requests.post(f"{BASE_URL}/api/upload-excel", files=files, timeout=10)

    if upload_response.status_code != 200:
        print("✗ Failed to upload file")
        return False

    data = upload_response.json()
    products = data['products']

    # Convert to items format
    items = []
    for p in products:
        items.append({
            'id': p['code'],
            'name': p['name'],
            'code': p['code'],
            'width': p['width'],
            'height': p['height'],
            'thickness': p['thickness'],
            'material': p['color'],
            'quantity': p['qty'],
            'rotatable': p['grain'] == 'mixed'
        })

    # Create solve request
    request_data = {
        'items': items,
        'bins': [{
            'id': 'Board-1220x2440',
            'width': 2440,
            'height': 1220,
            'thickness': 18,
            'material': 'Standard',
            'available': -1
        }],
        'parameters': {
            'kerf': 3.5,
            'utilizationThreshold': 0.78,
            'timeLimit': 10.0
        }
    }

    solve_response = requests.post(
        f"{BASE_URL}/api/solve",
        json=request_data,
        timeout=15
    )

    if solve_response.status_code == 200:
        solution = solve_response.json()
        print("✓ Solve successful!")
        print(f"  Bins used: {solution['metadata']['binsUsed']}")
        print(f"  Utilization: {solution['metadata']['utilization']*100:.1f}%")
        print(f"  Execution time: {solution['metadata']['executionTime']:.2f}s")
        print(f"  All placed: {'YES ✓' if solution['metadata']['isComplete'] else 'NO ✗'}")

        if solution.get('unplaced'):
            print(f"  ⚠ Unplaced items: {len(solution['unplaced'])}")

        return solution['metadata']['isComplete']
    else:
        print(f"✗ Solve failed!")
        print(f"  Status: {solve_response.status_code}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTING GENERATED WARDROBE DATA")
    print("=" * 60)

    # Wait for server
    print("\nWaiting for server...")
    time.sleep(2)

    # Test files
    test_dir = Path(__file__).parent / "test_data"
    test_files = sorted(test_dir.glob("wardrobe_order_*.xlsx"))[:3]  # Test first 3

    if not test_files:
        print("No test files found!")
        exit(1)

    print(f"Found {len(test_files)} test files")

    results = []

    # Test each file
    for filepath in test_files:
        # Test upload
        upload_ok = test_upload_generated_file(filepath)
        results.append(("Upload " + filepath.name, upload_ok))

        # Test solve
        if upload_ok:
            solve_ok = test_solve_with_generated_data(filepath)
            results.append(("Solve " + filepath.name, solve_ok))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    passed_count = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed_count}/{len(results)} tests passed")

    exit(0 if passed_count == len(results) else 1)
