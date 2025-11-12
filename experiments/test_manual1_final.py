"""
Final verification test for manual1.xlsx - 10 board solution.

This demonstrates the optimized Column Generation algorithm with rotated patterns.
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

# Standard board size (2440mm x 1220mm)
bins = [
    Bin(id="2440x1220", width=2440, height=1220, thickness=16, material="HS00", available=-1),
]

# Create problem with kerf=3mm
problem = Problem(
    items=items,
    bins=bins,
    kerf=3.0,
    time_limit=600.0
)

print("="*70)
print(" MANUAL1.XLSX - 10 BOARD SOLUTION VERIFICATION")
print("="*70)
print("\nProblem Specification:")
print(f"  - Board size: {bins[0].width}mm x {bins[0].height}mm")
print(f"  - Board area: {bins[0].area():,.0f} mm²")
print(f"  - Material: {bins[0].material}")
print(f"  - Thickness: {bins[0].thickness}mm")
print(f"  - Kerf (blade width): {problem.kerf}mm")

print(f"\nItems to cut:")
print(f"  - Unique items: {len(items)}")
print(f"  - Total pieces: {sum(item.quantity for item in items)}")
print(f"  - All rotatable: {all(item.rotatable for item in items)}")
print(f"  - Total area needed: {sum(item.area() * item.quantity for item in items):,.0f} mm²")

theoretical_min = sum(item.area() * item.quantity for item in items) / bins[0].area()
print(f"\nTheoretical Analysis:")
print(f"  - Theoretical minimum (no waste): {theoretical_min:.2f} boards")
print(f"  - Target: 10 boards")
print(f"  - Required utilization: {(sum(item.area() * item.quantity for item in items) / (10 * bins[0].area())) * 100:.2f}%")

print("\n" + "-"*70)
print("Running Column Generation Algorithm...")
print("-"*70)

# Solve using Column Generation with rotated patterns
packer = ColumnGenerationPacker(time_limit=600.0, num_patterns=10000)
solution = packer.solve(problem)

print("\n" + "="*70)
print(" SOLUTION RESULTS")
print("="*70)
print(f"\n✓ Bins used: {solution.num_bins()} boards")
print(f"✓ Average utilization: {solution.total_utilization():.2%}")
print(f"✓ All items placed: {solution.is_complete()}")
print(f"✓ Execution time: {solution.metadata.get('execution_time', 0):.2f}s")
print(f"✓ Algorithm: {solution.metadata.get('algorithm', 'Unknown')}")

# Detailed statistics
total_bin_area = solution.num_bins() * bins[0].area()
total_item_area = sum(item.area() * item.quantity for item in items)
total_waste = total_bin_area - total_item_area

print(f"\nMaterial Usage:")
print(f"  - Total material: {total_bin_area:,.0f} mm²")
print(f"  - Item area: {total_item_area:,.0f} mm²")
print(f"  - Waste: {total_waste:,.0f} mm² ({(total_waste/total_bin_area)*100:.2f}%)")

print(f"\nPer-board details:")
utilizations = sorted([bp.utilization() for bp in solution.bins], reverse=True)
for i, util in enumerate(utilizations, 1):
    print(f"  Board {i:2d}: {util:6.2%} utilization")

print("\n" + "="*70)
if solution.num_bins() <= 10:
    print(" 🎯 SUCCESS! Achieved 10-board solution with minimal waste!")
    print(f" Average utilization: {solution.total_utilization():.2%}")
else:
    print(f" Result: {solution.num_bins()} boards (target was 10)")
print("="*70)
