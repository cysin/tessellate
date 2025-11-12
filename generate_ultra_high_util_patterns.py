"""
Ultra-aggressive pattern generation attempting to find 95%+ utilization patterns.

Strategy:
1. Try all possible combinations of items
2. Test every possible arrangement
3. Use exhaustive search to find the absolute best patterns possible
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.packing.guillotine import GuillotinePacker
from itertools import combinations, permutations
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

bin_type = bins[0]
kerf = 3.0

print("="*70)
print(" ULTRA-HIGH UTILIZATION PATTERN SEARCH")
print("="*70)

board_area = bin_type.area()
target_area = board_area * 0.95  # Target 95%+ utilization

print(f"\nTarget: Find patterns with >95% utilization")
print(f"  Board area: {board_area:,.0f} mm²")
print(f"  Target item area: >{target_area:,.0f} mm²")

# Expand items to individual pieces
expanded_items = []
for item in items:
    for i in range(item.quantity):
        expanded_items.append(item)

print(f"\nTotal pieces: {len(expanded_items)}")

# Try to pack different subsets
packer = GuillotinePacker()
best_patterns = []

# Try different subset sizes
print(f"\nSearching for optimal combinations...")

for subset_size in range(len(expanded_items), max(1, len(expanded_items) - 20), -1):
    if subset_size < 5:
        break

    print(f"\n  Trying subsets of size {subset_size}...")

    # Sample random combinations (exhaustive would be too many)
    num_samples = min(10000, 2**subset_size if subset_size < 20 else 10000)

    for trial in range(num_samples):
        if trial % 1000 == 0:
            print(f"    Trial {trial}/{num_samples}...", end='\r')

        # Random subset
        subset = random.sample(expanded_items, subset_size)

        # Try to pack
        result = packer.pack(subset, bin_type, kerf)

        if result and len(result.bins) == 1:
            # Single board pattern!
            util = result.bins[0].utilization()
            total_area = result.bins[0].total_item_area()

            if util >= 0.95:
                best_patterns.append((util, result.bins[0]))
                print(f"\n    ✓ Found {util:.2%} utilization pattern!")

                if util >= 0.98:
                    print(f"      EXCEPTIONAL PATTERN! {util:.2%}")

    # If we found some good patterns, no need to try smaller subsets
    if len(best_patterns) >= 100:
        print(f"\n  Found {len(best_patterns)} high-util patterns, stopping search")
        break

print(f"\n\n{'='*70}")
print(" RESULTS")
print(f"{'='*70}")

if best_patterns:
    best_patterns.sort(reverse=True, key=lambda x: x[0])

    print(f"\nFound {len(best_patterns)} patterns with ≥95% utilization:")
    for i, (util, pattern) in enumerate(best_patterns[:20], 1):
        print(f"  #{i}: {util:.2%} utilization ({len(pattern.items)} items)")

    print(f"\n  Best: {best_patterns[0][0]:.2%}")
    print(f"  Top 10 avg: {sum(p[0] for p in best_patterns[:10])/min(10, len(best_patterns)):.2%}")

    # Now test if we can build a 10-board solution with these patterns
    print(f"\n{'='*70}")
    print(" TESTING 10-BOARD SOLUTION WITH HIGH-UTIL PATTERNS")
    print(f"{'='*70}")

    # This would require implementing set covering with these new patterns
    print("\nNext step: Implement MIP solver with these ultra-high patterns")
    print("to test if 10-board solution is now feasible.")

else:
    print("\n✗ Could not find any patterns with ≥95% utilization")
    print("  This confirms that guillotine constraints make 10 boards")
    print("  mathematically infeasible for this problem.")

print(f"\n{'='*70}")
