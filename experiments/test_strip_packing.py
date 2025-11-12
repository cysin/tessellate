"""
Test Strip Packing Algorithm

Tests the simple row-by-row strip packing algorithm.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.strip_packing import StripPackingAlgorithm
import time

print("="*70)
print(" STRIP PACKING ALGORITHM TEST")
print("="*70)
print()

# Read test data
df = pd.read_excel('../test_data/bench/manual1.xlsx')

items = []
for _, row in df.iterrows():
    item = Item(
        id=row['Code'],
        width=float(row['Width']),
        height=float(row['Height']),
        thickness=float(row['Thickness']),
        material=row['Color'],
        quantity=int(row['Qty']),
        rotatable=(row['Grain'] == 'mixed')
    )
    items.append(item)

bins = [
    Bin(id="2440x1220", width=2440, height=1220, thickness=16, material="HS00", available=-1),
]

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=60.0)

print(f"Test Data: manual1.xlsx")
print(f"  Items: {len(items)} types, {sum(item.quantity for item in items)} total pieces")
print(f"  Board: {bins[0].width}×{bins[0].height}mm")
print()

print("Algorithm: Strip Packing")
print("  Strategy: Arrange items in horizontal rows")
print("  1. Pack items in rows, maximizing width")
print("  2. Stack rows vertically, maximizing height")
print("  3. Try different sorting strategies")
print("  4. Support rotation for better fit")
print()

# Test strip packing
packer = StripPackingAlgorithm(
    time_limit=60.0,
    max_trials=100
)

start = time.time()
solution = packer.solve(problem)
elapsed = time.time() - start

boards = len(solution.bins)
utils = [bp.utilization() for bp in solution.bins]
avg_util = sum(utils) / len(utils) if utils else 0
items_placed = sum(len(bp.items) for bp in solution.bins)
items_required = sum(item.quantity for item in items)

print()
print(f"{'='*70}")
print(" RESULTS")
print(f"{'='*70}")
print(f"Boards: {boards}")
print(f"Average Utilization: {avg_util:.2%}")
print(f"Items Placed: {items_placed}/{items_required}")
print(f"Valid: {'✓' if items_placed == items_required else '✗'}")
print(f"Time: {elapsed:.2f}s")
print()

if items_placed == items_required:
    print("Per-board details:")
    for i, bp in enumerate(solution.bins, 1):
        rotated_count = sum(1 for pi in bp.items if pi.rotated)
        print(f"  Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items, {rotated_count} rotated)")

    print()
    print("Board utilization distribution:")
    print(f"  Min: {min(utils):.2%}")
    print(f"  Max: {max(utils):.2%}")
    print(f"  Avg: {avg_util:.2%}")
    print(f"  Range: {max(utils) - min(utils):.2%}")
else:
    print(f"⚠️  Warning: Did not place all items ({items_placed}/{items_required})")
    if solution.unplaced:
        print(f"  Unplaced items: {len(solution.unplaced)}")

print()
print("="*70)
print(" ALGORITHM CHARACTERISTICS")
print("="*70)
print()
print("Advantages:")
print("  ✓ Simple and fast")
print("  ✓ Deterministic results")
print("  ✓ Works well for similar-height items")
print("  ✓ Intelligent rotation selection")
print("  ✓ No complex guillotine logic needed")
print()
print("Best use cases:")
print("  • Items with similar heights")
print("  • Quick solutions needed")
print("  • When simplicity is important")
print()
print("="*70)
print("TEST COMPLETE")
print("="*70)
