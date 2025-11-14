"""
Test Original Chinese Furniture Factory Algorithm

Tests the algorithm that optimizes for minimum cutting PATTERNS (开板图),
not minimum boards. This is the key difference from Western bin packing.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.original_algorithm import OriginalAlgorithm
import time

print("="*70)
print(" ORIGINAL CHINESE FURNITURE FACTORY ALGORITHM TEST")
print("="*70)
print()

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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=300.0)

print(f"Test Data: manual1.xlsx")
print(f"  Items: {len(items)} types, {sum(item.quantity for item in items)} total pieces")
print(f"  Board: {bins[0].width}×{bins[0].height}mm")
print()

# Calculate theoretical values
total_area = sum(item.area() * item.quantity for item in items)
board_area = bins[0].area()
theoretical_min = total_area / board_area

print(f"Theoretical Analysis:")
print(f"  Total item area: {total_area:,.0f} mm²")
print(f"  Board area: {board_area:,.0f} mm²")
print(f"  Theoretical minimum (no waste): {theoretical_min:.2f} boards")
print()

print("Algorithm: Original Chinese Furniture Factory (原始开板算法)")
print("  Optimization Goal: Minimize cutting PATTERNS (开板图), not boards!")
print("  Strategy:")
print("  1. 串排长度 - Horizontal arrangement by width groups (long to short)")
print("  2. 并排宽度 - Vertical stacking of rows (wide to narrow)")
print("  3. 叠放 - Pattern reuse for multiple boards")
print("  Key: Same cutting pattern can be used for many boards!")
print()

# Test original algorithm
packer = OriginalAlgorithm(time_limit=300.0)

start = time.time()
solution = packer.solve(problem)
elapsed = time.time() - start

boards = len(solution.bins)
num_patterns = solution.metadata.get("num_patterns", 0)
utils = [bp.utilization() for bp in solution.bins]
avg_util = sum(utils) / len(utils) if utils else 0
items_placed = sum(len(bp.items) for bp in solution.bins)
items_required = sum(item.quantity for item in items)

print()
print(f"{'='*70}")
print(" RESULTS")
print(f"{'='*70}")
print(f"Cutting Patterns (开板图): {num_patterns}")
print(f"Total Boards: {boards}")
print(f"Pattern Reuse Factor: {boards / num_patterns if num_patterns > 0 else 0:.1f}x")
print(f"Average Utilization: {avg_util:.2%}")
print(f"Items Placed: {items_placed}/{items_required}")
print(f"Valid: {'✓' if items_placed == items_required else '✗'}")
print(f"Time: {elapsed:.2f}s")
print()

if items_placed == items_required:
    print("Per-board details:")
    for i, bp in enumerate(solution.bins, 1):
        rotated_count = sum(1 for pi in bp.items if pi.rotated)
        print(f"  Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items, {rotated_count} rotated)")

    print()
    print("Board utilization distribution:")
    print(f"  Min: {min(utils):.2%}")
    print(f"  Max: {max(utils):.2%}")
    print(f"  Avg: {avg_util:.2%}")
    print(f"  Range: {max(utils) - min(utils):.2%}")
    print()

    # Check pattern efficiency
    if num_patterns <= 3:
        print("="*70)
        print(f" ★★★ EXCELLENT: {num_patterns} CUTTING PATTERNS! ★★★")
        print("="*70)
        print()
        print("This matches the target of 2-3 cutting patterns!")
        print(f"Production efficiency: Each pattern used {boards / num_patterns:.1f}x on average")
        print("This maximizes production efficiency through pattern reuse (叠放).")
    elif num_patterns <= 5:
        print(f"Result: {num_patterns} cutting patterns (target was 2-3)")
        print(f"Pattern reuse: {boards / num_patterns:.1f}x average")
        print("Good pattern consolidation, but could be optimized further.")
    else:
        print(f"Result: {num_patterns} cutting patterns")
        print(f"This is higher than the target of 2-3 patterns.")
        print("May need re-optimization to consolidate patterns.")
else:
    print(f"⚠️  Warning: Did not place all items ({items_placed}/{items_required})")

print()
print("="*70)
print(" COMPARISON WITH OTHER ALGORITHMS")
print("="*70)
print()
print("Results comparison:")
print("  Strip Packing: 12 boards @ 78.96%")
print("  Guillotine: 11 boards @ 85.81%")
print("  Column Generation: 11-12 boards @ 78-86%")
print(f"  Original Algorithm: {boards} boards @ {avg_util:.2%} using {num_patterns} patterns")
print()
print("NOTE: Original algorithm optimizes for PATTERNS, not boards!")
print("      Fewer patterns = fewer machine setups = higher efficiency")
print()
print("="*70)
print("TEST COMPLETE")
print("="*70)
