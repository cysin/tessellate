"""
Skyline Bin Packing Algorithm.

This implements the Skyline packing algorithm as described by
Jukka Jylanki in "A Thousand Ways to Pack the Bin" (2010).

The Skyline algorithm maintains a "skyline" representing the top
contour of placed rectangles and tries to place new rectangles
on top of this skyline.
"""

import time
from typing import List, Tuple, Optional, NamedTuple
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class SkylineSegment(NamedTuple):
    """A segment of the skyline."""
    x: float  # Left x-coordinate
    y: float  # Y-coordinate (height)
    width: float  # Segment width


class SkylinePacker(PackingAlgorithm):
    """
    Skyline Bin Packing Algorithm.

    Features:
    - Bottom-Left and Min-Waste-Fit heuristics
    - Rotation support
    - Efficient skyline-based space management
    """

    def __init__(
        self,
        time_limit: float = 5.0,
        use_min_waste: bool = True
    ):
        """
        Initialize Skyline packer.

        Args:
            time_limit: Maximum execution time
            use_min_waste: Use Min-Waste-Fit heuristic (else Bottom-Left)
        """
        super().__init__(time_limit)
        self.use_min_waste = use_min_waste

    def get_name(self) -> str:
        heuristic = "MinWasteFit" if self.use_min_waste else "BottomLeft"
        return f"Skyline-{heuristic}"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using Skyline packing.

        Args:
            problem: Problem instance

        Returns:
            Solution
        """
        start_time = time.time()

        # Try both heuristics
        best_solution = None
        best_score = (float('inf'), float('inf'))

        heuristics = [True, False]  # Min-Waste-Fit and Bottom-Left

        for use_min_waste in heuristics:
            if time.time() - start_time > self.time_limit * 0.9:
                break

            self.use_min_waste = use_min_waste
            solution = self._solve_once(problem)
            score = (solution.num_bins(), -solution.total_utilization())

            if score < best_score:
                best_score = score
                best_solution = solution
                best_solution.metadata["heuristic"] = (
                    "MinWasteFit" if use_min_waste else "BottomLeft"
                )

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

            # Sort by area (descending) for better packing
            items_to_pack.sort(key=lambda item: -item.area())

            # Pack items
            bins, unpacked_items = self._pack_items_skyline(
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

    def _pack_items_skyline(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], List[Item]]:
        """
        Pack items using Skyline algorithm.

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

            # Initialize skyline with full bin width at bottom
            skyline = [SkylineSegment(0, 0, bin_type.width)]

            # Pack items into this bin
            packed_indices = []

            for i, item in enumerate(remaining_items):
                # Try to place this item
                placement = self._find_placement_skyline(
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
                    packed_indices.append(i)

                    # Update skyline
                    skyline = self._update_skyline(
                        skyline, x, y, width, height, kerf
                    )

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

    def _find_placement_skyline(
        self,
        item: Item,
        skyline: List[SkylineSegment],
        bin_type: Bin,
        kerf: float
    ) -> Optional[Tuple[float, float, float, float, bool]]:
        """
        Find best placement for item using skyline.

        Args:
            item: Item to place
            skyline: Current skyline
            bin_type: Bin type
            kerf: Kerf width

        Returns:
            Tuple of (x, y, width, height, rotated) or None
        """
        best_score = float('inf')
        best_placement = None

        # Try both orientations - even for non-rotatable items
        # we need to try both to find valid placements in the bin
        orientations = [
            (item.width, item.height, False),
            (item.height, item.width, True),
        ]

        for width, height, rotated in orientations:
            # Try placing at each skyline segment
            for seg_idx, segment in enumerate(skyline):
                # Try placing at segment start
                x = segment.x

                # Find the height needed at this position
                y, fits = self._find_skyline_height(
                    skyline, seg_idx, x, width, height, bin_type, kerf
                )

                if fits:
                    # Calculate score based on heuristic
                    if self.use_min_waste:
                        # Min-Waste-Fit: minimize wasted area under rectangle
                        waste = self._calculate_waste(
                            skyline, x, y, width, height
                        )
                        score = waste
                    else:
                        # Bottom-Left: prefer lower placement
                        score = y

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
        """
        Find the height at which item can be placed.

        Args:
            skyline: Current skyline
            start_seg_idx: Starting segment index
            x: X-coordinate to place item
            width: Item width
            height: Item height
            bin_type: Bin type
            kerf: Kerf width

        Returns:
            Tuple of (y-coordinate, fits)
        """
        # Find maximum y across all segments the item spans
        max_y = 0
        x_end = x + width

        for segment in skyline[start_seg_idx:]:
            seg_end = segment.x + segment.width

            # Check if segment overlaps with item's x-range
            if segment.x < x_end and seg_end > x:
                max_y = max(max_y, segment.y)

            # Stop if we've covered the item's width
            if seg_end >= x_end:
                break
        else:
            # Item extends beyond bin width
            return max_y, False

        # Check if item fits vertically (with kerf consideration)
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
        """
        Calculate wasted area below the placed rectangle.

        Args:
            skyline: Current skyline
            x: Rectangle x-coordinate
            y: Rectangle y-coordinate (top of placement)
            width: Rectangle width
            height: Rectangle height

        Returns:
            Wasted area
        """
        waste = 0
        x_end = x + width

        for segment in skyline:
            seg_end = segment.x + segment.width

            # Check if segment overlaps with rectangle
            if segment.x < x_end and seg_end > x:
                # Calculate overlap width
                overlap_start = max(segment.x, x)
                overlap_end = min(seg_end, x_end)
                overlap_width = overlap_end - overlap_start

                # Calculate wasted height
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
        """
        Update skyline after placing a rectangle.

        Args:
            skyline: Current skyline
            x: Rectangle x-coordinate
            y: Rectangle y-coordinate
            width: Rectangle width
            height: Rectangle height
            kerf: Kerf width

        Returns:
            Updated skyline
        """
        new_skyline = []
        x_end = x + width
        rect_top = y + height + kerf

        # Add new segment for the placed rectangle
        new_segment_added = False

        for segment in skyline:
            seg_end = segment.x + segment.width

            # Segment is completely before rectangle
            if seg_end <= x:
                new_skyline.append(segment)
                continue

            # Segment is completely after rectangle
            if segment.x >= x_end:
                # Add rectangle's top segment if not yet added
                if not new_segment_added:
                    new_skyline.append(SkylineSegment(x, rect_top, width))
                    new_segment_added = True
                new_skyline.append(segment)
                continue

            # Segment overlaps with rectangle
            # Split segment if needed

            # Left part (before rectangle)
            if segment.x < x:
                left_width = x - segment.x
                new_skyline.append(
                    SkylineSegment(segment.x, segment.y, left_width)
                )

            # Add rectangle's top segment
            if not new_segment_added:
                new_skyline.append(SkylineSegment(x, rect_top, width))
                new_segment_added = True

            # Right part (after rectangle)
            if seg_end > x_end:
                right_width = seg_end - x_end
                new_skyline.append(
                    SkylineSegment(x_end, segment.y, right_width)
                )

        # If rectangle extends to the end, make sure we added its segment
        if not new_segment_added:
            new_skyline.append(SkylineSegment(x, rect_top, width))

        # Merge adjacent segments at same height
        new_skyline = self._merge_skyline_segments(new_skyline)

        return new_skyline

    def _merge_skyline_segments(
        self,
        skyline: List[SkylineSegment]
    ) -> List[SkylineSegment]:
        """
        Merge adjacent skyline segments at the same height.

        Args:
            skyline: Skyline to merge

        Returns:
            Merged skyline
        """
        if not skyline:
            return skyline

        merged = [skyline[0]]

        for segment in skyline[1:]:
            last = merged[-1]

            # Check if segments are adjacent and at same height
            if (last.x + last.width == segment.x and
                abs(last.y - segment.y) < 1e-6):
                # Merge segments
                merged[-1] = SkylineSegment(
                    last.x,
                    last.y,
                    last.width + segment.width
                )
            else:
                merged.append(segment)

        return merged
