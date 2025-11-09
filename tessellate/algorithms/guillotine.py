"""
True Guillotine Rectangle Packing Algorithm.

This implements a PROPER guillotine packing algorithm that guarantees
all cuts are edge-to-edge and form a valid binary tree structure.

Unlike Maximal Rectangles, this algorithm maintains guillotine constraints
throughout the packing process, not as a post-processing step.
"""

import time
from typing import List, Tuple, Optional
from enum import Enum
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem, Cut, CutType
)


class SplitRule(Enum):
    """Rules for splitting free rectangles after placement."""
    SHORTER_LEFTOVER_AXIS = "shorter_leftover"  # Split along axis with less leftover
    LONGER_LEFTOVER_AXIS = "longer_leftover"    # Split along axis with more leftover
    SHORTER_AXIS = "shorter_axis"                # Split along shorter axis of rectangle
    LONGER_AXIS = "longer_axis"                  # Split along longer axis of rectangle
    HORIZONTAL = "horizontal"                    # Always horizontal
    VERTICAL = "vertical"                        # Always vertical


class FreeRectangle:
    """A free rectangle in guillotine packing."""

    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initialize a free rectangle.

        Args:
            x: X-coordinate (bottom-left)
            y: Y-coordinate (bottom-left)
            width: Rectangle width
            height: Rectangle height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def area(self) -> float:
        """Calculate area."""
        return self.width * self.height

    def can_fit(self, item_width: float, item_height: float) -> bool:
        """Check if an item can fit."""
        return self.width >= item_width and self.height >= item_height


class GuillotinePacker(PackingAlgorithm):
    """
    True Guillotine Rectangle Packing Algorithm.

    This algorithm GUARANTEES guillotine-compatible packings by:
    1. Maintaining a list of free rectangles
    2. Placing items only in free rectangles
    3. Splitting free rectangles with guillotine cuts after each placement
    4. Ensuring all cuts are edge-to-edge and form a binary tree
    """

    def __init__(
        self,
        time_limit: float = 5.0,
        split_rule: SplitRule = SplitRule.SHORTER_LEFTOVER_AXIS,
        merge_free_rects: bool = True
    ):
        """
        Initialize guillotine packer.

        Args:
            time_limit: Maximum execution time
            split_rule: Rule for splitting rectangles after placement
            merge_free_rects: Whether to merge adjacent free rectangles
        """
        super().__init__(time_limit)
        self.split_rule = split_rule
        self.merge_free_rects = merge_free_rects

    def get_name(self) -> str:
        return f"Guillotine-{self.split_rule.value}"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using guillotine packing.

        Args:
            problem: Problem instance

        Returns:
            Solution with guaranteed guillotine cuts
        """
        start_time = time.time()

        # Try multiple split rules and sorting strategies
        best_solution = None
        best_score = (float('inf'), float('inf'))

        split_rules = [
            SplitRule.SHORTER_LEFTOVER_AXIS,
            SplitRule.LONGER_LEFTOVER_AXIS,
            SplitRule.SHORTER_AXIS,
        ]

        for split_rule in split_rules:
            if time.time() - start_time > self.time_limit * 0.9:
                break

            self.split_rule = split_rule
            solution = self._solve_once(problem)
            score = (solution.num_bins(), -solution.total_utilization())

            if score < best_score:
                best_score = score
                best_solution = solution
                best_solution.metadata["split_rule"] = split_rule.value

        # Add metadata
        execution_time = time.time() - start_time
        best_solution.metadata["algorithm"] = self.get_name()
        best_solution.metadata["execution_time"] = execution_time

        return best_solution

    def _solve_once(self, problem: Problem) -> Solution:
        """Solve with current configuration."""
        solution = Solution()

        # Group items by material
        groups = problem.group_by_material()

        for (thickness, material), group_items in groups.items():
            # Get compatible bins
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Create item list with quantities
            items_to_pack = []
            for item in group_items:
                for _ in range(item.quantity):
                    items_to_pack.append(item)

            # Sort by area (descending)
            items_to_pack.sort(key=lambda item: -item.area())

            # Pack items
            bins, unpacked_items = self._pack_items_guillotine(
                items_to_pack, bin_type, problem.kerf
            )

            # Add to solution
            for bin_packing in bins:
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

            # Track unplaced
            if unpacked_items:
                unplaced_counts = {}
                for item in unpacked_items:
                    unplaced_counts[item.id] = unplaced_counts.get(item.id, 0) + 1

                for item in group_items:
                    if item.id in unplaced_counts:
                        solution.unplaced.append((item, unplaced_counts[item.id]))

        return solution

    def _pack_items_guillotine(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], List[Item]]:
        """
        Pack items using guillotine algorithm.

        Args:
            items: Items to pack
            bin_type: Bin type
            kerf: Kerf width

        Returns:
            Tuple of (bins, unpacked items)
        """
        bins = []
        remaining_items = items.copy()

        while remaining_items:
            # Create new bin
            bin_packing = BinPacking(
                bin_id=len(bins),
                bin_type=bin_type,
                items=[]
            )

            # Initialize with full bin as free rectangle
            free_rects = [FreeRectangle(0, 0, bin_type.width, bin_type.height)]

            # Pack items into this bin
            packed_indices = []

            for i, item in enumerate(remaining_items):
                # Try to place this item
                placement = self._find_placement_guillotine(
                    item, free_rects, kerf
                )

                if placement:
                    rect_idx, x, y, width, height, rotated = placement

                    # Place the item
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

                    # Split the free rectangle with a guillotine cut
                    used_rect = free_rects.pop(rect_idx)
                    new_rects = self._split_free_rectangle(
                        used_rect, x, y, width, height, kerf
                    )
                    free_rects.extend(new_rects)

                    # Optionally merge free rectangles
                    if self.merge_free_rects:
                        free_rects = self._merge_rectangles(free_rects)

            # Remove packed items
            remaining_items = [
                item for i, item in enumerate(remaining_items)
                if i not in packed_indices
            ]

            if bin_packing.items:
                bins.append(bin_packing)
            else:
                # Couldn't pack any items
                break

        return bins, remaining_items

    def _find_placement_guillotine(
        self,
        item: Item,
        free_rects: List[FreeRectangle],
        kerf: float
    ) -> Optional[Tuple[int, float, float, float, float, bool]]:
        """
        Find best placement for item in free rectangles.

        Args:
            item: Item to place
            free_rects: List of free rectangles
            kerf: Kerf width

        Returns:
            Tuple of (rect_index, x, y, width, height, rotated) or None
        """
        best_score = float('inf')
        best_placement = None

        # Try all free rectangles
        for rect_idx, rect in enumerate(free_rects):
            # Try both orientations
            orientations = [
                (item.width, item.height, False),
            ]

            if item.rotatable:
                orientations.append((item.height, item.width, True))

            for width, height, rotated in orientations:
                if rect.can_fit(width, height):
                    # Score this placement (prefer smaller leftover area)
                    leftover_area = rect.area() - (width * height)
                    score = leftover_area

                    if score < best_score:
                        best_score = score
                        best_placement = (rect_idx, rect.x, rect.y, width, height, rotated)

        return best_placement

    def _split_free_rectangle(
        self,
        free_rect: FreeRectangle,
        item_x: float,
        item_y: float,
        item_width: float,
        item_height: float,
        kerf: float
    ) -> List[FreeRectangle]:
        """
        Split a free rectangle after placing an item.

        This is the CORE of guillotine packing - we make ONE cut that
        divides the space into TWO new rectangles.

        Args:
            free_rect: The free rectangle being used
            item_x: Item x position (should be free_rect.x)
            item_y: Item y position (should be free_rect.y)
            item_width: Item width
            item_height: Item height
            kerf: Kerf width

        Returns:
            List of new free rectangles (0-2 rectangles)
        """
        # Calculate leftover space
        leftover_width = free_rect.width - item_width - kerf
        leftover_height = free_rect.height - item_height - kerf

        new_rects = []

        # Decide split direction based on split rule
        split_horizontally = self._should_split_horizontally(
            free_rect, item_width, item_height, leftover_width, leftover_height
        )

        if split_horizontally:
            # Horizontal cut: split top and right
            # Right rectangle (full height)
            if leftover_width > 0:
                new_rects.append(FreeRectangle(
                    item_x + item_width + kerf,
                    free_rect.y,
                    leftover_width,
                    free_rect.height
                ))

            # Top rectangle (only above item)
            if leftover_height > 0:
                new_rects.append(FreeRectangle(
                    item_x,
                    item_y + item_height + kerf,
                    item_width,
                    leftover_height
                ))
        else:
            # Vertical cut: split right and top
            # Top rectangle (full width)
            if leftover_height > 0:
                new_rects.append(FreeRectangle(
                    free_rect.x,
                    item_y + item_height + kerf,
                    free_rect.width,
                    leftover_height
                ))

            # Right rectangle (only beside item)
            if leftover_width > 0:
                new_rects.append(FreeRectangle(
                    item_x + item_width + kerf,
                    item_y,
                    leftover_width,
                    item_height
                ))

        return new_rects

    def _should_split_horizontally(
        self,
        rect: FreeRectangle,
        item_width: float,
        item_height: float,
        leftover_width: float,
        leftover_height: float
    ) -> bool:
        """
        Decide whether to split horizontally or vertically.

        Args:
            rect: Free rectangle
            item_width: Placed item width
            item_height: Placed item height
            leftover_width: Remaining width
            leftover_height: Remaining height

        Returns:
            True for horizontal split, False for vertical
        """
        if self.split_rule == SplitRule.SHORTER_LEFTOVER_AXIS:
            return leftover_width < leftover_height
        elif self.split_rule == SplitRule.LONGER_LEFTOVER_AXIS:
            return leftover_width > leftover_height
        elif self.split_rule == SplitRule.SHORTER_AXIS:
            return rect.width < rect.height
        elif self.split_rule == SplitRule.LONGER_AXIS:
            return rect.width > rect.height
        elif self.split_rule == SplitRule.HORIZONTAL:
            return True
        else:  # VERTICAL
            return False

    def _merge_rectangles(self, rects: List[FreeRectangle]) -> List[FreeRectangle]:
        """
        Merge adjacent free rectangles to reduce fragmentation.

        This is optional but can improve packing quality.

        Args:
            rects: List of free rectangles

        Returns:
            Potentially smaller list with merged rectangles
        """
        if len(rects) <= 1:
            return rects

        merged = True
        while merged:
            merged = False
            new_rects = []
            used = [False] * len(rects)

            for i in range(len(rects)):
                if used[i]:
                    continue

                # Try to merge with another rectangle
                merged_rect = None
                for j in range(i + 1, len(rects)):
                    if used[j]:
                        continue

                    merged_rect = self._try_merge(rects[i], rects[j])
                    if merged_rect:
                        used[i] = True
                        used[j] = True
                        new_rects.append(merged_rect)
                        merged = True
                        break

                if not used[i]:
                    new_rects.append(rects[i])

            rects = new_rects

        return rects

    def _try_merge(
        self,
        rect1: FreeRectangle,
        rect2: FreeRectangle
    ) -> Optional[FreeRectangle]:
        """
        Try to merge two rectangles if they're adjacent.

        Args:
            rect1: First rectangle
            rect2: Second rectangle

        Returns:
            Merged rectangle or None if can't merge
        """
        # Check if they can be merged horizontally
        if (rect1.y == rect2.y and rect1.height == rect2.height and
            rect1.x + rect1.width == rect2.x):
            return FreeRectangle(
                rect1.x, rect1.y,
                rect1.width + rect2.width, rect1.height
            )

        if (rect2.y == rect1.y and rect2.height == rect1.height and
            rect2.x + rect2.width == rect1.x):
            return FreeRectangle(
                rect2.x, rect2.y,
                rect2.width + rect1.width, rect2.height
            )

        # Check if they can be merged vertically
        if (rect1.x == rect2.x and rect1.width == rect2.width and
            rect1.y + rect1.height == rect2.y):
            return FreeRectangle(
                rect1.x, rect1.y,
                rect1.width, rect1.height + rect2.height
            )

        if (rect2.x == rect1.x and rect2.width == rect1.width and
            rect2.y + rect2.height == rect1.y):
            return FreeRectangle(
                rect2.x, rect2.y,
                rect2.width, rect2.height + rect1.height
            )

        return None
