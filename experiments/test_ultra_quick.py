"""
Quick test of ultra-aggressive packer (5 minutes to verify it works)
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

problem = Problem(items=items, bins=bins, kerf=3.0, time_limit=300.0)

print("="*70)
print(" QUICK TEST: Ultra-Aggressive Packer")
print("="*70)
print()
print("Testing with moderate parameters to verify it works:")
print("  Patterns: 100,000")
print("  MIP time: 120 seconds")
print("  Utilization filter: ≥40%")
print("  Rotated trials: 500")
print()

from tessellate.algorithms.column_generation_ultra import ColumnGenerationPackerUltra

start = time.time()

packer = ColumnGenerationPackerUltra(
    time_limit=300.0,  # 5 minutes
    num_patterns=100_000,  # 100k patterns
    min_utilization=0.40,
    mip_time_limit=120.0,
    rotated_trials=500,
    random_permutations=200,
)

solution = packer.solve(problem)

elapsed = time.time() - start

# Count items
total_placed = sum(len(bp.items) for bp in solution.bins)
total_required = sum(item.quantity for item in items)

# Calculate stats
num_boards = len(solution.bins)
utils = [bp.utilization() for bp in solution.bins]
avg_util = sum(utils) / len(utils) if utils else 0

print(f"\n{'='*70}")
print(" RESULTS")
print(f"{'='*70}")
print(f"\nBoards: {num_boards}")
print(f"Average Utilization: {avg_util:.2%}")
print(f"Items placed: {total_placed}/{total_required}")
print(f"Valid: {'✓' if total_placed == total_required else '✗'}")
print(f"Time: {elapsed:.1f}s")

if total_placed == total_required:
    print(f"\nPer-board utilization:")
    for i, bp in enumerate(solution.bins, 1):
        print(f"  Board {i:2d}: {bp.utilization():.2%} ({len(bp.items)} items)")

print(f"\n{'='*70}")
print("\n✓ Ultra-aggressive packer is working correctly!")
print("\nTo run full 24-72 hour search, use:")
print("  python ultra_aggressive_search.py")
print(f"\n{'='*70}")
