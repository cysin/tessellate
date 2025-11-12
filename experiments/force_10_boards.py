"""
TWO-STAGE OPTIMIZATION: Force 10 boards and maximize utilization

Stage 1: Generate many high-quality patterns
Stage 2: Solve MIP with constraint: EXACTLY 10 boards, maximize total area

This directly targets the user's goal: 10 boards with maximum utilization
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin, BinPacking, PlacedItem
from tessellate.algorithms.column_generation import ColumnGenerationPacker
from collections import defaultdict
import highspy
import time
import random

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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=3600.0)

print("="*70)
print(" TWO-STAGE OPTIMIZATION: FORCE 10 BOARDS + MAXIMIZE UTILIZATION")
print("="*70)
print("\nStrategy:")
print("  1. Generate 20,000+ diverse patterns")
print("  2. Solve MIP with FIXED constraint: exactly 10 boards")
print("  3. Objective: MAXIMIZE total item area (minimize waste)")
print()

# Run multiple trials with different random seeds
best_solution = None
best_util = 0
num_trials = 50

for trial in range(num_trials):
    random.seed(None)  # True randomness
    print(f"\n{'='*70}")
    print(f"TRIAL {trial+1}/{num_trials}")
    print(f"{'='*70}")

    # Stage 1: Generate patterns
    print("\nStage 1: Generating patterns...")
    start = time.time()

    packer = ColumnGenerationPacker(time_limit=600.0, num_patterns=50000)

    # Get the material group
    groups = problem.group_by_material()
    (thickness, material), group_items = list(groups.items())[0]

    compatible_bins = problem.get_compatible_bins(group_items[0])
    bin_type = compatible_bins[0]

    # Generate patterns
    patterns = packer._generate_patterns(group_items, bin_type, problem.kerf, start)

    # Filter to good patterns
    min_util = 0.60  # Slightly higher threshold for quality
    good_patterns = [p for p in patterns if p.utilization >= min_util]

    print(f"  Generated {len(patterns)} total patterns")
    print(f"  Kept {len(good_patterns)} patterns (util >= {min_util:.0%})")

    if len(good_patterns) < 10:
        print("  Not enough patterns, skipping this trial")
        continue

    # Stage 2: Solve MIP with EXACTLY 10 boards
    print(f"\nStage 2: Solving MIP for EXACTLY 10 boards...")

    h = highspy.Highs()
    h.setOptionValue("log_to_console", False)
    h.setOptionValue("mip_rel_gap", 0.0)
    h.setOptionValue("time_limit", 600.0)  # 10 minutes

    num_patterns = len(good_patterns)

    # Objective: MAXIMIZE total area (negative cost for maximization)
    obj_coeffs = [-p.total_area for p in good_patterns]

    # Variables: how many times to use each pattern
    col_lower = [0.0] * num_patterns
    col_upper = [10.0] * num_patterns  # Max 10 of any pattern

    # Build model
    h.addVars(num_patterns, col_lower, col_upper)

    # Set integrality
    for i in range(num_patterns):
        h.changeColIntegrality(i, highspy.HighsVarType.kInteger)

    h.changeColsCost(0, num_patterns - 1, obj_coeffs)

    # Constraints
    constraint_matrix = []
    row_lower = []
    row_upper = []

    # Constraint 1: Each item must be covered AT LEAST (allow slight overproduction if needed)
    for item in group_items:
        coeffs = []
        for pattern in good_patterns:
            count = pattern.get_item_count(item.id)
            coeffs.append(float(count))

        constraint_matrix.append(coeffs)
        row_lower.append(float(item.quantity))  # At least this many
        row_upper.append(float(item.quantity + 2))  # Allow up to 2 extra

    # Constraint 2: EXACTLY 10 boards
    coeffs = [1.0] * num_patterns
    constraint_matrix.append(coeffs)
    row_lower.append(10.0)  # Exactly 10
    row_upper.append(10.0)  # Exactly 10

    # Add all constraints
    for i, coeffs in enumerate(constraint_matrix):
        h.addRow(row_lower[i], row_upper[i], len(coeffs),
                list(range(num_patterns)), coeffs)

    # Solve
    print("  Running MIP solver...")
    solve_start = time.time()
    h.run()
    solve_time = time.time() - solve_start

    model_status = h.getModelStatus()
    print(f"  MIP status: {model_status} ({solve_time:.1f}s)")

    if model_status == highspy.HighsModelStatus.kOptimal or model_status == highspy.HighsModelStatus.kTimeLimit:
        solution_obj = h.getSolution()
        col_values = solution_obj.col_value

        # Extract solution
        selected_patterns = []
        for i, val in enumerate(col_values):
            count = int(round(val))
            if count > 0:
                for _ in range(count):
                    selected_patterns.append(i)

        print(f"  Selected {len(selected_patterns)} patterns")

        # Build solution
        solution_bins = []
        item_coverage = defaultdict(int)

        for p_idx in selected_patterns:
            pattern = good_patterns[p_idx]
            bin_packing = BinPacking(
                bin_id=len(solution_bins),
                bin_type=pattern.bin_type,
                items=pattern.items.copy()
            )
            solution_bins.append(bin_packing)

            # Track coverage
            for pi in pattern.items:
                item_coverage[pi.item.id] += 1

        # Validate
        is_valid = True
        for item in group_items:
            if item_coverage[item.id] < item.quantity:
                is_valid = False
                print(f"  ✗ Missing items: {item.id} has {item_coverage[item.id]}/{item.quantity}")

        if is_valid and len(solution_bins) == 10:
            # Calculate utilization
            total_util = sum(bp.utilization() for bp in solution_bins) / len(solution_bins)

            print(f"\n  ✓ VALID 10-board solution!")
            print(f"    Utilization: {total_util:.2%}")

            if total_util > best_util:
                best_util = total_util
                best_solution = solution_bins
                print(f"    ⭐ NEW BEST!")

                if total_util > 0.90:
                    print(f"\n🎯🎯🎯 TARGET ACHIEVED! 10 boards @ {total_util:.2%}! 🎯🎯🎯")
                    break
        else:
            if len(solution_bins) != 10:
                print(f"  ✗ Got {len(solution_bins)} boards instead of 10")
            if not is_valid:
                print(f"  ✗ Invalid solution")

    else:
        print(f"  ✗ MIP failed: {model_status}")

print("\n" + "="*70)
print(" FINAL RESULT")
print("="*70)

if best_solution:
    print(f"\nBest 10-board solution:")
    print(f"  Boards: 10")
    print(f"  Utilization: {best_util:.2%}")

    print(f"\n  Per-board utilization:")
    for i, bp in enumerate(best_solution, 1):
        print(f"    Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

    if best_util >= 0.90:
        print(f"\n  ✅ SUCCESS! Achieved 10 boards @ {best_util:.2%} (target: >90%)")
    else:
        print(f"\n  Best achieved: {best_util:.2%} (target: >90%)")
else:
    print("\n✗ No valid 10-board solution found")
    print("  The problem might be infeasible with exactly 10 boards")

print("="*70)
