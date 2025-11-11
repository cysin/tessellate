"""
ILP Decomposition Packer - Solves smaller subproblems optimally.

Strategy:
1. Partition items into groups (e.g., 20 items each)
2. Solve each group with ILP to minimize bins
3. Combine results

This makes ILP tractable by reducing problem size:
- 20 items: 190 pairs, ~10K variables (solvable!)
- 80 items: 3160 pairs, ~160K variables (too large)
"""

import time
import math
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.algorithms.ilp_simplified_packer import SimplifiedILPPacker
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking
)


class ILPDecompositionPacker(PackingAlgorithm):
    """
    ILP packer using decomposition strategy.

    Breaks large problems into smaller subproblems that ILP can solve optimally.
    """

    def __init__(
        self,
        time_limit: float = 300.0,
        group_size: int = 20,
        mip_gap: float = 0.05
    ):
        """
        Initialize decomposition ILP packer.

        Args:
            time_limit: Maximum solving time in seconds
            group_size: Number of items per group (20 is manageable for ILP)
            mip_gap: MIP optimality gap
        """
        super().__init__(time_limit)
        self.group_size = group_size
        self.mip_gap = mip_gap

    def get_name(self) -> str:
        return "ILP-Decomposition"

    def solve(self, problem: Problem) -> Solution:
        """Solve using decomposition strategy."""

        start_time = time.time()

        # Group by material (solve each material separately)
        groups = problem.group_by_material()

        solution = Solution()

        for (thickness, material), group_items in groups.items():
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Expand items by quantity
            items_list = []
            for item in group_items:
                for q in range(item.quantity):
                    items_list.append(item)

            print(f"\nSolving with ILP Decomposition for {len(items_list)} items...")
            print(f"Group size: {self.group_size} items per subproblem")

            # Partition into groups
            num_groups = math.ceil(len(items_list) / self.group_size)
            print(f"Number of subproblems: {num_groups}")

            total_bins = 0

            for group_idx in range(num_groups):
                if time.time() - start_time > self.time_limit * 0.9:
                    print(f"  Time limit reached, stopping at group {group_idx}/{num_groups}")
                    break

                start_idx = group_idx * self.group_size
                end_idx = min((group_idx + 1) * self.group_size, len(items_list))
                group_items_subset = items_list[start_idx:end_idx]

                print(f"\n  Subproblem {group_idx + 1}/{num_groups}: {len(group_items_subset)} items")

                # Convert to items with quantities
                item_counts = {}
                for item in group_items_subset:
                    item_counts[item.id] = item_counts.get(item.id, 0) + 1

                subproblem_items = []
                for orig_item in group_items:
                    if orig_item.id in item_counts:
                        subproblem_item = Item(
                            id=orig_item.id,
                            width=orig_item.width,
                            height=orig_item.height,
                            thickness=orig_item.thickness,
                            material=orig_item.material,
                            quantity=item_counts[orig_item.id],
                            rotatable=orig_item.rotatable
                        )
                        subproblem_items.append(subproblem_item)

                # Create subproblem
                subproblem = Problem(
                    items=subproblem_items,
                    bins=[bin_type],
                    kerf=problem.kerf
                )

                # Estimate target bins (based on area)
                total_area = sum(item.width * item.height * item.quantity
                                for item in subproblem_items)
                bin_area = bin_type.width * bin_type.height
                estimated_bins = max(1, math.ceil(total_area / (bin_area * 0.85)))

                print(f"    Estimated bins: {estimated_bins}")

                # Solve with ILP (try target bins, then target+1, target+2)
                subsolution = None
                for target in range(estimated_bins, estimated_bins + 3):
                    print(f"    Trying {target} bins...")

                    time_remaining = max(10, self.time_limit * 0.9 - (time.time() - start_time))
                    time_per_group = time_remaining / (num_groups - group_idx)

                    solver = SimplifiedILPPacker(
                        time_limit=min(30, time_per_group),
                        target_bins=target,
                        mip_gap=self.mip_gap
                    )

                    subsolution = solver.solve(subproblem)

                    if subsolution and len(subsolution.unplaced) == 0:
                        print(f"    ✓ Solved with {subsolution.num_bins()} bins")
                        break

                    print(f"    ✗ Failed with {target} bins")

                if subsolution and len(subsolution.unplaced) == 0:
                    # Add bins to solution
                    for bp in subsolution.bins:
                        bp.bin_id = len(solution.bins)
                        solution.bins.append(bp)
                    total_bins += subsolution.num_bins()
                else:
                    # Failed - add items to unplaced
                    print(f"    WARNING: Could not solve subproblem {group_idx + 1}")
                    for item in subproblem_items:
                        solution.unplaced.append((item, item.quantity))

            print(f"\nTotal bins used: {total_bins}")

        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution
