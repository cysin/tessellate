"""
Multi-start optimization to find the best solution for manual1.xlsx

Runs the algorithm multiple times with different random seeds and keeps the best result.
Prioritizes minimal bins, then minimal waste.
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker

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

# Standard board size
bins = [
    Bin(id="2440x1220", width=2440, height=1220, thickness=16, material="HS00", available=-1),
]

# Create problem
problem = Problem(
    items=items,
    bins=bins,
    kerf=3.0,
    time_limit=600.0
)

print("="*70)
print(" MULTI-START OPTIMIZATION FOR MANUAL1.XLSX")
print("="*70)
print(f"\nTarget: 10 boards with minimal waste")
print(f"Strategy: Run multiple trials with different random seeds\n")

# Run multiple trials
num_trials = 20  # Can increase for better results
best_solution = None
best_score = (float('inf'), float('inf'))  # (num_bins, waste)

print("Running trials...")
for trial in range(num_trials):
    # Each trial uses different random seed for pattern generation
    packer = ColumnGenerationPacker(time_limit=60.0, num_patterns=10000)

    # Modify random seed by trial number (hacky but works)
    import random
    random.seed(42 + trial)

    solution = packer.solve(problem)

    # Score: (bins, -utilization) - we want fewer bins and higher utilization
    score = (solution.num_bins(), -solution.total_utilization())

    status = "✓" if solution.num_bins() <= 10 else " "
    print(f"  Trial {trial+1:2d}: {solution.num_bins():2d} boards, {solution.total_utilization():.2%} util {status}")

    if score < best_score:
        best_score = score
        best_solution = solution
        if solution.num_bins() <= 10:
            print(f"    → New best: {solution.num_bins()} boards!")

    # Early exit if we found a perfect solution
    if solution.num_bins() == 10 and solution.total_utilization() > 0.90:
        print(f"\n  Found excellent 10-board solution, stopping early.")
        break

print("\n" + "="*70)
print(" BEST SOLUTION FOUND")
print("="*70)
print(f"\nBins used: {best_solution.num_bins()} boards")
print(f"Average utilization: {best_solution.total_utilization():.2%}")
print(f"Complete: {best_solution.is_complete()}")

# Calculate waste
total_bin_area = best_solution.num_bins() * bins[0].area()
total_item_area = sum(item.area() * item.quantity for item in items)
total_waste = total_bin_area - total_item_area

print(f"\nMaterial usage:")
print(f"  Total material: {total_bin_area:,.0f} mm²")
print(f"  Item area: {total_item_area:,.0f} mm²")
print(f"  Waste: {total_waste:,.0f} mm² ({(total_waste/total_bin_area)*100:.2f}%)")

print(f"\nPer-board utilization:")
sorted_bins = sorted(best_solution.bins, key=lambda x: -x.utilization())
for i, bp in enumerate(sorted_bins, 1):
    print(f"  Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

print("\n" + "="*70)
if best_solution.num_bins() <= 10:
    print(" 🎯 SUCCESS! Achieved 10-board solution!")
else:
    print(f" Best result: {best_solution.num_bins()} boards (target: 10)")
print("="*70)
