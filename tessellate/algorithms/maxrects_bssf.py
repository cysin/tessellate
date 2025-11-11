"""
MaxRects with Best Short Side Fit (BSSF) - Optimized for tight packing.

Based on research from multiple high-performance bin packing libraries,
particularly the BSSF heuristic which consistently achieves the tightest packings.
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


class MaxRectsBSSFAlgorithm(PackingAlgorithm):
    """
    MaxRects with Best Short Side Fit heuristic.

    This is one of the best-performing rectangle packing algorithms,
    minimizing wasted space by choosing placements that minimize
    the leftover space on the shorter side.
    """

    def __init__(self, time_limit: float = 30.0):
        super().__init__(time_limit)
        self.scorer = PlacementScorer()

    def get_name(self) -> str:
        return "MaxRects-BSSF"

    def solve(self, problem: Problem) -> Solution:
        """Solve using MaxRects BSSF."""
        start_time = time.time()

        # Try multiple sorting strategies
        strategies = [
            ("area_desc", lambda item: (-item.area(), -max(item.width, item.height))),
            ("perimeter_desc", lambda item: (-(item.width + item.height), -item.area())),
            ("max_side_desc", lambda item: (-max(item.width, item.height), -item.area())),
            ("aspect_ratio", lambda item: (-abs(item.width - item.height), -item.area())),
        ]

        best_solution = None
        best_score = (float('inf'), float('-inf'))

        for strategy_name, sort_key in strategies:
            if time.time() - start_time > self.time_limit * 0.9:
                break

            solution = self._solve_with_sorting(problem, sort_key)
            score = (solution.num_bins(), solution.total_utilization())

            if score[0] < best_score[0] or (score[0] == best_score[0] and score[1] > best_score[1]):
                best_score = score
                best_solution = solution

        execution_time = time.time() - start_time
        best_solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return best_solution

    def _solve_with_sorting(self, problem: Problem, sort_key) -> Solution:
        """Solve with a specific sorting strategy."""
        solution = Solution()

        # Group by material
        groups = problem.group_by_material()

        for (thickness, material), group_items in groups.items():
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Expand items with quantities
            items_to_pack = []
            for item in group_items:
                for _ in range(item.quantity):
                    items_to_pack.append(item)

            # Sort items
            items_to_pack.sort(key=sort_key)

            # Pack items
            bins, unpacked = self._pack_items(items_to_pack, bin_type, problem.kerf)

            for i, bin_packing in enumerate(bins):
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

            if unpacked:
                unplaced_counts = {}
                for item in unpacked:
                    unplaced_counts[item.id] = unplaced_counts.get(item.id, 0) + 1

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
        """Pack items into bins using MaxRects BSSF."""
        bins = []
        remaining_items = items.copy()

        while remaining_items:
            bin_packing = BinPacking(
                bin_id=len(bins),
                bin_type=bin_type,
                items=[]
            )

            # Initialize free rectangles with full bin
            free_rects = [Rectangle(0, 0, bin_type.width, bin_type.height)]

            packed_indices = []

            # Try to pack items greedily
            while True:
                best_item_idx = None
                best_placement = None
                best_score = (float('inf'), float('inf'))

                # Find best item to pack next
                for i, item in enumerate(remaining_items):
                    if i in packed_indices:
                        continue

                    placement, score = self._find_best_placement_bssf(
                        item, free_rects, kerf
                    )

                    if placement and score < best_score:
                        best_score = score
                        best_placement = placement
                        best_item_idx = i

                if best_item_idx is None:
                    break  # No more items can fit

                # Place the best item
                item = remaining_items[best_item_idx]
                x, y, width, height, rotated = best_placement

                placed_item = PlacedItem(
                    item=item,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    rotated=rotated
                )
                bin_packing.items.append(placed_item)
                packed_indices.append(best_item_idx)

                # Update free rectangles
                free_rects = self._update_free_rectangles(
                    free_rects, x, y, width, height, kerf
                )

            # Remove packed items
            remaining_items = [
                item for i, item in enumerate(remaining_items)
                if i not in packed_indices
            ]

            if bin_packing.items:
                bins.append(bin_packing)
            else:
                break

        return bins, remaining_items

    def _find_best_placement_bssf(
        self,
        item: Item,
        free_rects: List[Rectangle],
        kerf: float
    ) -> Tuple[Optional[Tuple[float, float, float, float, bool]], Tuple[float, float]]:
        """
        Find best placement using BSSF heuristic.

        Returns: (placement tuple, score tuple) or (None, (inf, inf))
        """
        best_placement = None
        best_score = (float('inf'), float('inf'))

        # Try all free rectangles
        for rect in free_rects:
            # Try both orientations
            orientations = [(item.width, item.height, False)]
            if item.rotatable:
                orientations.append((item.height, item.width, True))

            for width, height, rotated in orientations:
                if can_fit(rect, width, height):
                    # Calculate BSSF score
                    leftover_horizontal = rect.width - width
                    leftover_vertical = rect.height - height
                    short_side_fit = min(leftover_horizontal, leftover_vertical)
                    long_side_fit = max(leftover_horizontal, leftover_vertical)

                    # Primary: minimize short side, Secondary: minimize long side
                    score = (short_side_fit, long_side_fit)

                    if score < best_score:
                        best_score = score
                        best_placement = (rect.x, rect.y, width, height, rotated)

        return best_placement, best_score

    def _update_free_rectangles(
        self,
        free_rects: List[Rectangle],
        placed_x: float,
        placed_y: float,
        placed_width: float,
        placed_height: float,
        kerf: float
    ) -> List[Rectangle]:
        """
        Update free rectangles after placing an item.

        This implements the maximal rectangles algorithm:
        1. Remove any free rectangles that intersect the placed item
        2. Generate new maximal rectangles from the intersection
        """
        new_rects = []

        # Account for kerf
        placed_right = placed_x + placed_width + kerf
        placed_top = placed_y + placed_height + kerf

        for rect in free_rects:
            rect_right = rect.x + rect.width
            rect_top = rect.y + rect.height

            # Check if rectangles intersect
            if not (placed_right <= rect.x or placed_x >= rect_right or
                    placed_top <= rect.y or placed_y >= rect_top):
                # They intersect - split the free rectangle

                # Left slice
                if placed_x > rect.x:
                    new_rects.append(Rectangle(
                        rect.x,
                        rect.y,
                        placed_x - rect.x,
                        rect.height
                    ))

                # Right slice
                if placed_right < rect_right:
                    new_rects.append(Rectangle(
                        placed_right,
                        rect.y,
                        rect_right - placed_right,
                        rect.height
                    ))

                # Bottom slice
                if placed_y > rect.y:
                    new_rects.append(Rectangle(
                        rect.x,
                        rect.y,
                        rect.width,
                        placed_y - rect.y
                    ))

                # Top slice
                if placed_top < rect_top:
                    new_rects.append(Rectangle(
                        rect.x,
                        placed_top,
                        rect.width,
                        rect_top - placed_top
                    ))
            else:
                # No intersection, keep the rectangle
                new_rects.append(rect)

        # Remove redundant rectangles (those contained in others)
        new_rects = self._prune_rectangles(new_rects)

        return new_rects

    def _prune_rectangles(self, rects: List[Rectangle]) -> List[Rectangle]:
        """Remove rectangles that are contained within other rectangles."""
        if len(rects) <= 1:
            return rects

        pruned = []
        for i, rect1 in enumerate(rects):
            is_contained = False
            for j, rect2 in enumerate(rects):
                if i != j and self._is_contained(rect1, rect2):
                    is_contained = True
                    break
            if not is_contained:
                pruned.append(rect1)

        return pruned

    def _is_contained(self, rect1: Rectangle, rect2: Rectangle) -> bool:
        """Check if rect1 is contained within rect2."""
        return (rect1.x >= rect2.x and
                rect1.y >= rect2.y and
                rect1.x + rect1.width <= rect2.x + rect2.width and
                rect1.y + rect1.height <= rect2.y + rect2.height)
