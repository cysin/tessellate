"""
Test Uniform Height Algorithm

Tests the specialized algorithm for items with uniform height.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.uniform_height_algorithm import UniformHeightAlgorithm
import time

print("="*70)
print(" UNIFORM HEIGHT ALGORITHM TEST")
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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=300.0)

print(f"Test Data: manual1.xlsx")
print(f"  Items: {len(items)} types, {sum(item.quantity for item in items)} total pieces")
print(f"  Board: {bins[0].width}×{bins[0].height}mm")
print()

# Calculate theoretical values
total_area = sum(item.area() * item.quantity for item in items)
board_area = bins[0].area()
theoretical_min = total_area / board_area

print(f"Theoretical Analysis:")
print(f"  Total item area: {total_area:,.0f} mm²")
print(f"  Board area: {board_area:,.0f} mm²")
print(f"  Theoretical minimum (no waste): {theoretical_min:.2f} boards")
print()
print(f"  10 boards = {board_area * 10:,.0f} mm²")
print(f"  Required avg utilization for 10 boards: {(total_area / (board_area * 10)) * 100:.2f}%")
print()

# Test uniform height algorithm
packer = UniformHeightAlgorithm(time_limit=300.0)

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
    print()

    # Check if we achieved 10 boards
    if boards == 10:
        print("="*70)
        print(" ★★★ SUCCESS: ACHIEVED 10-BOARD SOLUTION! ★★★")
        print("="*70)
        print()
        print("This is the target solution we were looking for!")
        print(f"Average utilization: {avg_util:.2%}")
        print(f"This {'meets' if avg_util >= 0.90 else 'does not meet'} the >90% utilization target.")
    elif boards < 10:
        print("="*70)
        print(f" ★★★ EVEN BETTER: {boards} BOARDS! ★★★")
        print("="*70)
        print()
        print(f"Exceeded expectations! Found {boards}-board solution.")
    else:
        print(f"Result: {boards} boards (target was 10 boards)")
        print(f"Difference: {boards - 10} extra boards")
else:
    print(f"⚠️  Warning: Did not place all items ({items_placed}/{items_required})")

print()
print("="*70)
print(" COMPARISON WITH OTHER ALGORITHMS")
print("="*70)
print()
print("Results comparison:")
print("  Strip Packing: 12 boards @ 78.96%")
print("  Guillotine: 11 boards @ 85.81%")
print("  Column Generation: 11-12 boards @ 78-86%")
print(f"  Uniform Height: {boards} boards @ {avg_util:.2%}")
print()
print("="*70)
print("TEST COMPLETE")
print("="*70)
