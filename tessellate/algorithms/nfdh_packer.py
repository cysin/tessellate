"""
NFDH (Next Fit Decreasing Height) Packer.

This is a shelf-based packing algorithm inspired by the gomory implementation:
https://github.com/rmzlb/gomory

Strategy:
1. Sort items by height (descending)
2. Pack items into horizontal strips/shelves
3. Each strip has the height of the tallest item
4. Items are packed left-to-right within each strip
5. When a strip is full, move to the next strip below
"""

import time
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class NFDHPacker(PackingAlgorithm):
    """
    Next Fit Decreasing Height packer.

    A shelf-based algorithm that:
    - Sorts items by height (largest first)
    - Packs items into horizontal strips
    - Each strip height = tallest item in that strip
    """

    def __init__(self, time_limit: float = 5.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "NFDH"

    def solve(self, problem: Problem) -> Solution:
        """Solve using NFDH shelf packing."""

        start_time = time.time()

        # Group by material/thickness
        groups = problem.group_by_material()

        solution = Solution()

        for (thickness, material), group_items in groups.items():
            # Get compatible bins
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Expand items by quantity
            items_list = []
            for item in group_items:
                for q in range(item.quantity):
                    items_list.append(item)

            # Pack using NFDH
            bins = self._pack_nfdh(
                items_list, bin_type, problem.kerf, start_time
            )

            for bin_packing in bins:
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution

    def _pack_nfdh(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack items using NFDH algorithm.

        Steps:
        1. Determine best orientation for each item (maximize height)
        2. Sort by height descending
        3. Pack into strips shelf-by-shelf
        """

        bin_width = bin_type.width
        bin_height = bin_type.height

        # Prepare items with best orientation
        prepared_items = []
        for item in items:
            # Try both orientations
            orientations = [
                (item.width, item.height, False),
                (item.height, item.width, True),
            ]

            # Filter orientations that fit in bin width
            valid = [(w, h, r) for w, h, r in orientations if w <= bin_width]

            if not valid:
                # Item doesn't fit
                continue

            # Pick orientation that maximizes height (NFDH strategy)
            # But if heights are similar, prefer the orientation that uses less width
            best = max(valid, key=lambda x: (x[1], -x[0]))
            width, height, rotated = best

            prepared_items.append({
                'item': item,
                'width': width,
                'height': height,
                'rotated': rotated
            })

        # Sort by height descending, then by width descending (NFDH)
        # Secondary sort by width helps pack wider items first in each strip
        prepared_items.sort(key=lambda x: (x['height'], x['width']), reverse=True)

        # Pack into bins using shelf algorithm
        bins = []
        current_bin_index = 0

        while prepared_items:
            if time.time() - start_time > self.time_limit:
                break

            # Create new bin
            bin_packing = BinPacking(
                bin_id=current_bin_index,
                bin_type=bin_type,
                items=[]
            )

            current_y = 0

            # Pack items into this bin using strips
            while prepared_items and current_y < bin_height:
                # Start a new strip with the tallest remaining item
                strip_height = prepared_items[0]['height']

                # Check if strip fits
                if current_y + strip_height > bin_height:
                    break

                # Pack items into this strip (left to right)
                current_x = 0
                i = 0

                while i < len(prepared_items):
                    item_data = prepared_items[i]

                    # Check if item height fits in current strip
                    if item_data['height'] <= strip_height:
                        piece_width = item_data['width']

                        # Calculate needed width (add kerf if not first item)
                        needed_width = piece_width if current_x == 0 else piece_width + kerf

                        # Check if item fits horizontally
                        if current_x + needed_width <= bin_width:
                            # Place item
                            x = current_x if current_x == 0 else current_x + kerf

                            placed_item = PlacedItem(
                                item=item_data['item'],
                                x=x,
                                y=current_y,
                                width=item_data['width'],
                                height=item_data['height'],
                                rotated=item_data['rotated']
                            )

                            bin_packing.items.append(placed_item)
                            current_x = x + piece_width

                            # Remove item from list
                            prepared_items.pop(i)
                        else:
                            i += 1
                    else:
                        i += 1

                # If we placed at least one item in this strip, move to next strip
                if current_x > 0:
                    current_y += strip_height + kerf
                else:
                    # No items fit in this strip, stop trying to fill this bin
                    break

            # Add bin if it has items
            if bin_packing.items:
                bins.append(bin_packing)
                current_bin_index += 1
            else:
                # No more items can fit, stop
                break

        return bins


class NFDHDecreasingArea(PackingAlgorithm):
    """
    NFDH variant that sorts by area instead of height.

    This can sometimes give better results for items with varying aspect ratios.
    """

    def __init__(self, time_limit: float = 5.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "NFDH-Area"

    def solve(self, problem: Problem) -> Solution:
        """Solve using NFDH with area-based sorting."""

        start_time = time.time()

        groups = problem.group_by_material()
        solution = Solution()

        for (thickness, material), group_items in groups.items():
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            items_list = []
            for item in group_items:
                for q in range(item.quantity):
                    items_list.append(item)

            bins = self._pack_nfdh_area(
                items_list, bin_type, problem.kerf, start_time
            )

            for bin_packing in bins:
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution

    def _pack_nfdh_area(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """Pack using NFDH with area-based sorting."""

        bin_width = bin_type.width
        bin_height = bin_type.height

        # Prepare items with best orientation (maximize height)
        prepared_items = []
        for item in items:
            orientations = [
                (item.width, item.height, False),
                (item.height, item.width, True),
            ]

            valid = [(w, h, r) for w, h, r in orientations if w <= bin_width]
            if not valid:
                continue

            best = max(valid, key=lambda x: x[1])
            width, height, rotated = best

            prepared_items.append({
                'item': item,
                'width': width,
                'height': height,
                'rotated': rotated,
                'area': width * height
            })

        # Sort by area descending (variant)
        prepared_items.sort(key=lambda x: (x['area'], x['height']), reverse=True)

        # Pack into bins (same algorithm as NFDH)
        bins = []
        current_bin_index = 0

        while prepared_items:
            if time.time() - start_time > self.time_limit:
                break

            bin_packing = BinPacking(
                bin_id=current_bin_index,
                bin_type=bin_type,
                items=[]
            )

            current_y = 0

            while prepared_items and current_y < bin_height:
                strip_height = prepared_items[0]['height']

                if current_y + strip_height > bin_height:
                    break

                current_x = 0
                i = 0

                while i < len(prepared_items):
                    item_data = prepared_items[i]

                    if item_data['height'] <= strip_height:
                        piece_width = item_data['width']
                        needed_width = piece_width if current_x == 0 else piece_width + kerf

                        if current_x + needed_width <= bin_width:
                            x = current_x if current_x == 0 else current_x + kerf

                            placed_item = PlacedItem(
                                item=item_data['item'],
                                x=x,
                                y=current_y,
                                width=item_data['width'],
                                height=item_data['height'],
                                rotated=item_data['rotated']
                            )

                            bin_packing.items.append(placed_item)
                            current_x = x + piece_width
                            prepared_items.pop(i)
                        else:
                            i += 1
                    else:
                        i += 1

                if current_x > 0:
                    current_y += strip_height + kerf
                else:
                    break

            if bin_packing.items:
                bins.append(bin_packing)
                current_bin_index += 1
            else:
                break

        return bins
