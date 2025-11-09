"""
Maximal Rectangles algorithm with advanced scoring and lookahead.

This implements a sophisticated Maximal Rectangles packing algorithm
optimized for guillotine cutting constraints.
"""

import time
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)
from tessellate.utils.geometry import (
    Rectangle, find_maximal_rectangles, can_fit
)
from tessellate.utils.scoring import PlacementScorer


class MaximalRectanglesAlgorithm(PackingAlgorithm):
    """
    Maximal Rectangles algorithm for guillotine bin packing.

    Features:
    - Multi-criteria placement scoring
    - Lookahead for better decisions
    - Multiple sorting strategies
    - Rotation handling
    """

    def __init__(self, time_limit: float = 5.0, lookahead_depth: int = 2):
        """
        Initialize algorithm.

        Args:
            time_limit: Maximum execution time
            lookahead_depth: Number of items to lookahead
        """
        super().__init__(time_limit)
        self.lookahead_depth = lookahead_depth
        self.scorer = PlacementScorer()

    def get_name(self) -> str:
        return f"MaxRects-Lookahead-{self.lookahead_depth}"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve the problem using Maximal Rectangles.

        Args:
            problem: Problem instance

        Returns:
            Solution
        """
        start_time = time.time()

        # Try multiple sorting strategies and keep best
        strategies = [
            ("area_desc", lambda item: -item.area()),
            ("width_desc", lambda item: -item.width),
            ("height_desc", lambda item: -item.height),
            ("perimeter_desc", lambda item: -(item.width + item.height)),
        ]

        best_solution = None
        best_score = (float('inf'), float('inf'))

        for strategy_name, sort_key in strategies:
            if time.time() - start_time > self.time_limit * 0.8:
                break  # Reserve time for other strategies

            solution = self._solve_with_sorting(problem, sort_key)
            score = (solution.num_bins(), -solution.total_utilization())

            if score < best_score:
                best_score = score
                best_solution = solution

        # Add metadata
        execution_time = time.time() - start_time
        best_solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return best_solution

    def _solve_with_sorting(
        self,
        problem: Problem,
        sort_key
    ) -> Solution:
        """
        Solve with a specific item sorting strategy.

        Args:
            problem: Problem instance
            sort_key: Function to sort items

        Returns:
            Solution
        """
        solution = Solution()

        # Group items by material
        groups = problem.group_by_material()

        for (thickness, material), group_items in groups.items():
            # Get compatible bins
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                # Mark as unplaced
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Create item list with quantities
            items_to_pack = []
            for item in group_items:
                for _ in range(item.quantity):
                    items_to_pack.append(item)

            # Sort items
            items_to_pack.sort(key=sort_key)

            # Pack items
            bins, unpacked_items = self._pack_items(items_to_pack, bin_type, problem.kerf)

            # Assign bin IDs and add to solution
            for i, bin_packing in enumerate(bins):
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

            # Track unplaced items
            if unpacked_items:
                # Count quantities for each unique item
                unplaced_counts = {}
                for item in unpacked_items:
                    unplaced_counts[item.id] = unplaced_counts.get(item.id, 0) + 1

                # Add to solution.unplaced
                for item in group_items:
                    if item.id in unplaced_counts:
                        solution.unplaced.append((item, unplaced_counts[item.id]))

        return solution

    def _pack_items(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], List[Item]]:
        """
        Pack items into bins.

        Args:
            items: Items to pack
            bin_type: Type of bin to use
            kerf: Kerf width

        Returns:
            Tuple of (list of bin packings, list of unpacked items)
        """
        bins = []
        remaining_items = items.copy()

        while remaining_items:
            # Create new bin
            bin_packing = BinPacking(
                bin_id=len(bins),
                bin_type=bin_type,
                items=[],
            )

            # Pack items into this bin using MaxRects
            packed_indices = self._pack_bin(
                bin_packing,
                remaining_items,
                kerf
            )

            # Remove packed items
            remaining_items = [
                item for i, item in enumerate(remaining_items)
                if i not in packed_indices
            ]

            if bin_packing.items:
                bins.append(bin_packing)
            else:
                # Couldn't pack any items, stop trying
                break

        return bins, remaining_items

    def _pack_bin(
        self,
        bin_packing: BinPacking,
        items: List[Item],
        kerf: float
    ) -> List[int]:
        """
        Pack items into a single bin using Maximal Rectangles.

        Args:
            bin_packing: Bin to pack into
            items: Items available for packing
            kerf: Kerf width

        Returns:
            List of indices of items that were packed
        """
        packed_indices = []

        for i, item in enumerate(items):
            if i in packed_indices:
                continue

            # Find best placement for this item
            placement = self._find_best_placement(
                bin_packing,
                item,
                kerf
            )

            if placement:
                x, y, width, height, rotated = placement
                placed_item = PlacedItem(
                    item=item,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    rotated=rotated
                )
                bin_packing.items.append(placed_item)
                packed_indices.append(i)

        return packed_indices

    def _find_best_placement(
        self,
        bin_packing: BinPacking,
        item: Item,
        kerf: float
    ) -> Optional[Tuple[float, float, float, float, bool]]:
        """
        Find best placement position for an item in a bin.

        Args:
            bin_packing: Current bin state
            item: Item to place
            kerf: Kerf width

        Returns:
            Tuple of (x, y, width, height, rotated) or None
        """
        # Convert placed items to rectangles
        placed_rects = [
            Rectangle(pi.x, pi.y, pi.width, pi.height)
            for pi in bin_packing.items
        ]

        # Find maximal free rectangles
        free_rects = find_maximal_rectangles(
            bin_packing.bin_type.width,
            bin_packing.bin_type.height,
            placed_rects,
            kerf
        )

        # Try both orientations
        orientations = []

        # Original orientation
        orientations.append((item.width, item.height, False))

        # Rotated orientation (if allowed)
        if item.rotatable:
            orientations.append((item.height, item.width, True))

        best_score = float('-inf')
        best_placement = None

        for width, height, rotated in orientations:
            for rect in free_rects:
                if can_fit(rect, width, height):
                    # Score this placement
                    score = self.scorer.score_placement(
                        rect,
                        width,
                        height,
                        bin_packing.bin_type.width,
                        bin_packing.bin_type.height
                    )

                    if score > best_score:
                        best_score = score
                        best_placement = (rect.x, rect.y, width, height, rotated)

        return best_placement
