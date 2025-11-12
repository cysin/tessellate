"""
Feasibility analysis: What's the highest utilization patterns we can generate?
And what's the theoretical minimum boards with those patterns?
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker
import random

random.seed(42)

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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=600.0)

print("="*70)
print(" FEASIBILITY ANALYSIS")
print("="*70)

# Calculate theoretical values
total_item_area = sum(item.area() * item.quantity for item in items)
board_area = bins[0].area()

print(f"\nTheoretical analysis:")
print(f"  Total item area: {total_item_area:,.0f} mm²")
print(f"  Board area: {board_area:,.0f} mm²")
print(f"  Theoretical minimum (no waste): {total_item_area / board_area:.2f} boards")
print(f"")
print(f"  10 boards = {board_area * 10:,.0f} mm²")
print(f"  Required avg utilization: {(total_item_area / (board_area * 10)) * 100:.2f}%")
print(f"")
print(f"  11 boards = {board_area * 11:,.0f} mm²")
print(f"  Required avg utilization: {(total_item_area / (board_area * 11)) * 100:.2f}%")

# Generate patterns and analyze distribution
print(f"\nGenerating patterns to analyze what's achievable...")
packer = ColumnGenerationPacker(time_limit=600.0, num_patterns=50000)

groups = problem.group_by_material()
(thickness, material), group_items = list(groups.items())[0]

compatible_bins = problem.get_compatible_bins(group_items[0])
bin_type = compatible_bins[0]

import time
start = time.time()
patterns = packer._generate_patterns(group_items, bin_type, problem.kerf, start)

print(f"\nGenerated {len(patterns)} patterns")

# Analyze utilization distribution
utils = [p.utilization for p in patterns]
utils.sort(reverse=True)

print(f"\nUtilization distribution:")
print(f"  Top 10 patterns: {[f'{u:.1%}' for u in utils[:10]]}")
print(f"  Max: {max(utils):.2%}")
print(f"  Top 100 avg: {sum(utils[:100])/100:.2%}")
print(f"  Top 500 avg: {sum(utils[:500])/500:.2%}")
print(f"  Median: {utils[len(utils)//2]:.2%}")

# Count patterns by utilization thresholds
thresholds = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60]
for threshold in thresholds:
    count = sum(1 for u in utils if u >= threshold)
    print(f"  >= {threshold:.0%}: {count} patterns")

# Try MIP with different utilization thresholds
import highspy
from collections import defaultdict

print(f"\n{'='*70}")
print(" TESTING MIP WITH DIFFERENT UTILIZATION FILTERS")
print(f"{'='*70}")

for min_util in [0.90, 0.85, 0.80, 0.75, 0.70]:
    good_patterns = [p for p in patterns if p.utilization >= min_util]

    if len(good_patterns) < 10:
        print(f"\nMin util {min_util:.0%}: Only {len(good_patterns)} patterns, skipping")
        continue

    print(f"\nMin util >= {min_util:.0%}: {len(good_patterns)} patterns")

    # Build MIP
    h = highspy.Highs()
    h.setOptionValue("log_to_console", False)
    h.setOptionValue("mip_rel_gap", 0.0)
    h.setOptionValue("time_limit", 120.0)

    num_patterns = len(good_patterns)

    # Objective: minimize boards
    obj_coeffs = [1.0] * num_patterns

    # Variables
    col_lower = [0.0] * num_patterns
    col_upper = [100.0] * num_patterns

    h.addVars(num_patterns, col_lower, col_upper)

    # Set integrality
    for i in range(num_patterns):
        h.changeColIntegrality(i, highspy.HighsVarType.kInteger)

    h.changeColsCost(0, num_patterns - 1, obj_coeffs)

    # Constraints: cover all items
    constraint_matrix = []
    row_lower = []
    row_upper = []

    for item in group_items:
        coeffs = []
        for pattern in good_patterns:
            count = pattern.get_item_count(item.id)
            coeffs.append(float(count))

        constraint_matrix.append(coeffs)
        row_lower.append(float(item.quantity))
        row_upper.append(float(item.quantity))

    for i, coeffs in enumerate(constraint_matrix):
        h.addRow(row_lower[i], row_upper[i], len(coeffs),
                list(range(num_patterns)), coeffs)

    # Solve
    h.run()

    model_status = h.getModelStatus()

    if model_status == highspy.HighsModelStatus.kOptimal:
        solution = h.getSolution()
        col_values = solution.col_value

        num_boards = sum(int(round(v)) for v in col_values)

        # Calculate average utilization of selected patterns
        selected_utils = []
        for i, val in enumerate(col_values):
            count = int(round(val))
            if count > 0:
                selected_utils.extend([good_patterns[i].utilization] * count)

        avg_util = sum(selected_utils) / len(selected_utils) if selected_utils else 0

        print(f"  Result: {num_boards} boards @ {avg_util:.2%} avg utilization")
    else:
        print(f"  Result: {model_status}")

print(f"\n{'='*70}")
