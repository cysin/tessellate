"""
GDRR (Goal-Driven Ruin and Recreate) Packer

Inspired by the algorithm from https://github.com/JeroenGar/gdrr-2bp.git
Paper: "A goal-driven ruin and recreate heuristic for the 2D variable-sized
        bin packing problem with guillotine constraints"
        https://doi.org/10.1016/j.ejor.2021.11.031

Key concepts:
1. Late Acceptance Hill Climbing (LAHC): Accepts solutions better than
   the solution from L_h iterations ago (not just current best)
2. Ruin phase: Removes items from bins, biased towards low-utilization bins
3. Recreate phase: Rebuilds using greedy insertion
4. Goal-driven: Uses goals to guide the search towards complete solutions
"""

import time
import random
from collections import deque
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.algorithms.skyline import SkylinePacker
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking
)


class GDRRPacker(PackingAlgorithm):
    """
    GDRR-inspired packer using Late Acceptance Hill Climbing.

    Implements:
    - Late Acceptance: Accepts solutions better than L_h iterations ago
    - Biased Ruin: Prefers to ruin bins with lower utilization
    - Goal-Driven: Targets complete solutions with minimum bins
    """

    def __init__(
        self,
        time_limit: float = 60.0,
        iterations: int = 500,
        history_length: int = 100,
        avg_items_removed: int = 8,
        ruin_percentage: float = 0.25
    ):
        """
        Initialize GDRR packer.

        Args:
            time_limit: Maximum execution time in seconds
            iterations: Number of ruin-recreate iterations
            history_length: Length of LAHC history queue
            avg_items_removed: Average number of items to remove per iteration
            ruin_percentage: Percentage of bins to ruin (fallback)
        """
        super().__init__(time_limit)
        self.iterations = iterations
        self.history_length = history_length
        self.avg_items_removed = avg_items_removed
        self.ruin_percentage = ruin_percentage

    def get_name(self) -> str:
        return "GDRR"

    def solve(self, problem: Problem) -> Solution:
        """Solve using GDRR with Late Acceptance Hill Climbing."""

        start_time = time.time()

        # Get initial solution using Skyline
        print(f"GDRR: Getting initial solution...")
        initial_solver = SkylinePacker(time_limit=min(5.0, self.time_limit * 0.1))
        current_solution = initial_solver.solve(problem)

        if current_solution.num_bins() == 0:
            return current_solution

        print(f"GDRR: Initial solution: {current_solution.num_bins()} bins @ {current_solution.total_utilization():.2%}")

        # Initialize LAHC history queue
        lahc_history = deque(maxlen=self.history_length)
        initial_cost = self._solution_cost(current_solution)
        lahc_history.append(initial_cost)

        best_solution = current_solution
        best_cost = initial_cost

        n_accepted = 0
        n_improved = 0

        # Main GDRR loop
        for iteration in range(self.iterations):
            if time.time() - start_time > self.time_limit * 0.9:
                print(f"GDRR: Time limit reached at iteration {iteration}")
                break

            # Ruin phase: Remove items from low-utilization bins
            items_to_repack, remaining_solution = self._ruin_biased(
                current_solution, problem
            )

            if not items_to_repack:
                continue

            # Recreate phase: Rebuild solution
            new_solution = self._recreate(
                items_to_repack, remaining_solution, problem, start_time
            )

            if not new_solution or len(new_solution.unplaced) > 0:
                # Failed to recreate, keep current solution
                if iteration < 10 or iteration % 100 == 0:
                    print(f"  Iteration {iteration}: Recreate failed, keeping current solution")
                continue

            new_cost = self._solution_cost(new_solution)

            # Late Acceptance criterion:
            # Accept if better than oldest entry in history
            accept = False

            if new_cost <= lahc_history[0]:
                accept = True
                n_accepted += 1

                # Update best if improved
                if new_cost < best_cost:
                    best_solution = new_solution
                    best_cost = new_cost
                    n_improved += 1

                    if iteration % 10 == 0:
                        print(f"  Iteration {iteration}: {best_solution.num_bins()} bins @ "
                              f"{best_solution.total_utilization():.2%} "
                              f"(accepted: {n_accepted}, improved: {n_improved})")

            # Update history queue
            if accept:
                current_solution = new_solution
                lahc_history.append(new_cost)

                # Verify item count for debugging
                items_in_solution = sum(len(bp.items) for bp in current_solution.bins)
                if items_in_solution != 80 and iteration < 10:
                    print(f"  WARNING: Iteration {iteration}: Only {items_in_solution}/80 items in solution!")
            else:
                # Keep current solution, add its cost to history
                lahc_history.append(lahc_history[-1])

        print(f"GDRR: Finished {iteration + 1} iterations in {time.time() - start_time:.1f}s")
        print(f"      Accepted: {n_accepted}/{iteration + 1}, Improved: {n_improved}")
        print(f"      Final: {best_solution.num_bins()} bins @ {best_solution.total_utilization():.2%}")

        best_solution.metadata["algorithm"] = self.get_name()
        best_solution.metadata["iterations"] = iteration + 1
        best_solution.metadata["accepted"] = n_accepted
        best_solution.metadata["improved"] = n_improved

        return best_solution

    def _solution_cost(self, solution: Solution) -> Tuple[int, float]:
        """
        Calculate solution cost: (bins, -utilization)
        Lower is better.
        """
        return (solution.num_bins(), -solution.total_utilization())

    def _ruin_biased(
        self,
        solution: Solution,
        problem: Problem
    ) -> Tuple[List[Item], Solution]:
        """
        Ruin phase: Remove items from bins, biased towards low-utilization bins.

        Strategy:
        1. Calculate utilization for each bin
        2. Bias selection towards bins with lower utilization
        3. Remove items from selected bins
        """

        if solution.num_bins() == 0:
            return [], solution

        # Calculate bin utilizations
        bin_utils = []
        for bin_packing in solution.bins:
            util = bin_packing.utilization()
            bin_utils.append((bin_packing, util))

        # Sort by utilization (lowest first) - these are preferred for ruining
        bin_utils.sort(key=lambda x: x[1])

        # Determine number of items to remove (random around average)
        min_items = max(2, self.avg_items_removed - 4)
        max_items = self.avg_items_removed + 4
        num_items_to_remove = random.randint(min_items, max_items)

        # Biased sampling: prefer bins with lower utilization
        # Use inverse of rank as weight
        weights = [1.0 / (i + 1) for i in range(len(bin_utils))]
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]

        items_to_repack = []
        bins_to_keep = []
        ruined_bin_indices = set()

        # Remove items
        items_removed = 0
        while items_removed < num_items_to_remove and len(bin_utils) > 0:
            # Biased selection
            selected_idx = random.choices(range(len(bin_utils)), weights=weights[:len(bin_utils)])[0]
            bin_packing, util = bin_utils.pop(selected_idx)
            weights.pop(selected_idx)

            # Mark for ruining and collect items
            ruined_bin_indices.add(bin_packing.bin_id)
            for placed_item in bin_packing.items:
                items_to_repack.append(placed_item.item)
                items_removed += 1

        # Keep bins that weren't ruined - make deep copies to avoid mutation
        for bin_packing in solution.bins:
            if bin_packing.bin_id not in ruined_bin_indices:
                # Create a new BinPacking with copied items list
                from tessellate.core.models import BinPacking as BP
                new_bp = BP(
                    bin_id=bin_packing.bin_id,
                    bin_type=bin_packing.bin_type,
                    items=bin_packing.items.copy()  # Copy the items list
                )
                bins_to_keep.append(new_bp)

        # Create remaining solution
        remaining_solution = Solution()
        remaining_solution.bins = bins_to_keep
        remaining_solution.metadata = solution.metadata.copy()

        return items_to_repack, remaining_solution

    def _recreate(
        self,
        items_to_repack: List[Item],
        remaining_solution: Solution,
        problem: Problem,
        start_time: float
    ) -> Optional[Solution]:
        """
        Recreate phase: Rebuild solution by packing removed items.

        Uses Skyline algorithm for repacking.
        """

        if not items_to_repack:
            return remaining_solution

        # Get compatible bins for these items
        if not items_to_repack:
            return remaining_solution

        compatible_bins = problem.get_compatible_bins(items_to_repack[0])
        if not compatible_bins:
            return None

        bin_type = compatible_bins[0]

        # Count items by type - use Item objects as keys to handle instances properly
        item_counts = {}
        item_map = {}  # Map from item.id to original Item object

        for item in items_to_repack:
            if item.id not in item_map:
                item_map[item.id] = item
            item_counts[item.id] = item_counts.get(item.id, 0) + 1

        # Create items with quantities for subproblem using original Item objects
        repack_items = []
        for item_id, count in item_counts.items():
            original_item = item_map[item_id]
            repack_item = Item(
                id=original_item.id,
                width=original_item.width,
                height=original_item.height,
                thickness=original_item.thickness,
                material=original_item.material,
                quantity=count,
                rotatable=original_item.rotatable
            )
            repack_items.append(repack_item)

        # Create subproblem
        subproblem = Problem(
            items=repack_items,
            bins=[bin_type],
            kerf=problem.kerf
        )

        # Solve subproblem with Skyline
        time_remaining = max(1.0, self.time_limit * 0.9 - (time.time() - start_time))
        repacker = SkylinePacker(time_limit=min(5.0, time_remaining / 10), use_min_waste=True)
        repack_solution = repacker.solve(subproblem)

        # Check if all items were placed
        if len(repack_solution.unplaced) > 0:
            # Debug: print why recreate failed
            total_unplaced = sum(qty for _, qty in repack_solution.unplaced)
            # print(f"    Recreate failed: {total_unplaced} items unplaced")
            return None

        # Combine solutions
        combined_solution = Solution()
        combined_solution.bins = remaining_solution.bins + repack_solution.bins

        # Renumber bin IDs
        for i, bin_packing in enumerate(combined_solution.bins):
            bin_packing.bin_id = i

        combined_solution.metadata = remaining_solution.metadata.copy()

        return combined_solution


class GDRRLightPacker(PackingAlgorithm):
    """
    Lightweight GDRR variant with fewer iterations.

    Suitable for quick optimization (10-30 seconds).
    """

    def __init__(self, time_limit: float = 30.0):
        self.gdrr = GDRRPacker(
            time_limit=time_limit,
            iterations=200,
            history_length=50,
            avg_items_removed=6
        )
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "GDRR-Light"

    def solve(self, problem: Problem) -> Solution:
        return self.gdrr.solve(problem)
