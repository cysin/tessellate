"""
Rotated Strip Packer - specialized for same-dimension items.

When all items have the same dimension (e.g., all 554mm in one direction),
rotating them can allow much better packing.
"""

import time
from typing import List, Tuple
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class RotatedStripPacker(PackingAlgorithm):
    """
    Pack items by rotating them to fit more rows.

    This algorithm is optimized for items that share a common dimension.
    """

    def __init__(self, time_limit: float = 60.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "RotatedStripPacker"

    def solve(self, problem: Problem) -> Solution:
        """Solve by rotating items to optimize row packing."""
        start_time = time.time()

        groups = problem.group_by_material()
        all_bins = []
        all_unplaced = []

        for (thickness, material), group_items in groups.items():
            # Check if items are rotatable and share common dimension
            if not all(item.rotatable for item in group_items):
                # Fall back if not all rotatable
                from tessellate.algorithms.guillotine import GuillotinePacker
                packer = GuillotinePacker(time_limit=self.time_limit)
                temp_problem = Problem(
                    items=group_items,
                    bins=problem.bins,
                    kerf=problem.kerf,
                    time_limit=self.time_limit
                )
                temp_solution = packer.solve(temp_problem)
                all_bins.extend(temp_solution.bins)
                all_unplaced.extend(temp_solution.unplaced)
                continue

            # Get compatible bin
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    all_unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Pack with rotation
            bins = self._pack_rotated(group_items, bin_type, problem.kerf)

            for i, bin_packing in enumerate(bins):
                bin_packing.bin_id = len(all_bins) + i
                all_bins.append(bin_packing)

        solution = Solution(bins=all_bins, unplaced=all_unplaced)
        solution.metadata["algorithm"] = self.get_name()
        solution.metadata["execution_time"] = time.time() - start_time

        return solution

    def _pack_rotated(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> List[BinPacking]:
        """
        Pack items by rotating them 90 degrees.

        Original: width x height (e.g., 336x554, 400x554, etc.)
        Rotated: 554 x variable_height (554x336, 554x400, etc.)
        """
        # Create rotated item list
        rotated_items = []
        for item in items:
            for _ in range(item.quantity):
                rotated_items.append(item)

        # After rotation: all items have width=554, heights vary (336-864)
        # Sort by rotated height (original width) to pack smaller heights together
        rotated_items.sort(key=lambda x: x.width)  # width becomes height after rotation

        bins = []

        iteration = 0
        max_iterations = 1000  # Safety limit
        while rotated_items and iteration < max_iterations:
            iteration += 1
            if iteration % 10 == 0:
                print(f"    Iteration {iteration}, {len(rotated_items)} items remaining, {len(bins)} bins created")

            # Create new bin
            bin_packing = BinPacking(bin_id=len(bins), bin_type=bin_type, items=[])

            # Pack items into this bin using rows
            # Each row has different height (the rotated height)
            y = 0
            row_items = []
            items_packed_this_bin = 0

            while rotated_items and y < bin_type.height:
                # Start new row
                row_height = rotated_items[0].width  # rotated height
                x = 0

                # Pack items with same rotated height in this row
                row_packed = []
                for item in rotated_items[:]:
                    # Check if item has same rotated height and fits in row
                    if item.width == row_height:  # same rotated height
                        # After rotation: width=554, height=item.width
                        item_width_rotated = item.height  # 554mm
                        item_height_rotated = item.width  # original width

                        if y + item_height_rotated + (kerf if row_items else 0) <= bin_type.height:
                            if x + item_width_rotated <= bin_type.width:
                                # Place item (rotated)
                                placed = PlacedItem(
                                    item=item,
                                    x=x,
                                    y=y,
                                    width=item_width_rotated,
                                    height=item_height_rotated,
                                    rotated=True  # Mark as rotated
                                )
                                bin_packing.items.append(placed)
                                row_packed.append(item)
                                row_items.append(item)
                                items_packed_this_bin += 1
                                x += item_width_rotated + kerf
                            else:
                                break

                # Remove packed items
                for item in row_packed:
                    rotated_items.remove(item)

                # Move to next row
                if row_packed:
                    y += row_height + kerf
                else:
                    # Couldn't pack any more items, finish this bin
                    break

            if bin_packing.items:
                bins.append(bin_packing)
                print(f"    Bin {len(bins)}: packed {items_packed_this_bin} items, utilization={bin_packing.utilization():.2%}")
            else:
                # Couldn't pack any items, stop to avoid infinite loop
                print(f"    Warning: Could not pack any items in bin, {len(rotated_items)} items remaining")
                break

        return bins
