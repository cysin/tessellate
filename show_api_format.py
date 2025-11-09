#!/usr/bin/env python3
"""
Demonstration of the Tessellate API Input and Output Format
============================================================
"""

import json
import requests

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TESSELLATE API INPUT/OUTPUT FORMAT DEMONSTRATION")
print("=" * 80)

# ============================================================================
# INPUT FORMAT
# ============================================================================

print("\n" + "=" * 80)
print("INPUT FORMAT (JSON sent to /api/solve)")
print("=" * 80)

input_format = {
    "items": [
        {
            "id": "ITEM-001",              # Unique identifier for the item
            "name": "Cabinet Door",        # Human-readable name (optional)
            "code": "CAB-001",            # Product code (optional)
            "width": 800,                 # Width in mm (number)
            "height": 600,                # Height in mm (number)
            "thickness": 18,              # Thickness in mm (number)
            "material": "Oak",            # Material/color name (string)
            "quantity": 2,                # How many pieces needed (integer)
            "rotatable": False            # Can rotate 90 degrees? (boolean)
        },
        {
            "id": "ITEM-002",
            "name": "Shelf",
            "code": "SHF-001",
            "width": 1200,
            "height": 400,
            "thickness": 18,
            "material": "Oak",
            "quantity": 3,
            "rotatable": True
        }
    ],

    "bins": [
        {
            "id": "STD-Board-Oak-18mm",   # Unique identifier for board type
            "width": 2440,                # Board width in mm (number)
            "height": 1220,               # Board height in mm (number)
            "thickness": 18,              # Board thickness in mm (number)
            "material": "Oak",            # Material/color name (must match items)
            "available": -1               # Number available (-1 = unlimited)
        }
    ],

    "parameters": {
        "kerf": 3.5,                      # Saw blade width in mm (number)
        "utilizationThreshold": 0.78,     # Minimum utilization ratio (0.0-1.0)
        "timeLimit": 10.0                 # Maximum solving time in seconds
    }
}

print("\nINPUT STRUCTURE:")
print(json.dumps(input_format, indent=2))

print("\n" + "-" * 80)
print("FIELD DESCRIPTIONS:")
print("-" * 80)
print("""
ITEMS (array of parts to cut):
  - id:         Unique identifier (string)
  - name:       Display name (string, optional)
  - code:       Product code (string, optional)
  - width:      Width in millimeters (number)
  - height:     Height in millimeters (number)
  - thickness:  Thickness in millimeters (number)
  - material:   Material/color identifier (string)
  - quantity:   Number of pieces needed (integer >= 1)
  - rotatable:  Can be rotated 90 degrees (boolean)

BINS (array of available board types):
  - id:         Unique identifier (string)
  - width:      Board width in millimeters (number)
  - height:     Board height in millimeters (number)
  - thickness:  Board thickness in millimeters (number)
  - material:   Material/color identifier (string)
  - available:  Number of boards available (-1 = unlimited, integer)

PARAMETERS:
  - kerf:                  Saw blade width in mm (number, typically 3-4mm)
  - utilizationThreshold:  Minimum board utilization (0.0-1.0, typically 0.7-0.85)
  - timeLimit:             Maximum solving time in seconds (number)

IMPORTANT CONSTRAINTS:
  - Each board can only contain items of ONE material/thickness
  - Item dimensions must fit within board dimensions (considering kerf)
  - Item thickness must match board thickness
  - Item material must match board material
""")

# ============================================================================
# OUTPUT FORMAT
# ============================================================================

print("\n" + "=" * 80)
print("OUTPUT FORMAT (JSON returned from /api/solve)")
print("=" * 80)

output_format = {
    "metadata": {
        "binsUsed": 2,                    # Total number of physical boards used
        "isComplete": True,               # All items placed successfully?
        "totalItems": 5,                  # Total number of item pieces
        "utilization": 0.82,              # Overall utilization ratio (0.0-1.0)
        "validated": True                 # Solution is valid?
    },

    "bins": [
        {
            "binId": 0,                   # Board index
            "binType": "STD-Board-Oak-18mm",  # Board type identifier
            "width": 2440.0,              # Board width
            "height": 1220.0,             # Board height
            "thickness": 18.0,            # Board thickness
            "material": "Oak",            # Board material
            "utilization": 0.85,          # This board's utilization (0.0-1.0)
            "quantity": 2,                # Number of identical boards (aggregated)

            "items": [                    # Items placed on this board
                {
                    "itemId": "ITEM-001", # Item identifier
                    "x": 0,               # X position on board (bottom-left corner)
                    "y": 0,               # Y position on board (bottom-left corner)
                    "width": 800.0,       # Item width (after rotation if rotated)
                    "height": 600.0,      # Item height (after rotation if rotated)
                    "thickness": 18.0,    # Item thickness
                    "material": "Oak",    # Item material
                    "rotated": False      # Was item rotated 90 degrees?
                },
                {
                    "itemId": "ITEM-002",
                    "x": 803.5,           # X position (800 + 3.5 kerf)
                    "y": 0,
                    "width": 1200.0,
                    "height": 400.0,
                    "thickness": 18.0,
                    "material": "Oak",
                    "rotated": False
                }
            ],

            "cuts": [                     # Guillotine cuts (for visualization)
                {
                    "type": "vertical",   # Cut direction: "vertical" or "horizontal"
                    "position": 800.0,    # Cut position along the axis
                    "start": 0,           # Cut start coordinate
                    "end": 600.0          # Cut end coordinate
                }
            ]
        }
    ],

    "unplaced": [                         # Items that couldn't be placed
        {
            "itemId": "ITEM-XXX",
            "quantity": 1,                # How many pieces couldn't be placed
            "reason": "Does not fit"      # Why it couldn't be placed
        }
    ]
}

print("\nOUTPUT STRUCTURE:")
print(json.dumps(output_format, indent=2))

print("\n" + "-" * 80)
print("OUTPUT FIELD DESCRIPTIONS:")
print("-" * 80)
print("""
METADATA:
  - binsUsed:     Total physical boards used (integer)
  - isComplete:   True if all items placed successfully (boolean)
  - totalItems:   Total number of item pieces to place (integer)
  - utilization:  Overall material utilization 0.0-1.0 (number)
  - validated:    Solution passed validation (boolean)

BINS (array of board groups - aggregated by identical layout):
  - binId:        Board index/identifier (integer)
  - binType:      Board type identifier (string)
  - width:        Board width in mm (number)
  - height:       Board height in mm (number)
  - thickness:    Board thickness in mm (number)
  - material:     Board material identifier (string)
  - utilization:  This board's utilization 0.0-1.0 (number)
  - quantity:     Number of identical boards (integer) **AGGREGATED**

  - items:        Array of items on this board
    - itemId:     Item identifier from input (string)
    - x:          X coordinate (left edge) in mm (number)
    - y:          Y coordinate (bottom edge) in mm (number)
    - width:      Item width in mm after rotation (number)
    - height:     Item height in mm after rotation (number)
    - thickness:  Item thickness in mm (number)
    - material:   Item material (string)
    - rotated:    Was rotated 90 degrees? (boolean)

  - cuts:         Guillotine cut sequence for visualization
    - type:       "vertical" or "horizontal" (string)
    - position:   Cut position along axis in mm (number)
    - start:      Cut start coordinate in mm (number)
    - end:        Cut end coordinate in mm (number)

UNPLACED (array of items that couldn't be placed):
  - itemId:       Item identifier (string)
  - quantity:     Number of pieces not placed (integer)
  - reason:       Why it couldn't be placed (string)

AGGREGATION LOGIC:
  - Boards with identical layouts are grouped together
  - "quantity" field indicates how many identical boards
  - Example: quantity=3 means make 3 copies of this board layout
  - Aggregation ignores item ID/name, only considers:
    * Board dimensions, material, thickness
    * Item positions, dimensions, material, thickness
    * Item rotation state
""")

# ============================================================================
# REAL EXAMPLE
# ============================================================================

print("\n" + "=" * 80)
print("REAL EXAMPLE - SOLVING A SIMPLE PROBLEM")
print("=" * 80)

# Simple real problem
real_input = {
    'items': [
        {
            'id': 'PART-A',
            'name': 'Part A',
            'code': 'PA-001',
            'width': 600,
            'height': 400,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 2,
            'rotatable': False
        },
        {
            'id': 'PART-B',
            'name': 'Part B',
            'code': 'PB-001',
            'width': 800,
            'height': 500,
            'thickness': 16,
            'material': 'HS00',
            'quantity': 1,
            'rotatable': True
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
        'utilizationThreshold': 0.78,
        'timeLimit': 10.0
    }
}

print("\nREAL INPUT:")
print(json.dumps(real_input, indent=2))

# Make the API call
try:
    response = requests.post(
        f"{BASE_URL}/api/solve",
        json=real_input,
        timeout=15
    )

    if response.status_code == 200:
        result = response.json()

        print("\n" + "=" * 80)
        print("REAL OUTPUT:")
        print("=" * 80)
        print(json.dumps(result, indent=2))

        print("\n" + "=" * 80)
        print("SOLUTION SUMMARY:")
        print("=" * 80)
        print(f"Boards used: {result['metadata']['binsUsed']}")
        print(f"All items placed: {result['metadata']['isComplete']}")
        print(f"Overall utilization: {result['metadata']['utilization']*100:.1f}%")
        print(f"Number of board groups: {len(result['bins'])}")

        for i, board in enumerate(result['bins'], 1):
            qty = board.get('quantity', 1)
            print(f"\nBoard Group {i}:")
            print(f"  Quantity: {qty} (make {qty} copies of this layout)")
            print(f"  Material: {board['material']}")
            print(f"  Board size: {board['height']} x {board['width']} x {board['thickness']} mm")
            print(f"  Utilization: {board['utilization']*100:.1f}%")
            print(f"  Items on each board: {len(board['items'])}")
            for item in board['items']:
                rot_str = " (rotated)" if item['rotated'] else ""
                print(f"    - {item['itemId']}: {item['width']}x{item['height']} at ({item['x']}, {item['y']}){rot_str}")

        if result.get('unplaced'):
            print("\nUnplaced items:")
            for unplaced in result['unplaced']:
                print(f"  - {unplaced['itemId']}: {unplaced['quantity']} pieces")
        else:
            print("\n✓ All items successfully placed!")

    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("\n✗ Error: Server not running")
    print("Please start the server with: python webapp/app.py")
except Exception as e:
    print(f"\n✗ Error: {e}")

print("\n" + "=" * 80)
print("KEY POINTS:")
print("=" * 80)
print("""
1. INPUT must include items, bins, and parameters
2. OUTPUT includes metadata, bins (aggregated), and unplaced items
3. Coordinates use bottom-left corner as (x, y)
4. All dimensions in millimeters
5. Kerf is automatically applied between cuts
6. Boards are AGGREGATED by identical layout
7. Use 'quantity' field to know how many copies to make
8. Items with same dimensions/material are treated as identical for cutting
   (ID/name doesn't matter for aggregation)
""")
