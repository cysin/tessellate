"""
Improved column generation with smarter pattern generation.
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
    time_limit=600.0  # Give it more time
)

print("="*60)
print("IMPROVED COLUMN GENERATION TEST")
print("="*60)
print("\nItem details:")
for item in items:
    print(f"  {item.id}: {item.width}x{item.height} x{item.quantity} = {item.area() * item.quantity:,.0f} mm²")

print(f"\nTotal area needed: {sum(item.area() * item.quantity for item in items):,.0f} mm²")
print(f"Board area: {bins[0].area():,.0f} mm²")
print(f"Theoretical minimum: {sum(item.area() * item.quantity for item in items) / bins[0].area():.2f} boards")
print()

# Test with more patterns
print("Running Column Generation with 5000 patterns...")
packer = ColumnGenerationPacker(time_limit=600.0, num_patterns=5000)
solution = packer.solve(problem)

print("\n" + "="*60)
print("RESULTS")
print("="*60)
print(f"Bins used: {solution.num_bins()}")
print(f"Utilization: {solution.total_utilization():.2%}")
print(f"Complete: {solution.is_complete()}")
print(f"Execution time: {solution.metadata.get('execution_time', 0):.2f}s")

# Show per-bin utilization
print("\nTop 15 bins by utilization:")
sorted_bins = sorted(enumerate(solution.bins), key=lambda x: -x[1].utilization())
for rank, (i, bp) in enumerate(sorted_bins[:15], 1):
    print(f"  #{rank} Bin {i+1}: {bp.utilization():.2%} ({len(bp.items)} items)")

# Calculate waste
total_bin_area = solution.num_bins() * bins[0].area()
total_item_area = sum(item.area() * item.quantity for item in items)
total_waste = total_bin_area - total_item_area
waste_percentage = (total_waste / total_bin_area) * 100

print(f"\nTotal waste: {total_waste:,.0f} mm² ({waste_percentage:.2f}%)")
print(f"Avg utilization needed for 10 boards: {(total_item_area / (10 * bins[0].area())) * 100:.2f}%")

print("\n" + "="*60)
if solution.num_bins() <= 10:
    print("🎯 SUCCESS! Achieved 10 or fewer boards!")
elif solution.num_bins() == 11:
    print("⚠️  Close! Just 1 board away from target")
else:
    print(f"⚠️  Need optimization - currently using {solution.num_bins()} boards")
print("="*60)
