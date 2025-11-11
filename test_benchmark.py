#!/usr/bin/env python3
"""
Test the benchmark data from test_data/bench/cutting_plan_data.xlsx
"""

import pandas as pd
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.maxrects import MaximalRectanglesAlgorithm
from tessellate.algorithms.guillotine import GuillotinePacker

def load_benchmark_data(filepath):
    """Load benchmark data from Excel file."""
    df = pd.read_excel(filepath)

    # Map grain to rotatable
    # mixed = rotatable, fixed = not rotatable
    grain_map = {
        'mixed': True,
        'fixed': False
    }

    items = []
    for idx, row in df.iterrows():
        # Use the first Grain column to determine rotatability
        grain = str(row['Grain']).lower()
        rotatable = grain_map.get(grain, True)  # Default to rotatable

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

    # Get unique material+thickness combinations
    material_combos = set((item.thickness, item.material) for item in items)
    print(f"Material combinations: {material_combos}")

    # Standard board size: 2440mm x 1220mm (common plywood/MDF size)
    bins = []
    for thickness, material in material_combos:
        bin_id = f"Board-{material}-{thickness}mm"
        bins.append(Bin(
            id=bin_id,
            width=2440,
            height=1220,
            thickness=thickness,
            material=material,
            available=-1  # Unlimited
        ))

    print(f"Created {len(bins)} bin types")

    return items, bins


def test_algorithms(items, bins):
    """Test different algorithms and compare results."""

    problem = Problem(
        items=items,
        bins=bins,
        kerf=3.5,
        utilization_threshold=0.78,
        time_limit=30.0
    )

    algorithms = [
        MaximalRectanglesAlgorithm(time_limit=30.0, lookahead_depth=1),
        MaximalRectanglesAlgorithm(time_limit=30.0, lookahead_depth=2),
        MaximalRectanglesAlgorithm(time_limit=30.0, lookahead_depth=3),
        GuillotinePacker(time_limit=30.0),
    ]

    results = []

    for algo in algorithms:
        print(f"\n{'='*60}")
        print(f"Testing: {algo.get_name()}")
        print(f"{'='*60}")

        solution = algo.solve(problem)

        print(f"Bins used: {solution.num_bins()}")
        print(f"Utilization: {solution.total_utilization()*100:.1f}%")
        print(f"Execution time: {solution.metadata.get('execution_time', 0):.2f}s")
        print(f"Complete: {solution.is_complete()}")

        if solution.unplaced:
            print(f"Unplaced items: {len(solution.unplaced)}")
            for item, qty in solution.unplaced:
                print(f"  - {item.id}: {qty} pieces")

        # Show bin details
        print(f"\nBin details:")
        for bin_packing in solution.bins[:5]:  # Show first 5
            print(f"  Bin {bin_packing.bin_id}: {len(bin_packing.items)} items, "
                  f"{bin_packing.utilization()*100:.1f}% utilized")

        if len(solution.bins) > 5:
            print(f"  ... and {len(solution.bins) - 5} more bins")

        results.append({
            'algorithm': algo.get_name(),
            'bins': solution.num_bins(),
            'utilization': solution.total_utilization(),
            'time': solution.metadata.get('execution_time', 0),
            'complete': solution.is_complete()
        })

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'Algorithm':<30} {'Bins':<10} {'Util%':<10} {'Time(s)':<10}")
    print(f"{'-'*60}")
    for r in results:
        print(f"{r['algorithm']:<30} {r['bins']:<10} {r['utilization']*100:<10.1f} {r['time']:<10.2f}")

    best = min(results, key=lambda x: (x['bins'], -x['utilization']))
    print(f"\nBest result: {best['algorithm']} with {best['bins']} bins")

    return results


if __name__ == "__main__":
    print("Loading benchmark data...")
    items, bins = load_benchmark_data('test_data/bench/cutting_plan_data.xlsx')

    print("\nTesting algorithms...")
    results = test_algorithms(items, bins)

    print("\nDone!")
