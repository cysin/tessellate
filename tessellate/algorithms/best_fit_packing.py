"""
Best-Fit Decreasing packing with multiple sorting strategies.

Inspired by rectpack's BBF (Bin Best Fit) strategy and various sorting methods.
"""

import time
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.algorithms.skyline import SkylinePacker, SkylineSegment
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class BestFitDecreasingPacker(PackingAlgorithm):
    """
    Best-Fit Decreasing strategy: tries to place each item in the bin
    where it fits best (tightest fit), minimizing wasted space.

    Key difference from First-Fit: evaluates ALL open bins and chooses
    the one with least wasted space after placement.
    """

    def __init__(self, time_limit: float = 30.0, sort_by: str = "long_side"):
        """
        Initialize packer.

        Args:
            time_limit: Maximum execution time
            sort_by: Sorting strategy - "long_side", "area", "short_side", "ratio"
        """
        super().__init__(time_limit)
        self.sort_by = sort_by

    def get_name(self) -> str:
        return f"BestFit-{self.sort_by}"

    def solve(self, problem: Problem) -> Solution:
        """Solve using best-fit decreasing strategy."""
        start_time = time.time()

        # Try multiple sorting strategies
        sort_strategies = {
            "long_side": lambda item: (-max(item.width, item.height), -min(item.width, item.height)),
            "area": lambda item: (-item.area(), -max(item.width, item.height)),
            "short_side": lambda item: (-min(item.width, item.height), -max(item.width, item.height)),
            "ratio": lambda item: (-max(item.width, item.height) / min(item.width, item.height) if min(item.width, item.height) > 0 else 0, -item.area()),
            "perimeter": lambda item: (-(item.width + item.height), -item.area()),
        }

        best_solution = None
        best_bins = float('inf')

        for strategy_name, sort_key in sort_strategies.items():
            if time.time() - start_time > self.time_limit * 0.9:
                break

            solution = self._solve_with_sorting(problem, sort_key, strategy_name)

            if solution.num_bins() < best_bins:
                best_bins = solution.num_bins()
                best_solution = solution
                best_solution.metadata["sort_strategy"] = strategy_name

        execution_time = time.time() - start_time
        if best_solution:
            best_solution.metadata["algorithm"] = self.get_name()
            best_solution.metadata["execution_time"] = execution_time

        return best_solution if best_solution else Solution()

    def _solve_with_sorting(
        self,
        problem: Problem,
        sort_key,
        strategy_name: str
    ) -> Solution:
        """Solve with specific sorting strategy."""
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

            # Expand and sort items
            items_to_pack = []
            for item in group_items:
                for _ in range(item.quantity):
                    items_to_pack.append(item)

            items_to_pack.sort(key=sort_key)

            # Pack using best-fit
            bins, unpacked = self._pack_best_fit(
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

        return solution

    def _pack_best_fit(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], List[Item]]:
        """
        Pack items using best-fit strategy.

        For each item:
        1. Try to place in ALL existing bins
        2. Calculate waste for each placement
        3. Choose bin with MINIMUM waste
        4. If doesn't fit anywhere, open new bin
        """
        bins: List[Tuple[BinPacking, List[SkylineSegment]]] = []
        unpacked_items = []

        for item in items:
            best_bin_idx = None
            best_placement = None
            best_waste = float('inf')

            # Try all existing bins
            for idx, (bin_packing, skyline) in enumerate(bins):
                placement = self._try_place_item(
                    item, skyline, bin_type, kerf
                )

                if placement:
                    x, y, width, height, rotated = placement

                    # Calculate waste for this placement
                    waste = self._calculate_waste(skyline, x, y, width, height)

                    # Best-fit: choose bin with minimum waste
                    if waste < best_waste:
                        best_waste = waste
                        best_bin_idx = idx
                        best_placement = placement

            # Place in best bin if found
            if best_bin_idx is not None:
                bin_packing, skyline = bins[best_bin_idx]
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

                # Update skyline
                new_skyline = self._update_skyline(
                    skyline, x, y, width, height, kerf
                )
                skyline.clear()
                skyline.extend(new_skyline)

            else:
                # No bin fits, create new bin
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
                else:
                    unpacked_items.append(item)

        final_bins = [bp for bp, _ in bins]
        return final_bins, unpacked_items

    def _try_place_item(
        self,
        item: Item,
        skyline: List[SkylineSegment],
        bin_type: Bin,
        kerf: float
    ) -> Optional[Tuple[float, float, float, float, bool]]:
        """Try to place item using skyline."""
        best_score = float('inf')
        best_placement = None

        # Try both orientations
        orientations = [
            (item.width, item.height, False),
            (item.height, item.width, True),
        ]

        for width, height, rotated in orientations:
            for seg_idx, segment in enumerate(skyline):
                x = segment.x

                y, fits = self._find_skyline_height(
                    skyline, seg_idx, x, width, height, bin_type, kerf
                )

                if fits:
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
