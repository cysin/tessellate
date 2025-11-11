#!/usr/bin/env python3
"""
Test the MaxRects BSSF algorithm on benchmark data.
"""

import pandas as pd
import time
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.maxrects_bssf import MaxRectsBSSFAlgorithm

def load_benchmark_data(filepath):
    """Load benchmark data from Excel file."""
    df = pd.read_excel(filepath)

    # Map grain to rotatable
    grain_map = {'mixed': True, 'fixed': False}

    items = []
    for idx, row in df.iterrows():
        grain = str(row['Grain']).lower()
        rotatable = grain_map.get(grain, True)

        item = Item(
            id=row['Code'],
            width=float(row['Width']),
            height=float(row['Height']),
            thickness=float(row['Thickness']),
            material=row['Color'],
            quantity=int(row['Qty']),
            rotatable=rotatable
        )
        items.append(item)

    print(f"Loaded {len(items)} unique items")
    total_qty = sum(item.quantity for item in items)
    print(f"Total pieces: {total_qty}")

    # Calculate total area
    total_area = sum(item.width * item.height * item.quantity for item in items)
    print(f"Total area: {total_area:,.0f} mm²")

    # Standard board: 2440mm x 1220mm
    board_area = 2440 * 1220
    theoretical_min = total_area / board_area
    print(f"Theoretical minimum boards (area only): {theoretical_min:.1f}")

    # Get unique material+thickness combinations
    material_combos = set((item.thickness, item.material) for item in items)
    print(f"Material combinations: {len(material_combos)}")

    bins = []
    for thickness, material in material_combos:
        bin_id = f"Board-{material}-{thickness}mm"
        bins.append(Bin(
            id=bin_id,
            width=2440,
            height=1220,
            thickness=thickness,
            material=material,
            available=-1
        ))

    return items, bins


def test_bssf():
    """Test MaxRects BSSF algorithm."""
    print("="*60)
    print("MaxRects BSSF Algorithm Test")
    print("="*60)

    items, bins = load_benchmark_data('test_data/bench/cutting_plan_data.xlsx')

    problem = Problem(
        items=items,
        bins=bins,
        kerf=3.5,
        utilization_threshold=0.78,
        time_limit=60.0
    )

    algo = MaxRectsBSSFAlgorithm(time_limit=60.0)

    print(f"\nRunning {algo.get_name()}...")
    start = time.time()
    solution = algo.solve(problem)
    elapsed = time.time() - start

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Bins used: {solution.num_bins()}")
    print(f"Utilization: {solution.total_utilization()*100:.1f}%")
    print(f"Execution time: {elapsed:.2f}s")
    print(f"Complete: {solution.is_complete()}")

    if solution.unplaced:
        print(f"\n⚠ Unplaced items: {len(solution.unplaced)}")
        total_unplaced = sum(qty for _, qty in solution.unplaced)
        print(f"  Total unplaced pieces: {total_unplaced}")

    # Show bin utilization distribution
    if solution.bins:
        utils = [bp.utilization() for bp in solution.bins]
        print(f"\nUtilization distribution:")
        print(f"  Min: {min(utils)*100:.1f}%")
        print(f"  Max: {max(utils)*100:.1f}%")
        print(f"  Avg: {sum(utils)/len(utils)*100:.1f}%")

        # Show first few bins
        print(f"\nFirst 10 bins:")
        for i, bp in enumerate(solution.bins[:10]):
            print(f"  Bin {bp.bin_id} ({bp.bin_type.id}): "
                  f"{len(bp.items)} items, {bp.utilization()*100:.1f}% utilized")

    return solution


if __name__ == "__main__":
    solution = test_bssf()
    print("\nDone!")
