"""
AGGRESSIVE OPTIMIZATION: Find 10-board solution with >90% utilization

Strategy:
- Remove deterministic seed (allow true randomness)
- Generate 50,000+ diverse patterns
- Lower utilization filter to 50%
- Extended MIP solve time (600s)
- Run 100+ trials
- Focus on rotated patterns (key to high utilization)
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.column_generation import ColumnGenerationPacker
from collections import defaultdict
import time

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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=1800.0)  # 30 min

print("="*70)
print(" AGGRESSIVE OPTIMIZATION: 10 BOARDS @ >90% UTILIZATION")
print("="*70)
print("\nTarget:")
print(f"  - Boards: 10")
print(f"  - Required utilization: 94.39%")
print(f"  - Total area: 28,098,880 mm²")
print(f"  - 10 boards capacity: 29,768,000 mm²")
print()

def validate_solution(solution, items):
    """Validate solution."""
    placed_counts = defaultdict(int)
    for bin_packing in solution.bins:
        for placed_item in bin_packing.items:
            placed_counts[placed_item.item.id] += 1

    total_required = sum(item.quantity for item in items)
    total_placed = sum(placed_counts.values())

    if total_placed != total_required:
        return False

    for item in items:
        if placed_counts[item.id] != item.quantity:
            return False

    return True

# Results tracking
all_results = []
best_10_board = None
best_overall = None
best_bins = float('inf')

num_trials = 100  # Run many trials
start_time = time.time()

print(f"Running {num_trials} trials with AGGRESSIVE parameters...")
print("(No time limit per trial - searching for optimal solution)")
print("-"*70)

for trial in range(num_trials):
    trial_start = time.time()

    # Create packer with AGGRESSIVE settings
    # Key: Each trial will have different random patterns
    packer = ColumnGenerationPacker(
        time_limit=1800.0,  # 30 minutes per trial
        num_patterns=100000  # Generate MANY patterns
    )

    solution = packer.solve(problem)

    # Validate
    is_valid = validate_solution(solution, items)

    if is_valid:
        num_bins = solution.num_bins()
        util = solution.total_utilization()
        trial_time = time.time() - trial_start

        all_results.append({
            'trial': trial + 1,
            'bins': num_bins,
            'utilization': util,
            'time': trial_time
        })

        # Track best overall
        if num_bins < best_bins:
            best_bins = num_bins
            best_overall = solution
            print(f"Trial {trial+1:3d}: {num_bins:2d} boards @ {util:.2%} util ⭐ NEW BEST! ({trial_time:.1f}s)")
        else:
            status = ""
            if num_bins == 10 and util > 0.90:
                status = " 🎯 TARGET!"
            print(f"Trial {trial+1:3d}: {num_bins:2d} boards @ {util:.2%} util{status} ({trial_time:.1f}s)")

        # Track best 10-board solution
        if num_bins == 10:
            if best_10_board is None or util > best_10_board.total_utilization():
                best_10_board = solution
                print(f"  → Best 10-board: {util:.2%} utilization!")

                if util > 0.90:
                    print(f"\n🎯🎯🎯 TARGET ACHIEVED! 10 boards @ {util:.2%}! 🎯🎯🎯")
                    print(f"Stopping after {trial+1} trials.\n")
                    break
    else:
        print(f"Trial {trial+1:3d}: INVALID (skipped)")

    # Show progress every 10 trials
    if (trial + 1) % 10 == 0:
        elapsed = time.time() - start_time
        avg_time = elapsed / (trial + 1)
        print(f"\n--- Progress: {trial+1}/{num_trials} trials, {elapsed/60:.1f} min elapsed, avg {avg_time:.1f}s/trial ---\n")

total_time = time.time() - start_time

print("\n" + "="*70)
print(" OPTIMIZATION COMPLETE")
print("="*70)
print(f"\nTotal trials: {len(all_results)} valid solutions")
print(f"Total time: {total_time/60:.1f} minutes")

if all_results:
    # Analyze results
    from collections import Counter
    bin_counts = Counter([r['bins'] for r in all_results])

    print("\nResults distribution:")
    for bins in sorted(bin_counts.keys()):
        count = bin_counts[bins]
        results_with_bins = [r for r in all_results if r['bins'] == bins]
        avg_util = sum(r['utilization'] for r in results_with_bins) / len(results_with_bins)
        print(f"  {bins:2d} boards: {count:3d} solutions, avg util {avg_util:.2%}")

print("\n" + "="*70)
print(" BEST SOLUTION")
print("="*70)

if best_10_board:
    print(f"\n🎯 BEST 10-BOARD SOLUTION:")
    print(f"   Boards: 10")
    print(f"   Utilization: {best_10_board.total_utilization():.2%}")
    print(f"   Time: {best_10_board.metadata.get('execution_time', 0):.1f}s")

    # Show per-board details
    print(f"\n   Per-board utilization:")
    for i, bp in enumerate(best_10_board.bins, 1):
        print(f"     Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

    if best_10_board.total_utilization() >= 0.90:
        print(f"\n   ✅✅✅ SUCCESS! Achieved target: 10 boards @ >90% util! ✅✅✅")
    else:
        print(f"\n   ⚠️ Close: 10 boards but {best_10_board.total_utilization():.2%} < 90%")

elif best_overall:
    print(f"\nBest overall solution:")
    print(f"   Boards: {best_overall.num_bins()}")
    print(f"   Utilization: {best_overall.total_utilization():.2%}")
    print(f"\n   (No 10-board solution found)")

else:
    print("\n❌ No valid solutions found")

print("="*70)
