"""
Debug: Why is the MIP solution failing validation?
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker
from collections import defaultdict
import random
import highspy

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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=60.0)

print("="*70)
print(" MIP FORMULATION DEBUG")
print("="*70)

# Generate patterns manually
packer = ColumnGenerationPacker(time_limit=60.0, num_patterns=10000)

# We need to intercept at the pattern generation stage
# Let's manually call the internal methods
print("\nGenerating patterns...")
groups = problem.group_by_material()

for (thickness, material), group_items in groups.items():
    print(f"\nMaterial group: {material} {thickness}mm")
    print(f"Items: {len(group_items)}, pieces: {sum(i.quantity for i in group_items)}")

    compatible_bins = problem.get_compatible_bins(group_items[0])
    if not compatible_bins:
        continue

    bin_type = compatible_bins[0]

    # Generate patterns
    import time
    start_time = time.time()
    patterns = packer._generate_patterns(group_items, bin_type, problem.kerf, start_time)

    print(f"Generated {len(patterns)} patterns")

    # Filter patterns
    min_util = 0.65
    good_patterns = [i for i, p in enumerate(patterns) if p.utilization >= min_util]
    print(f"Filtered to {len(good_patterns)} patterns (util >= {min_util:.0%})")

    # Build MIP manually with detailed logging
    print("\nBuilding MIP model...")
    h = highspy.Highs()
    h.setOptionValue("log_to_console", True)  # Enable logging
    h.setOptionValue("mip_rel_gap", 0.0)
    h.setOptionValue("time_limit", 120.0)

    num_patterns = len(good_patterns)

    # Objective
    bin_area = patterns[0].bin_type.area()
    obj_coeffs = [10000.0 - patterns[idx].total_area / bin_area for idx in good_patterns]

    # Variables
    col_lower = [0.0] * num_patterns
    col_upper = [100.0] * num_patterns
    var_types = [highspy.HighsVarType.kInteger] * num_patterns

    # Constraints
    print(f"\nConstraint matrix ({len(group_items)} items x {num_patterns} patterns):")
    constraint_matrix = []
    row_lower = []
    row_upper = []

    for item in group_items:
        coeffs = []
        for p_idx in good_patterns:
            pattern = patterns[p_idx]
            count = pattern.get_item_count(item.id)
            coeffs.append(float(count))

        constraint_matrix.append(coeffs)
        row_lower.append(float(item.quantity))
        row_upper.append(float(item.quantity))

        # Show constraint details
        print(f"  {item.id}: need exactly {item.quantity}")
        print(f"    Constraint: {sum(coeffs)} total coverage if all patterns used once")

    # Build and solve - match the actual code
    h.addVars(num_patterns, col_lower, col_upper)

    # Set integrality for each variable
    for i in range(num_patterns):
        h.changeColIntegrality(i, highspy.HighsVarType.kInteger)

    h.changeColsCost(0, num_patterns - 1, obj_coeffs)

    for i, coeffs in enumerate(constraint_matrix):
        h.addRow(row_lower[i], row_upper[i], len(coeffs),
                list(range(num_patterns)), coeffs)

    print("\nSolving MIP...")
    h.run()

    # Check status
    model_status = h.getModelStatus()
    print(f"\nMIP Status: {model_status}")

    if model_status == highspy.HighsModelStatus.kOptimal:
        print("✓ MIP found optimal solution")

        solution = h.getSolution()
        col_values = solution.col_value

        # Show which patterns were selected
        print("\nSelected patterns (RAW MIP values):")
        selected_patterns = []
        for i, val in enumerate(col_values):
            if val > 0.01:
                p_idx = good_patterns[i]
                print(f"  Pattern {p_idx}: MIP value = {val:.3f}, rounded = {int(round(val))} (util={patterns[p_idx].utilization:.1%})")
                count = int(round(val))
                selected_patterns.extend([p_idx] * count)

        print(f"\nTotal bins: {len(selected_patterns)}")

        # Validate coverage
        print("\nValidating item coverage:")
        item_coverage = defaultdict(int)
        for p_idx in selected_patterns:
            pattern = patterns[p_idx]
            for pi in pattern.items:
                item_coverage[pi.item.id] += 1

        all_valid = True
        for item in group_items:
            required = item.quantity
            placed = item_coverage[item.id]
            status = "✓" if placed == required else f"✗ ({placed}/{required})"
            print(f"  {item.id}: {status}")
            if placed != required:
                all_valid = False

        if all_valid:
            print("\n✅ MIP solution is VALID!")
        else:
            print("\n❌ MIP solution is INVALID!")

    else:
        print(f"✗ MIP failed: {model_status}")
