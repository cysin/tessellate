"""Verify a solution for correctness"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker
import random

# Set seed to reproduce the 9-board solution
random.seed(42 + 6)  # Trial 7 which got 9 boards

# Read test data
df = pd.read_excel('test_data/bench/manual1.xlsx')

# Convert to Problem format
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

packer = ColumnGenerationPacker(time_limit=60.0, num_patterns=10000)
solution = packer.solve(problem)

print("="*70)
print(" SOLUTION VERIFICATION")
print("="*70)
print(f"\nBins used: {solution.num_bins()}")
print(f"Complete: {solution.is_complete()}")
print(f"Unplaced: {len(solution.unplaced)}")

# Count items placed
print("\n" + "="*70)
print(" ITEM COUNT VERIFICATION")
print("="*70)

from collections import defaultdict
placed_counts = defaultdict(int)

for bin_packing in solution.bins:
    for placed_item in bin_packing.items:
        placed_counts[placed_item.item.id] += 1

print("\nRequired vs Placed:")
total_required = 0
total_placed = 0
all_correct = True

for item in items:
    required = item.quantity
    placed = placed_counts.get(item.id, 0)
    total_required += required
    total_placed += placed
    status = "✓" if placed == required else "✗"
    print(f"  {item.id}: required={required:2d}, placed={placed:2d} {status}")
    if placed != required:
        all_correct = False
        if placed > required:
            print(f"    WARNING: {placed - required} extra items placed!")
        else:
            print(f"    ERROR: {required - placed} items missing!")

print(f"\nTotal: required={total_required}, placed={total_placed}")
print(f"Item count correct: {all_correct}")

# Verify no overlaps
print("\n" + "="*70)
print(" OVERLAP VERIFICATION")
print("="*70)

has_overlaps = False
for i, bp in enumerate(solution.bins):
    if not bp.is_valid(problem.kerf):
        print(f"  Bin {i+1}: INVALID (overlaps or out of bounds)")
        has_overlaps = True
    else:
        print(f"  Bin {i+1}: Valid ({len(bp.items)} items, {bp.utilization():.2%} util)")

print(f"\nNo overlaps: {not has_overlaps}")

print("\n" + "="*70)
if all_correct and not has_overlaps:
    print(f" ✓ SOLUTION VERIFIED: {solution.num_bins()} boards is valid!")
else:
    print(" ✗ SOLUTION HAS ERRORS")
print("="*70)
