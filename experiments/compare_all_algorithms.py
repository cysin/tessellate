"""
Compare All Algorithms

Tests and compares:
1. Strip Packing (Simple row-by-row)
2. Guillotine Packing (Recursive subdivision)
3. Column Generation (Pattern-based MIP)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.strip_packing import StripPackingAlgorithm
from tessellate.algorithms.guillotine import GuillotinePacker
from tessellate.algorithms.column_generation import ColumnGenerationPacker
import time

print("="*80)
print(" ALGORITHM COMPARISON: Strip vs Guillotine vs Column Generation")
print("="*80)
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

kerf = 3.0
print(f"Test Data: manual1.xlsx")
print(f"  Items: {len(items)} types")
print(f"  Total pieces: {sum(item.quantity for item in items)}")
print(f"  Board size: {bins[0].width}×{bins[0].height}mm")
print(f"  Kerf: {kerf}mm")
print()

# Calculate theoretical minimum
total_area = sum(item.area() * item.quantity for item in items)
board_area = bins[0].area()
theoretical_min = total_area / board_area

print(f"Theoretical minimum (no waste): {theoretical_min:.2f} boards")
print()

results = []

# ============================================================================
# Test 1: Strip Packing
# ============================================================================

print("="*80)
print(" TEST 1: STRIP PACKING (Row-by-row)")
print("="*80)
print()

problem1 = Problem(items=items, bins=bins, kerf=kerf, time_limit=60.0)
packer1 = StripPackingAlgorithm(time_limit=60.0, max_trials=100)

start = time.time()
solution1 = packer1.solve(problem1)
time1 = time.time() - start

boards1 = len(solution1.bins)
utils1 = [bp.utilization() for bp in solution1.bins]
avg_util1 = sum(utils1) / len(utils1) if utils1 else 0
items1 = sum(len(bp.items) for bp in solution1.bins)
required = sum(item.quantity for item in items)

print()
print(f"Results:")
print(f"  Boards: {boards1}")
print(f"  Avg Utilization: {avg_util1:.2%}")
print(f"  Items: {items1}/{required}")
print(f"  Valid: {'✓' if items1 == required else '✗'}")
print(f"  Time: {time1:.2f}s")

results.append({
    'name': 'Strip Packing',
    'boards': boards1,
    'util': avg_util1,
    'time': time1,
    'valid': items1 == required
})

print()

# ============================================================================
# Test 2: Guillotine Packing
# ============================================================================

print("="*80)
print(" TEST 2: GUILLOTINE PACKING (Recursive subdivision)")
print("="*80)
print()

problem2 = Problem(items=items, bins=bins, kerf=kerf, time_limit=60.0)
packer2 = GuillotinePacker(time_limit=60.0)

start = time.time()
solution2 = packer2.solve(problem2)
time2 = time.time() - start

boards2 = len(solution2.bins)
utils2 = [bp.utilization() for bp in solution2.bins]
avg_util2 = sum(utils2) / len(utils2) if utils2 else 0
items2 = sum(len(bp.items) for bp in solution2.bins)

print()
print(f"Results:")
print(f"  Boards: {boards2}")
print(f"  Avg Utilization: {avg_util2:.2%}")
print(f"  Items: {items2}/{required}")
print(f"  Valid: {'✓' if items2 == required else '✗'}")
print(f"  Time: {time2:.2f}s")

results.append({
    'name': 'Guillotine',
    'boards': boards2,
    'util': avg_util2,
    'time': time2,
    'valid': items2 == required
})

print()

# ============================================================================
# Test 3: Column Generation
# ============================================================================

print("="*80)
print(" TEST 3: COLUMN GENERATION (Pattern-based MIP)")
print("="*80)
print()

problem3 = Problem(items=items, bins=bins, kerf=kerf, time_limit=120.0)
packer3 = ColumnGenerationPacker(time_limit=120.0, num_patterns=10000)

start = time.time()
solution3 = packer3.solve(problem3)
time3 = time.time() - start

boards3 = len(solution3.bins)
utils3 = [bp.utilization() for bp in solution3.bins]
avg_util3 = sum(utils3) / len(utils3) if utils3 else 0
items3 = sum(len(bp.items) for bp in solution3.bins)

print()
print(f"Results:")
print(f"  Boards: {boards3}")
print(f"  Avg Utilization: {avg_util3:.2%}")
print(f"  Items: {items3}/{required}")
print(f"  Valid: {'✓' if items3 == required else '✗'}")
print(f"  Time: {time3:.2f}s")

results.append({
    'name': 'Column Generation',
    'boards': boards3,
    'util': avg_util3,
    'time': time3,
    'valid': items3 == required
})

print()

# ============================================================================
# Comparison Summary
# ============================================================================

print("="*80)
print(" COMPARISON SUMMARY")
print("="*80)
print()

# Table header
print(f"{'Algorithm':<25} {'Boards':<10} {'Utilization':<15} {'Time':<10} {'Valid':<10}")
print("-" * 80)

for r in results:
    print(f"{r['name']:<25} {r['boards']:<10} {r['util']:<14.2%} {r['time']:<9.2f}s {'✓' if r['valid'] else '✗':<10}")

print()

# Find best
valid_results = [r for r in results if r['valid']]
if valid_results:
    best_boards = min(r['boards'] for r in valid_results)
    best_util = max(r['util'] for r in valid_results)
    fastest = min(r['time'] for r in valid_results)

    print("Best results:")
    for r in valid_results:
        if r['boards'] == best_boards:
            print(f"  ✓ Fewest boards: {r['name']} ({r['boards']} boards)")
        if r['util'] == best_util:
            print(f"  ✓ Best utilization: {r['name']} ({r['util']:.2%})")
        if r['time'] == fastest:
            print(f"  ✓ Fastest: {r['name']} ({r['time']:.2f}s)")

print()
print("="*80)
print(" ALGORITHM CHARACTERISTICS")
print("="*80)
print()

print("Strip Packing:")
print("  • Simple row-by-row arrangement")
print("  • Fast and deterministic")
print("  • Best for similar-height items")
print("  • Good for quick solutions")
print()

print("Guillotine Packing:")
print("  • Recursive subdivision (binary tree)")
print("  • Multiple split rules")
print("  • Good general-purpose performance")
print("  • Moderate complexity")
print()

print("Column Generation:")
print("  • Pattern-based optimization")
print("  • MIP solver (exact optimization)")
print("  • Best utilization")
print("  • Slower but most optimal")
print()

print("="*80)
print("TEST COMPLETE")
print("="*80)
