"""
First-Fit Decreasing with aggressive bin filling.

This algorithm focuses on filling bins as much as possible before
opening new ones, which often leads to fewer total bins.
"""

import time
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.algorithms.skyline import SkylinePacker, SkylineSegment
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class FirstFitDecreasingPacker(PackingAlgorithm):
    """
    First-Fit Decreasing with Skyline-based placement.

    Key differences from standard approach:
    - Sorts items by area (largest first)
    - Tries to place each item in ALL existing bins before opening a new one
    - Uses Skyline algorithm for efficient space management within each bin
    """

    def __init__(self, time_limit: float = 30.0):
        """
        Initialize packer.

        Args:
            time_limit: Maximum execution time
        """
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "FirstFit-Decreasing-Skyline"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using first-fit decreasing strategy.

        Args:
            problem: Problem instance

        Returns:
            Solution
        """
        start_time = time.time()
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

            # Create item list with quantities (expanded)
            items_to_pack = []
            for item in group_items:
                for _ in range(item.quantity):
                    items_to_pack.append(item)

            # Sort by area (largest first) - this is the "Decreasing" part
            items_to_pack.sort(key=lambda item: (-item.area(), -max(item.width, item.height)))

            # Pack using first-fit strategy
            bins, unpacked = self._pack_first_fit(
                items_to_pack, bin_type, problem.kerf
            )

            # Add to solution
            for bin_packing in bins:
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

            # Track unplaced
            if unpacked:
                unplaced_counts = {}
                for item in unpacked:
                    unplaced_counts[item.id] = unplaced_counts.get(item.id, 0) + 1

                for item in group_items:
                    if item.id in unplaced_counts:
                        solution.unplaced.append((item, unplaced_counts[item.id]))

        # Add metadata
        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution

    def _pack_first_fit(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], List[Item]]:
        """
        Pack items using first-fit strategy.

        For each item, try to place it in an existing bin.
        Only open a new bin if it doesn't fit in any existing bin.

        Args:
            items: Items to pack (should be sorted)
            bin_type: Bin type
            kerf: Kerf width

        Returns:
            Tuple of (bins, unpacked items)
        """
        bins: List[Tuple[BinPacking, List[SkylineSegment]]] = []
        unpacked_items = []

        for item in items:
            placed = False

            # Try to place in existing bins (first-fit)
            for bin_packing, skyline in bins:
                placement = self._try_place_item(
                    item, skyline, bin_type, kerf
                )

                if placement:
                    x, y, width, height, rotated = placement

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

                    # Update skyline
                    new_skyline = self._update_skyline(
                        skyline, x, y, width, height, kerf
                    )
                    # Replace skyline in place
                    skyline.clear()
                    skyline.extend(new_skyline)

                    placed = True
                    break

            # If not placed in any existing bin, open a new one
            if not placed:
                bin_packing = BinPacking(
                    bin_id=len(bins),
                    bin_type=bin_type,
                    items=[]
                )
                skyline = [SkylineSegment(0, 0, bin_type.width)]

                placement = self._try_place_item(
                    item, skyline, bin_type, kerf
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

                    new_skyline = self._update_skyline(
                        skyline, x, y, width, height, kerf
                    )

                    bins.append((bin_packing, new_skyline))
                    placed = True

            if not placed:
                unpacked_items.append(item)

        # Extract just the bin packings
        final_bins = [bp for bp, _ in bins]
        return final_bins, unpacked_items

    def _try_place_item(
        self,
        item: Item,
        skyline: List[SkylineSegment],
        bin_type: Bin,
        kerf: float
    ) -> Optional[Tuple[float, float, float, float, bool]]:
        """
        Try to place item in bin using skyline.

        Returns best placement if found, None otherwise.
        """
        best_score = float('inf')
        best_placement = None

        # Try both orientations
        orientations = [
            (item.width, item.height, False),
            (item.height, item.width, True),
        ]

        for width, height, rotated in orientations:
            # Try each skyline segment
            for seg_idx, segment in enumerate(skyline):
                x = segment.x

                # Find height needed
                y, fits = self._find_skyline_height(
                    skyline, seg_idx, x, width, height, bin_type, kerf
                )

                if fits:
                    # Use min-waste scoring
                    waste = self._calculate_waste(skyline, x, y, width, height)
                    score = waste

                    if score < best_score:
                        best_score = score
                        best_placement = (x, y, width, height, rotated)

        return best_placement

    def _find_skyline_height(
        self,
        skyline: List[SkylineSegment],
        start_seg_idx: int,
        x: float,
        width: float,
        height: float,
        bin_type: Bin,
        kerf: float
    ) -> Tuple[float, bool]:
        """Find height for placement."""
        max_y = 0
        x_end = x + width

        for segment in skyline[start_seg_idx:]:
            seg_end = segment.x + segment.width

            if segment.x < x_end and seg_end > x:
                max_y = max(max_y, segment.y)

            if seg_end >= x_end:
                break
        else:
            return max_y, False

        if max_y + height + kerf > bin_type.height:
            return max_y, False

        return max_y, True

    def _calculate_waste(
        self,
        skyline: List[SkylineSegment],
        x: float,
        y: float,
        width: float,
        height: float
    ) -> float:
        """Calculate wasted area."""
        waste = 0
        x_end = x + width

        for segment in skyline:
            seg_end = segment.x + segment.width

            if segment.x < x_end and seg_end > x:
                overlap_start = max(segment.x, x)
                overlap_end = min(seg_end, x_end)
                overlap_width = overlap_end - overlap_start

                if segment.y < y:
                    waste += overlap_width * (y - segment.y)

        return waste

    def _update_skyline(
        self,
        skyline: List[SkylineSegment],
        x: float,
        y: float,
        width: float,
        height: float,
        kerf: float
    ) -> List[SkylineSegment]:
        """Update skyline after placement."""
        new_skyline = []
        x_end = x + width
        rect_top = y + height + kerf
        new_segment_added = False

        for segment in skyline:
            seg_end = segment.x + segment.width

            if seg_end <= x:
                new_skyline.append(segment)
                continue

            if segment.x >= x_end:
                if not new_segment_added:
                    new_skyline.append(SkylineSegment(x, rect_top, width))
                    new_segment_added = True
                new_skyline.append(segment)
                continue

            # Overlaps
            if segment.x < x:
                left_width = x - segment.x
                new_skyline.append(
                    SkylineSegment(segment.x, segment.y, left_width)
                )

            if not new_segment_added:
                new_skyline.append(SkylineSegment(x, rect_top, width))
                new_segment_added = True

            if seg_end > x_end:
                right_width = seg_end - x_end
                new_skyline.append(
                    SkylineSegment(x_end, segment.y, right_width)
                )

        if not new_segment_added:
            new_skyline.append(SkylineSegment(x, rect_top, width))

        # Merge adjacent segments at same height
        return self._merge_segments(new_skyline)

    def _merge_segments(
        self,
        skyline: List[SkylineSegment]
    ) -> List[SkylineSegment]:
        """Merge adjacent segments at same height."""
        if not skyline:
            return skyline

        merged = [skyline[0]]

        for segment in skyline[1:]:
            last = merged[-1]

            if (last.x + last.width == segment.x and
                abs(last.y - segment.y) < 1e-6):
                merged[-1] = SkylineSegment(
                    last.x,
                    last.y,
                    last.width + segment.width
                )
            else:
                merged.append(segment)

        return merged
