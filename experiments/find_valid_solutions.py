"""
Find what valid solutions the algorithm actually produces.
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker
from collections import defaultdict

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

bins = [Bin(id="2440x1220", width=2440, height=1220, thickness=16, material="HS00", available=-1)]
problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=60.0)

print("Finding valid solutions...")
print("="*70)

results = defaultdict(list)

for trial in range(30):
    import random
    random.seed(42 + trial)

    packer = ColumnGenerationPacker(time_limit=60.0, num_patterns=10000)
    solution = packer.solve(problem)

    # Verify solution
    placed_counts = defaultdict(int)
    for bin_packing in solution.bins:
        for placed_item in bin_packing.items:
            placed_counts[placed_item.item.id] += 1

    total_required = sum(item.quantity for item in items)
    total_placed = sum(placed_counts.values())

    is_valid = (total_placed == total_required and solution.is_complete())
    num_bins = solution.num_bins()

    if is_valid:
        results[num_bins].append((trial, solution.total_utilization()))
        status = "✓ VALID"
    else:
        status = f"✗ INVALID ({total_placed}/{total_required} items)"

    print(f"Trial {trial+1:2d}: {num_bins:2d} boards - {solution.total_utilization():.2%} util - {status}")

print("\n" + "="*70)
print("SUMMARY OF VALID SOLUTIONS:")
print("="*70)

for num_bins in sorted(results.keys()):
    count = len(results[num_bins])
    avg_util = sum(util for _, util in results[num_bins]) / count
    print(f"{num_bins} boards: {count} valid solutions, avg utilization {avg_util:.2%}")

if results:
    best_bins = min(results.keys())
    print(f"\n✓ Best valid solution: {best_bins} boards")
else:
    print(f"\n✗ No valid solutions found!")
