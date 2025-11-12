"""Test Rotated Strip Packer"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.rotated_strip_packer import RotatedStripPacker

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
    time_limit=60.0
)

print("="*60)
print("ROTATED STRIP PACKER TEST")
print("="*60)
print(f"\nAll items rotatable: {all(item.rotatable for item in items)}")
print(f"Total pieces: {sum(item.quantity for item in items)}")
print(f"Total area: {sum(item.area() * item.quantity for item in items):,.0f} mm²")
print()

# Test Rotated Strip Packer
print("Running Rotated Strip Packer...")
packer = RotatedStripPacker(time_limit=60.0)
solution = packer.solve(problem)

print("\n" + "="*60)
print("RESULTS")
print("="*60)
print(f"Bins used: {solution.num_bins()}")
print(f"Average utilization: {solution.total_utilization():.2%}")
print(f"Complete: {solution.is_complete()}")
print(f"Execution time: {solution.metadata.get('execution_time', 0):.2f}s")

# Show per-bin details
print("\nPer-bin utilization:")
for i, bp in enumerate(solution.bins):
    print(f"  Bin {i+1}: {bp.utilization():.2%} ({len(bp.items)} items)")

# Calculate waste
total_bin_area = solution.num_bins() * bins[0].area()
total_item_area = sum(item.area() * item.quantity for item in items)
total_waste = total_bin_area - total_item_area

print(f"\nTotal waste: {total_waste:,.0f} mm² ({(total_waste/total_bin_area)*100:.2f}%)")
print(f"Required for 10 boards: {(total_item_area / (10 * bins[0].area())) * 100:.2f}% utilization")

print("\n" + "="*60)
if solution.num_bins() <= 10:
    print("🎯 SUCCESS! Achieved 10 or fewer boards!")
else:
    print(f"Current: {solution.num_bins()} boards (target: 10)")
print("="*60)
