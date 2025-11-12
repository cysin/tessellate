"""
Final push to achieve 10 boards - generate many high-quality patterns.
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

# Create problem with extended time
problem = Problem(
    items=items,
    bins=bins,
    kerf=3.0,
    time_limit=600.0
)

print("="*60)
print("FINAL PUSH FOR 10 BOARDS")
print("="*60)

print("\nProblem Analysis:")
print(f"- Total pieces: {sum(item.quantity for item in items)}")
print(f"- Total area: {sum(item.area() * item.quantity for item in items):,.0f} mm²")
print(f"- Board area: {bins[0].area():,.0f} mm²")
print(f"- Theoretical minimum: {sum(item.area() * item.quantity for item in items) / bins[0].area():.2f} boards")
print(f"- Target utilization for 10 boards: {(sum(item.area() * item.quantity for item in items) / (10 * bins[0].area())) * 100:.2f}%")
print()

print("Generating 10000 patterns with extended time...")
packer = ColumnGenerationPacker(time_limit=600.0, num_patterns=10000)
solution = packer.solve(problem)

print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)
print(f"Bins used: {solution.num_bins()}")
print(f"Average utilization: {solution.total_utilization():.2%}")
print(f"Complete: {solution.is_complete()}")
print(f"Execution time: {solution.metadata.get('execution_time', 0):.2f}s")

if solution.num_bins() <= 10:
    print("\n🎯 SUCCESS! Achieved 10 or fewer boards!")
else:
    print(f"\n⚠️  Result: {solution.num_bins()} boards (target: 10)")

# Show detailed utilization
print("\nDetailed per-bin utilization:")
for i, bp in enumerate(solution.bins):
    item_list = ", ".join([f"{pi.item.id.split('-')[2]}x{pi.item.id.split('-')[3]}" for pi in bp.items])
    print(f"  Bin {i+1}: {bp.utilization():.2%} - {len(bp.items)} items - {item_list[:80]}")

print("="*60)
