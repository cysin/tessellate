#!/usr/bin/env python3
"""
Test script for webapp functionality.
Tests both manual input and Excel upload workflows.
"""

import requests
import json
from io import BytesIO

BASE_URL = "http://localhost:5000"


def test_manual_input():
    """Test the manual input workflow with /api/solve endpoint."""
    print("\n" + "=" * 60)
    print("TEST 1: Manual Input Workflow")
    print("=" * 60)

    # Prepare test data matching frontend format
    request_data = {
        "items": [
            {
                "id": "CAB-001",
                "width": 800,  # Length in UI
                "height": 600,  # Width in UI
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": True,  # mixed grain
                "name": "Cabinet Door",
                "code": "CAB-001"
            },
            {
                "id": "SHF-001",
                "width": 1200,
                "height": 400,
                "thickness": 18,
                "material": "Oak",
                "quantity": 3,
                "rotatable": False,  # horizontal grain
                "name": "Shelf Board",
                "code": "SHF-001"
            }
        ],
        "bins": [
            {
                "id": "Board-1220x2440",
                "width": 1220,
                "height": 2440,
                "thickness": 18,
                "material": "Wood",
                "available": -1
            }
        ],
        "parameters": {
            "kerf": 3.0,
            "utilizationThreshold": 0.75,
            "timeLimit": 10.0
        }
    }

    print("\nSending request to /api/solve...")
    print(f"Items: {len(request_data['items'])}")

    try:
        response = requests.post(
            f"{BASE_URL}/api/solve",
            json=request_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )

        if response.status_code == 200:
            solution = response.json()
            print("\n✓ SUCCESS!")
            print(f"\nResults:")
            print(f"  Bins used: {solution['metadata']['binsUsed']}")
            print(f"  Utilization: {solution['metadata']['utilization']*100:.1f}%")
            print(f"  Execution time: {solution['metadata']['executionTime']:.2f}s")
            print(f"  Algorithm: {solution['metadata']['algorithmName']}")
            print(f"  All placed: {'Yes' if solution['metadata']['isComplete'] else 'No'}")

            if solution.get('unplaced'):
                print(f"\n⚠ Warning: {len(solution['unplaced'])} items unplaced")

            return True
        else:
            print(f"\n✗ FAILED!")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


def test_template_download():
    """Test the template download endpoint."""
    print("\n" + "=" * 60)
    print("TEST 2: Template Download")
    print("=" * 60)

    try:
        print("\nDownloading template from /api/download-template...")
        response = requests.get(f"{BASE_URL}/api/download-template", timeout=10)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            content_length = len(response.content)

            print("\n✓ SUCCESS!")
            print(f"  Content-Type: {content_type}")
            print(f"  File size: {content_length} bytes")

            # Check if it's an Excel file
            if 'spreadsheet' in content_type or content_length > 5000:
                print("  ✓ Valid Excel file received")

                # Save for inspection
                with open('/tmp/template_test.xlsx', 'wb') as f:
                    f.write(response.content)
                print("  Saved to: /tmp/template_test.xlsx")
                return True
            else:
                print("  ✗ Response doesn't look like an Excel file")
                return False
        else:
            print(f"\n✗ FAILED!")
            print(f"Status: {response.status_code}")
            return False

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


def test_excel_upload():
    """Test the Excel upload endpoint with the downloaded template."""
    print("\n" + "=" * 60)
    print("TEST 3: Excel Upload")
    print("=" * 60)

    try:
        # First download the template
        print("\nDownloading template...")
        response = requests.get(f"{BASE_URL}/api/download-template", timeout=10)

        if response.status_code != 200:
            print("✗ Failed to download template")
            return False

        # Upload it back
        print("Uploading template to /api/upload-excel...")
        files = {'file': ('test.xlsx', BytesIO(response.content), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

        upload_response = requests.post(
            f"{BASE_URL}/api/upload-excel",
            files=files,
            timeout=10
        )

        if upload_response.status_code == 200:
            data = upload_response.json()
            print("\n✓ SUCCESS!")
            print(f"\nParsed data:")
            print(f"  Products found: {data.get('count', 0)}")

            if data.get('warnings'):
                print(f"  Warnings: {len(data['warnings'])}")

            if data.get('products'):
                print(f"\n  Sample product:")
                product = data['products'][0]
                print(f"    Name: {product['name']}")
                print(f"    Code: {product['code']}")
                print(f"    Dimensions: {product['length']} x {product['width']} x {product['thickness']}")
                print(f"    Grain: {product['grain']}")
                print(f"    Qty: {product['qty']}")

            return True
        else:
            print(f"\n✗ FAILED!")
            print(f"Status: {upload_response.status_code}")
            print(f"Response: {upload_response.text}")
            return False

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


def test_health():
    """Test the health endpoint."""
    print("\n" + "=" * 60)
    print("TEST 0: Server Health Check")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Server is {data['status']}")
            print(f"  Version: {data['version']}")
            return True
        else:
            print(f"\n✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"\n✗ Cannot connect to server: {e}")
        print("\nMake sure the server is running:")
        print("  cd webapp && source venv/bin/activate && python app.py")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("WEBAPP FUNCTIONALITY TEST SUITE")
    print("=" * 60)
    print(f"Testing server at: {BASE_URL}")

    results = []

    # Run tests
    results.append(("Health Check", test_health()))

    if results[0][1]:  # Only continue if server is healthy
        results.append(("Manual Input", test_manual_input()))
        results.append(("Template Download", test_template_download()))
        results.append(("Excel Upload", test_excel_upload()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        exit(0)
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        exit(1)
