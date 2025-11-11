"""
MaxRects with Contact Point Rule.

Implements the Contact Point heuristic from Jukka Jylänki's MaxRects algorithm.
This heuristic prefers placements that maximize contact with already-placed rectangles.
"""

import time
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.algorithms.maxrects import MaximalRectanglesAlgorithm
from tessellate.algorithms.guillotine import FreeRectangle
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class ContactPointMaxRects(PackingAlgorithm):
    """
    MaxRects with Contact Point scoring.

    The Contact Point Rule maximizes the "contact rating" - the total
    length of the edges of the placed rectangle that touch other rectangles
    or the bin boundaries.

    This creates more compact, connected packings.
    """

    def __init__(self, time_limit: float = 30.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "MaxRects-ContactPoint"

    def solve(self, problem: Problem) -> Solution:
        """Solve using MaxRects with Contact Point scoring."""
        start_time = time.time()
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

            # Expand items
            items_to_pack = []
            for item in group_items:
                for _ in range(item.quantity):
                    items_to_pack.append(item)

            # Sort by area (descending) for better initial placement
            items_to_pack.sort(key=lambda x: (-x.area(), -max(x.width, x.height)))

            # Pack using contact point
            bins, unpacked = self._pack_contact_point(
                items_to_pack, bin_type, problem.kerf
            )

            for bin_packing in bins:
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

            if unpacked:
                unplaced_counts = {}
                for item in unpacked:
                    unplaced_counts[item.id] = unplaced_counts.get(item.id, 0) + 1

                for item in group_items:
                    if item.id in unplaced_counts:
                        solution.unplaced.append((item, unplaced_counts[item.id]))

        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution

    def _pack_contact_point(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], List[Item]]:
        """Pack items using Contact Point heuristic."""
        bins: List[Tuple[BinPacking, List[FreeRectangle], List[PlacedItem]]] = []
        unpacked = []

        for item in items:
            best_bin_idx = None
            best_placement = None
            best_contact_score = -1

            # Try all existing bins
            for idx, (bin_packing, free_rects, placed_rects) in enumerate(bins):
                placement, contact_score = self._find_best_placement_in_bin(
                    item, free_rects, placed_rects, bin_type, kerf
                )

                if placement and contact_score > best_contact_score:
                    best_contact_score = contact_score
                    best_bin_idx = idx
                    best_placement = placement

            # Place in best bin or create new bin
            if best_bin_idx is not None:
                bin_packing, free_rects, placed_rects = bins[best_bin_idx]
                x, y, width, height, rotated, _ = best_placement

                placed_item = PlacedItem(
                    item=item,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                    rotated=rotated
                )
                bin_packing.items.append(placed_item)
                placed_rects.append(placed_item)

                # Update free rectangles
                new_free_rects = self._update_free_rectangles(
                    free_rects, x, y, width, height, kerf
                )
                free_rects.clear()
                free_rects.extend(new_free_rects)

            else:
                # Create new bin
                bin_packing = BinPacking(
                    bin_id=len(bins),
                    bin_type=bin_type,
                    items=[]
                )
                free_rects = [FreeRectangle(0, 0, bin_type.width, bin_type.height)]
                placed_rects = []

                placement, contact_score = self._find_best_placement_in_bin(
                    item, free_rects, placed_rects, bin_type, kerf
                )

                if placement:
                    x, y, width, height, rotated, _ = placement

                    placed_item = PlacedItem(
                        item=item,
                        x=x,
                        y=y,
                        width=width,
                        height=height,
                        rotated=rotated
                    )
                    bin_packing.items.append(placed_item)
                    placed_rects.append(placed_item)

                    new_free_rects = self._update_free_rectangles(
                        free_rects, x, y, width, height, kerf
                    )

                    bins.append((bin_packing, new_free_rects, placed_rects))
                else:
                    unpacked.append(item)

        final_bins = [bp for bp, _, _ in bins]
        return final_bins, unpacked

    def _find_best_placement_in_bin(
        self,
        item: Item,
        free_rects: List[FreeRectangle],
        placed_rects: List[PlacedItem],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[Optional[Tuple[float, float, float, float, bool, int]], int]:
        """
        Find best placement using Contact Point scoring.

        Returns:
            (placement tuple, contact_score)
        """
        best_placement = None
        best_contact_score = -1

        # Try both orientations
        orientations = [
            (item.width, item.height, False),
            (item.height, item.width, True),
        ]

        for width, height, rotated in orientations:
            for free_rect in free_rects:
                if free_rect.can_fit(width, height):
                    x = free_rect.x
                    y = free_rect.y

                    # Calculate contact score
                    contact_score = self._calculate_contact_score(
                        x, y, width, height, placed_rects, bin_type
                    )

                    if contact_score > best_contact_score:
                        best_contact_score = contact_score
                        best_placement = (x, y, width, height, rotated, 0)

        return best_placement, best_contact_score

    def _calculate_contact_score(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        placed_rects: List[PlacedItem],
        bin_type: Bin
    ) -> int:
        """
        Calculate contact score for a placement.

        Contact score = total length of edges touching other rectangles or bin edges.
        """
        score = 0

        # Contact with bin edges
        if x == 0:  # Left edge
            score += height
        if y == 0:  # Bottom edge
            score += width
        if x + width >= bin_type.width - 0.1:  # Right edge
            score += height
        if y + height >= bin_type.height - 0.1:  # Top edge
            score += width

        # Contact with other rectangles
        for placed in placed_rects:
            # Check if rectangles are adjacent
            # Right edge of new rect touches left edge of placed rect
            if abs((x + width) - placed.x) < 0.1:
                overlap = min(y + height, placed.y + placed.height) - max(y, placed.y)
                if overlap > 0:
                    score += overlap

            # Left edge of new rect touches right edge of placed rect
            if abs(x - (placed.x + placed.width)) < 0.1:
                overlap = min(y + height, placed.y + placed.height) - max(y, placed.y)
                if overlap > 0:
                    score += overlap

            # Top edge of new rect touches bottom edge of placed rect
            if abs((y + height) - placed.y) < 0.1:
                overlap = min(x + width, placed.x + placed.width) - max(x, placed.x)
                if overlap > 0:
                    score += overlap

            # Bottom edge of new rect touches top edge of placed rect
            if abs(y - (placed.y + placed.height)) < 0.1:
                overlap = min(x + width, placed.x + placed.width) - max(x, placed.x)
                if overlap > 0:
                    score += overlap

        return score

    def _update_free_rectangles(
        self,
        free_rects: List[FreeRectangle],
        x: float,
        y: float,
        width: float,
        height: float,
        kerf: float
    ) -> List[FreeRectangle]:
        """Update free rectangles after placing an item."""
        new_free_rects = []

        for rect in free_rects:
            # Check if this free rect intersects with the placed item
            if not (x >= rect.x + rect.width or
                    x + width <= rect.x or
                    y >= rect.y + rect.height or
                    y + height <= rect.y):
                # Split the free rectangle
                # Left portion
                if rect.x < x:
                    new_free_rects.append(FreeRectangle(
                        rect.x, rect.y, x - rect.x, rect.height
                    ))

                # Right portion
                if rect.x + rect.width > x + width:
                    new_free_rects.append(FreeRectangle(
                        x + width, rect.y, rect.x + rect.width - (x + width), rect.height
                    ))

                # Bottom portion
                if rect.y < y:
                    new_free_rects.append(FreeRectangle(
                        rect.x, rect.y, rect.width, y - rect.y
                    ))

                # Top portion
                if rect.y + rect.height > y + height:
                    new_free_rects.append(FreeRectangle(
                        rect.x, y + height, rect.width, rect.y + rect.height - (y + height)
                    ))
            else:
                # No intersection, keep the rectangle
                new_free_rects.append(rect)

        # Remove redundant rectangles (contained within others)
        final_rects = []
        for i, rect1 in enumerate(new_free_rects):
            is_contained = False
            for j, rect2 in enumerate(new_free_rects):
                if i != j and self._is_contained(rect1, rect2):
                    is_contained = True
                    break
            if not is_contained:
                final_rects.append(rect1)

        return final_rects

    def _is_contained(self, rect1: FreeRectangle, rect2: FreeRectangle) -> bool:
        """Check if rect1 is contained within rect2."""
        return (rect1.x >= rect2.x and
                rect1.y >= rect2.y and
                rect1.x + rect1.width <= rect2.x + rect2.width and
                rect1.y + rect1.height <= rect2.y + rect2.height)
