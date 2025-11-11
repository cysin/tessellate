"""
Row-based packing strategy optimized for items with common dimension.

This strategy is particularly effective when items share a common dimension
(e.g., all items are X×554mm) and can be packed in horizontal rows.
"""

import time
from typing import List, Tuple
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class RowPacker(PackingAlgorithm):
    """
    Row-based packing that packs items in horizontal rows.

    Particularly effective when all items share a common dimension.
    """

    def __init__(self, time_limit: float = 30.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "Row-Based-Packer"

    def solve(self, problem: Problem) -> Solution:
        """Solve using row-based packing."""
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

            # Expand items by quantity
            items_to_pack = []
            for item in group_items:
                for _ in range(item.quantity):
                    items_to_pack.append(item)

            # Sort by longer dimension (descending)
            items_to_pack.sort(key=lambda x: -max(x.width, x.height))

            # Pack using row strategy
            bins, unpacked = self._pack_rows(
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

    def _pack_rows(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], List[Item]]:
        """
        Pack items using row-based strategy.

        Strategy:
        1. For each bin, pack items in horizontal rows
        2. Each row uses the SHORT dimension as height
        3. Fill row width with multiple items
        4. Move to next row when current row is full
        """
        bins = []
        unpacked = []

        current_bin = None
        current_y = 0
        current_row_items = []
        current_row_width = 0
        current_row_height = 0

        for item in items:
            # Determine orientation: use shorter dimension as row height
            short_dim = min(item.width, item.height)
            long_dim = max(item.width, item.height)

            # Determine actual placement dimensions
            # We want short dimension to be the ROW HEIGHT for efficiency
            if item.width == short_dim:
                # Item is already oriented correctly (width is short)
                place_width = long_dim
                place_height = short_dim
                rotated = True
            else:
                # Need to rotate
                place_width = short_dim
                place_height = long_dim
                rotated = False

            # Check if we need a new bin
            if current_bin is None:
                current_bin = BinPacking(
                    bin_id=len(bins),
                    bin_type=bin_type,
                    items=[]
                )
                current_y = 0
                current_row_width = 0
                current_row_height = place_height

            # Try to add to current row
            if current_row_width + place_width + (kerf if current_row_width > 0 else 0) <= bin_type.width:
                # Fits in current row
                x = current_row_width + (kerf if current_row_width > 0 else 0)

                placed = PlacedItem(
                    item=item,
                    x=x,
                    y=current_y,
                    width=place_width,
                    height=place_height,
                    rotated=rotated
                )
                current_bin.items.append(placed)
                current_row_items.append(placed)

                current_row_width = x + place_width
                current_row_height = max(current_row_height, place_height)

            else:
                # Doesn't fit in current row, try next row
                next_y = current_y + current_row_height + kerf

                if next_y + place_height <= bin_type.height:
                    # Fits in next row
                    current_y = next_y
                    current_row_width = place_width
                    current_row_height = place_height
                    current_row_items = []

                    placed = PlacedItem(
                        item=item,
                        x=0,
                        y=current_y,
                        width=place_width,
                        height=place_height,
                        rotated=rotated
                    )
                    current_bin.items.append(placed)
                    current_row_items.append(placed)

                else:
                    # Doesn't fit in this bin, need a new bin
                    bins.append(current_bin)

                    # Start new bin
                    current_bin = BinPacking(
                        bin_id=len(bins),
                        bin_type=bin_type,
                        items=[]
                    )
                    current_y = 0
                    current_row_width = place_width
                    current_row_height = place_height
                    current_row_items = []

                    placed = PlacedItem(
                        item=item,
                        x=0,
                        y=0,
                        width=place_width,
                        height=place_height,
                        rotated=rotated
                    )
                    current_bin.items.append(placed)
                    current_row_items.append(placed)

        # Add last bin
        if current_bin and current_bin.items:
            bins.append(current_bin)

        return bins, unpacked
