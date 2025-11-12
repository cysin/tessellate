"""Test Column Generation algorithm on manual1.xlsx"""

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
    time_limit=300.0
)

print("="*60)
print("COLUMN GENERATION ALGORITHM TEST")
print("="*60)
print("\nTest Data Summary:")
print(f"Total unique items: {len(items)}")
print(f"Total pieces: {sum(item.quantity for item in items)}")
print(f"Total area needed: {sum(item.area() * item.quantity for item in items):,.0f} mm²")
print(f"Board area: {bins[0].area():,.0f} mm²")
print(f"Theoretical minimum boards: {sum(item.area() * item.quantity for item in items) / bins[0].area():.2f}")
print()

# Test Column Generation algorithm
print("Running Column Generation algorithm...")
packer = ColumnGenerationPacker(time_limit=300.0, num_patterns=2000)
solution = packer.solve(problem)

print("\n" + "="*60)
print("RESULTS")
print("="*60)
print(f"Bins used: {solution.num_bins()}")
print(f"Utilization: {solution.total_utilization():.2%}")
print(f"Complete: {solution.is_complete()}")
print(f"Execution time: {solution.metadata.get('execution_time', 0):.2f}s")

if solution.unplaced:
    print(f"\nUnplaced items: {len(solution.unplaced)}")
    for item, qty in solution.unplaced:
        print(f"  - {item.id}: {qty} pieces")

# Show per-bin utilization
print("\nPer-bin utilization:")
for i, bp in enumerate(solution.bins):
    print(f"  Bin {i+1}: {bp.utilization():.2%} ({len(bp.items)} items)")

# Calculate waste
total_bin_area = solution.num_bins() * bins[0].area()
total_item_area = sum(item.area() * item.quantity for item in items)
total_waste = total_bin_area - total_item_area
waste_percentage = (total_waste / total_bin_area) * 100

print(f"\nTotal waste: {total_waste:,.0f} mm² ({waste_percentage:.2f}%)")
print(f"Total material used: {total_bin_area:,.0f} mm²")
print(f"Total items area: {total_item_area:,.0f} mm²")

print("\n" + "="*60)
if solution.num_bins() <= 10:
    print("🎯 SUCCESS! Achieved 10 or fewer boards!")
else:
    print(f"⚠️  Need optimization - currently using {solution.num_bins()} boards")
print("="*60)
