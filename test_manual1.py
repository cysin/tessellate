"""Test current algorithm on manual1.xlsx"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.guillotine import GuillotinePacker

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
        rotatable=(row['Grain'] == 'mixed')  # mixed means rotatable
    )
    items.append(item)

# Standard board sizes (common plywood sizes)
bins = [
    Bin(id="2440x1220", width=2440, height=1220, thickness=16, material="HS00", available=-1),
]

# Create problem
problem = Problem(
    items=items,
    bins=bins,
    kerf=3.0,
    time_limit=30.0
)

print("Test Data Summary:")
print(f"Total unique items: {len(items)}")
print(f"Total pieces: {sum(item.quantity for item in items)}")
print(f"Total area needed: {sum(item.area() * item.quantity for item in items):,.0f} mm²")
print(f"Board area: {bins[0].area():,.0f} mm²")
print(f"Theoretical minimum boards (ignoring waste): {sum(item.area() * item.quantity for item in items) / bins[0].area():.2f}")
print()

# Test current algorithm
print("Testing current Guillotine algorithm...")
packer = GuillotinePacker(time_limit=30.0)
solution = packer.solve(problem)

print(f"\nCurrent Algorithm Results:")
print(f"Bins used: {solution.num_bins()}")
print(f"Utilization: {solution.total_utilization():.2%}")
print(f"Complete: {solution.is_complete()}")
if solution.unplaced:
    print(f"Unplaced items: {len(solution.unplaced)}")
    for item, qty in solution.unplaced:
        print(f"  - {item.id}: {qty} pieces")

# Show per-bin utilization
print("\nPer-bin utilization:")
for i, bp in enumerate(solution.bins):
    print(f"  Bin {i+1}: {bp.utilization():.2%} ({len(bp.items)} items)")
