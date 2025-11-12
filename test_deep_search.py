"""
Deep search optimization for manual1.xlsx with extended time and validation.

This runs the algorithm with:
- Extended time limits (600s = 10 minutes)
- More pattern generation (20000 patterns)
- Strict validation of all solutions
- Multiple trials to find best valid solution
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

bins = [
    Bin(id="2440x1220", width=2440, height=1220, thickness=16, material="HS00", available=-1),
]

# Create problem with EXTENDED time limit
problem = Problem(
    items=items,
    bins=bins,
    kerf=3.0,
    time_limit=600.0  # 10 minutes per trial
)

print("="*70)
print(" DEEP SEARCH OPTIMIZATION - EXTENDED TIME & VALIDATION")
print("="*70)
print(f"\nConfiguration:")
print(f"  - Time limit per trial: {problem.time_limit}s (10 minutes)")
print(f"  - Pattern generation: 20000+ patterns")
print(f"  - MIP time limit: 120s")
print(f"  - Validation: Strict (all 80 items must be placed)")
print()

def validate_solution(solution, items):
    """Validate that solution places all items exactly."""
    placed_counts = defaultdict(int)
    for bin_packing in solution.bins:
        for placed_item in bin_packing.items:
            placed_counts[placed_item.item.id] += 1

    total_required = sum(item.quantity for item in items)
    total_placed = sum(placed_counts.values())

    if total_placed != total_required:
        return False, f"Placed {total_placed}/{total_required} items"

    for item in items:
        if placed_counts[item.id] != item.quantity:
            return False, f"Item {item.id}: {placed_counts[item.id]}/{item.quantity}"

    return True, "All items placed correctly"

# Run multiple trials
num_trials = 10
best_valid_solution = None
best_bins = float('inf')

print(f"Running {num_trials} deep search trials...")
print("-"*70)

for trial in range(num_trials):
    print(f"\nTrial {trial+1}/{num_trials}:")

    import random
    random.seed(42 + trial)

    # Use increased pattern count
    packer = ColumnGenerationPacker(time_limit=600.0, num_patterns=20000)
    solution = packer.solve(problem)

    # Validate solution
    is_valid, msg = validate_solution(solution, items)

    status = "✓ VALID" if is_valid else f"✗ INVALID ({msg})"
    print(f"  Result: {solution.num_bins()} boards, {solution.total_utilization():.2%} util - {status}")

    if is_valid and solution.num_bins() < best_bins:
        best_bins = solution.num_bins()
        best_valid_solution = solution
        print(f"  → NEW BEST: {best_bins} boards!")

        # If we found a 10-board solution, show details
        if best_bins <= 10:
            print(f"  🎯 TARGET ACHIEVED! Stopping early.")
            break

print("\n" + "="*70)
print(" BEST VALID SOLUTION FOUND")
print("="*70)

if best_valid_solution:
    print(f"\n✓ Boards used: {best_valid_solution.num_bins()}")
    print(f"✓ Average utilization: {best_valid_solution.total_utilization():.2%}")
    print(f"✓ Execution time: {best_valid_solution.metadata.get('execution_time', 0):.2f}s")

    # Calculate waste
    total_bin_area = best_valid_solution.num_bins() * bins[0].area()
    total_item_area = sum(item.area() * item.quantity for item in items)
    total_waste = total_bin_area - total_item_area

    print(f"\nMaterial efficiency:")
    print(f"  Material used: {total_bin_area:,.0f} mm²")
    print(f"  Item area: {total_item_area:,.0f} mm²")
    print(f"  Waste: {total_waste:,.0f} mm² ({(total_waste/total_bin_area)*100:.2f}%)")

    print(f"\nPer-board utilization:")
    for i, bp in enumerate(best_valid_solution.bins, 1):
        print(f"  Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

    print("\n" + "="*70)
    if best_valid_solution.num_bins() <= 10:
        print(" 🎯 SUCCESS! Achieved 10-board or better solution!")
    else:
        print(f" Best valid result: {best_valid_solution.num_bins()} boards")
    print("="*70)
else:
    print("\n✗ No valid solutions found")
    print("="*70)
