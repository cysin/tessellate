"""
ULTRA-AGGRESSIVE PATTERN SEARCH

This script explores the absolute deepest, widest, and longest search possible.
Time estimate: 24-72 hours per trial
Resource usage: High memory and CPU

Parameters maximized:
- 1,000,000 patterns per trial
- Extended MIP time (2 hours)
- Very low utilization filter (40%)
- Massive rotated pattern generation
- 100 independent trials
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=14400.0)  # 4 hour time limit

print("="*70)
print(" ULTRA-AGGRESSIVE SEARCH")
print("="*70)
print()
print("Configuration:")
print("  Patterns per trial: 1,000,000")
print("  MIP time limit: 7,200 seconds (2 hours)")
print("  Utilization filter: ≥40%")
print("  Number of trials: 100")
print("  Estimated total time: 24-72 hours")
print()

# Import the modified packer
import sys
sys.path.insert(0, '/home/user/tessellate')

from tessellate.algorithms.column_generation_ultra import ColumnGenerationPackerUltra

best_solution = None
best_boards = float('inf')
best_util = 0.0

results = []

for trial in range(1, 101):
    print(f"\n{'='*70}")
    print(f"TRIAL {trial}/100")
    print(f"{'='*70}")

    trial_start = time.time()

    # Create ultra-aggressive packer
    packer = ColumnGenerationPackerUltra(
        time_limit=14400.0,  # 4 hours per trial
        num_patterns=1_000_000,  # 1 million patterns
        min_utilization=0.40,  # Very permissive
        mip_time_limit=7200.0,  # 2 hours for MIP
        rotated_trials=1000,  # Massive rotated pattern generation
        random_permutations=1000,  # Many random attempts
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
    print(f"  Time: {trial_time:.1f}s")

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
                print(f"  Time: {sum(r['time'] for r in results):.1f}s total")

                # Print board details
                for i, bp in enumerate(best_solution.bins, 1):
                    print(f"    Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

                print(f"\n  Continuing to search for even better solutions...")

print(f"\n{'='*70}")
print(" FINAL RESULTS")
print(f"{'='*70}")

# Count distribution
from collections import Counter
board_counts = Counter(r['boards'] for r in results if r['valid'])

print(f"\nDistribution of solutions:")
for boards, count in sorted(board_counts.items()):
    print(f"  {boards} boards: {count} trials")

if best_solution:
    print(f"\nBest solution found:")
    print(f"  Boards: {best_boards}")
    print(f"  Avg utilization: {best_util:.2%}")
    print(f"\n  Board details:")
    for i, bp in enumerate(best_solution.bins, 1):
        print(f"    Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")
else:
    print(f"\n✗ No valid solution found")

total_time = sum(r['time'] for r in results)
print(f"\nTotal runtime: {total_time:.1f}s ({total_time/3600:.2f} hours)")
print(f"Average per trial: {total_time/len(results):.1f}s")

print(f"\n{'='*70}")
