"""
Quick verification: Does a 10-board solution place all 80 items?
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker
from collections import defaultdict

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

bins = [
    Bin(id="2440x1220", width=2440, height=1220, thickness=16, material="HS00", available=-1),
]

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=60.0)

# Run multiple trials to find 10-board solutions
print("Testing 10-board solutions for completeness...")
print("="*70)

valid_10_board_count = 0
invalid_10_board_count = 0

for trial in range(30):
    import random
    random.seed(42 + trial)

    packer = ColumnGenerationPacker(time_limit=60.0, num_patterns=10000)
    solution = packer.solve(problem)

    if solution.num_bins() == 10:
        # Count placed items
        placed_counts = defaultdict(int)
        for bin_packing in solution.bins:
            for placed_item in bin_packing.items:
                placed_counts[placed_item.item.id] += 1

        total_required = sum(item.quantity for item in items)
        total_placed = sum(placed_counts.values())

        is_valid = (total_placed == total_required and solution.is_complete())

        if is_valid:
            valid_10_board_count += 1
            print(f"Trial {trial+1}: 10 boards ✓ VALID - All {total_placed} items placed")
        else:
            invalid_10_board_count += 1
            print(f"Trial {trial+1}: 10 boards ✗ INVALID - Only {total_placed}/{total_required} items")

            # Show which items are missing
            for item in items:
                required = item.quantity
                placed = placed_counts.get(item.id, 0)
                if placed != required:
                    print(f"  {item.id}: required={required}, placed={placed}")

print("\n" + "="*70)
print(f"Valid 10-board solutions found: {valid_10_board_count}")
print(f"Invalid 10-board solutions found: {invalid_10_board_count}")

if valid_10_board_count > 0:
    print("\n✓ SUCCESS: Algorithm CAN produce valid 10-board solutions!")
else:
    print("\n✗ WARNING: No valid 10-board solutions found in 30 trials")
print("="*70)
