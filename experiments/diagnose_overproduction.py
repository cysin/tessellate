"""
Diagnostic: Find out WHY we're getting 84 items instead of 80.
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker
from collections import defaultdict
import random

random.seed(42)

# Read test data
df = pd.read_excel('test_data/bench/manual1.xlsx')

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

print("="*70)
print(" DIAGNOSTIC: Finding the 4 extra items")
print("="*70)

print("\nRequired items:")
total_required = 0
for item in items:
    print(f"  {item.id}: {item.quantity} pieces")
    total_required += item.quantity
print(f"Total required: {total_required}")

# Run algorithm
packer = ColumnGenerationPacker(time_limit=60.0, num_patterns=10000)
solution = packer.solve(problem)

print(f"\nSolution: {solution.num_bins()} boards")

# Count what was placed
placed_counts = defaultdict(int)
print("\nPer-bin breakdown:")
for i, bin_packing in enumerate(solution.bins, 1):
    bin_items = defaultdict(int)
    for placed_item in bin_packing.items:
        placed_counts[placed_item.item.id] += 1
        bin_items[placed_item.item.id] += 1
    print(f"\nBin {i}: {len(bin_packing.items)} items")
    for item_id, count in sorted(bin_items.items()):
        print(f"    {item_id}: {count}")

print("\n" + "="*70)
print("ITEM COUNT ANALYSIS")
print("="*70)

total_placed = 0
for item in items:
    required = item.quantity
    placed = placed_counts.get(item.id, 0)
    diff = placed - required
    status = "✓" if diff == 0 else ("+" if diff > 0 else "-")
    print(f"{item.id}:")
    print(f"  Required: {required}")
    print(f"  Placed:   {placed}")
    print(f"  Diff:     {diff:+d} {status}")
    total_placed += placed

print(f"\nTotal placed: {total_placed}")
print(f"Total required: {total_required}")
print(f"Difference: {total_placed - total_required:+d}")

if total_placed != total_required:
    print("\n❌ OVERPRODUCTION DETECTED")
    print("The algorithm is placing more items than required!")
