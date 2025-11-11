#!/usr/bin/env python3
"""
Test the simplified ILP packer on manual1.xlsx dataset.
"""

import sys
import json
from pathlib import Path

# Add tessellate to path
sys.path.insert(0, str(Path(__file__).parent))

from tessellate.core.models import Problem
from tessellate.algorithms.ilp_simplified_packer import SimplifiedILPPacker


def main():
    # Load the manual1 test dataset
    data_path = Path("test_data/bench/manual1.json")

    if not data_path.exists():
        print(f"ERROR: {data_path} not found")
        return

    with open(data_path) as f:
        problem_data = json.load(f)

    problem = Problem.from_dict(problem_data)

    print("=" * 70)
    print("Testing Simplified ILP Packer on manual1.xlsx")
    print("=" * 70)
    print(f"Items: {sum(item.quantity for item in problem.items)}")
    print(f"Target: 10 boards")
    print()

    # Try simplified ILP targeting 10 bins
    solver = SimplifiedILPPacker(
        time_limit=300.0,  # 5 minutes
        target_bins=10,
        mip_gap=0.05
    )

    solution = solver.solve(problem)

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Bins: {solution.num_bins()}")
    print(f"Utilization: {solution.total_utilization():.2%}")
    print(f"Items placed: {sum(len(bp.items) for bp in solution.bins)}")
    print(f"Items unplaced: {sum(qty for _, qty in solution.unplaced)}")

    if solution.num_bins() == 10 and len(solution.unplaced) == 0:
        print()
        print("🎉 SUCCESS: Achieved 10 boards target!")
    elif solution.num_bins() > 0:
        print()
        print(f"Result: {solution.num_bins()} boards (target was 10)")
    else:
        print()
        print("❌ ILP solver could not find solution")


if __name__ == "__main__":
    main()
