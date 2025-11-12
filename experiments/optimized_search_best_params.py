"""
Optimized search with BEST PARAMETERS based on analysis.

Key insights:
1. Rotated patterns achieve highest utilization (85-90%)
2. Need balance between pattern quantity and quality
3. MIP needs enough time to find optimal combination

This uses:
- MASSIVE rotated pattern generation (20,000 trials)
- Balanced utilization filter (60%)
- Moderate total patterns to keep MIP tractable (300,000)
- Extended MIP time (2 hours)
- 50 independent trials

Estimated time: 3-6 hours per trial = 150-300 hours total for 50 trials
"""

import sys
import os
# Add parent directory to path so we can import tessellate
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
import time

# Read test data
df = pd.read_excel('../test_data/bench/manual1.xlsx')

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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=21600.0)

print("="*70)
print(" OPTIMIZED SEARCH - BEST PARAMETERS")
print("="*70)
print()
print("Configuration (optimized for highest chance of 10 boards):")
print("  Total patterns: 300,000 (manageable for MIP)")
print("  Rotated trials: 20,000 (MAXIMUM - this is critical)")
print("  Random permutations: 3,000")
print("  Min utilization: 60% (balanced filter)")
print("  MIP time: 7,200s (2 hours)")
print("  Number of trials: 50")
print()
print("Estimated time per trial: 3-6 hours")
print("Total time for 50 trials: 150-300 hours (6-12 days)")
print()
print("Press Ctrl+C to stop at any time. Best solution will be preserved.")
print("="*70)
print()

from tessellate.algorithms.column_generation_ultra import ColumnGenerationPackerUltra

best_solution = None
best_boards = float('inf')
best_util = 0.0
results = []

for trial in range(1, 51):
    print(f"\n{'='*70}")
    print(f"TRIAL {trial}/50")
    print(f"{'='*70}")

    trial_start = time.time()

    # OPTIMIZED PARAMETERS
    packer = ColumnGenerationPackerUltra(
        time_limit=21600.0,  # 6 hours per trial
        num_patterns=300_000,  # 300k patterns (sweet spot)
        min_utilization=0.60,  # Balanced filter (not too permissive)
        mip_time_limit=7200.0,  # 2 hours for MIP
        rotated_trials=20_000,  # MASSIVE rotated generation
        random_permutations=3_000,  # Many random attempts
    )

    solution = packer.solve(problem)

    trial_time = time.time() - trial_start

    # Count items
    total_placed = sum(len(bp.items) for bp in solution.bins)
    total_required = sum(item.quantity for item in items)

    # Calculate stats
    num_boards = len(solution.bins)
    utils = [bp.utilization() for bp in solution.bins]
    avg_util = sum(utils) / len(utils) if utils else 0

    valid = (total_placed == total_required)

    print(f"\nTrial {trial} Result:")
    print(f"  Boards: {num_boards}")
    print(f"  Avg Utilization: {avg_util:.2%}")
    print(f"  Items: {total_placed}/{total_required}")
    print(f"  Valid: {'✓' if valid else '✗'}")
    print(f"  Time: {trial_time/3600:.2f} hours")

    results.append({
        'trial': trial,
        'boards': num_boards,
        'util': avg_util,
        'valid': valid,
        'time': trial_time
    })

    # Track best
    if valid:
        if num_boards < best_boards or (num_boards == best_boards and avg_util > best_util):
            best_boards = num_boards
            best_util = avg_util
            best_solution = solution

            print(f"\n  ★ NEW BEST: {best_boards} boards @ {best_util:.2%}")

            # If we found 10 boards, celebrate!
            if best_boards == 10:
                print(f"\n{'='*70}")
                print("  ★★★ FOUND 10-BOARD SOLUTION! ★★★")
                print(f"{'='*70}")
                print(f"\n  Utilization: {best_util:.2%}")
                print(f"  Trial: {trial}")
                print(f"  Time: {sum(r['time'] for r in results)/3600:.1f} hours total")

                # Print board details
                for i, bp in enumerate(best_solution.bins, 1):
                    print(f"    Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

                print(f"\n  Continuing search for even better solutions...")

    # Progress summary every 5 trials
    if trial % 5 == 0:
        from collections import Counter
        board_counts = Counter(r['boards'] for r in results if r['valid'])
        print(f"\n  Progress after {trial} trials:")
        print(f"    Best so far: {best_boards} boards @ {best_util:.2%}")
        print(f"    Distribution: {dict(sorted(board_counts.items()))}")
        print(f"    Total time: {sum(r['time'] for r in results)/3600:.1f} hours")

print(f"\n{'='*70}")
print(" FINAL RESULTS")
print(f"{'='*70}")

# Count distribution
from collections import Counter
board_counts = Counter(r['boards'] for r in results if r['valid'])

print(f"\nDistribution of solutions:")
for boards, count in sorted(board_counts.items()):
    pct = count / len([r for r in results if r['valid']]) * 100
    print(f"  {boards} boards: {count:2d} trials ({pct:.1f}%)")

if best_solution:
    print(f"\nBest solution found:")
    print(f"  Boards: {best_boards}")
    print(f"  Avg utilization: {best_util:.2%}")

    print(f"\n  Board details:")
    for i, bp in enumerate(best_solution.bins, 1):
        print(f"    Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

    if best_boards == 10:
        print(f"\n  ★★★ SUCCESS: 10-board solution achieved!")
    elif best_boards == 11:
        print(f"\n  ✓ 11-board solution (likely mathematical optimum)")
    else:
        print(f"\n  Result: {best_boards} boards")
else:
    print(f"\n✗ No valid solution found")

total_time = sum(r['time'] for r in results)
print(f"\nTotal runtime: {total_time/3600:.1f} hours ({total_time/86400:.1f} days)")
print(f"Average per trial: {total_time/len(results)/3600:.2f} hours")

print(f"\n{'='*70}")
