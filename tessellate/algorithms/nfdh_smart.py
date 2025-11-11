"""
Smart NFDH Packer - orientation selection based on bin aspect ratio.

Unlike traditional NFDH that always maximizes height, this variant:
1. Analyzes bin aspect ratio (portrait vs landscape)
2. Chooses orientations that align with bin shape
3. Sorts by height, then width for better strip packing
"""

import time
from typing import List
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class SmartNFDHPacker(PackingAlgorithm):
    """
    Smart NFDH with aspect-ratio-aware orientation selection.

    For landscape bins (width > height), prefers landscape items.
    This avoids the pitfall of rotating all items to tall orientations.
    """

    def __init__(self, time_limit: float = 5.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "NFDH-Smart"

    def solve(self, problem: Problem) -> Solution:
        """Solve using smart NFDH."""

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

            bins = self._pack_smart_nfdh(
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

    def _pack_smart_nfdh(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack using smart NFDH with aspect-ratio-aware orientation.
        """

        bin_width = bin_type.width
        bin_height = bin_type.height

        # Determine bin's preferred orientation
        bin_is_landscape = bin_width > bin_height

        # Prepare items with smart orientation selection
        prepared_items = []
        for item in items:
            orientations = [
                (item.width, item.height, False),
                (item.height, item.width, True),
            ]

            # Filter orientations that fit
            valid = [(w, h, r) for w, h, r in orientations if w <= bin_width and h <= bin_height]

            if not valid:
                continue

            # Smart selection: prefer orientation matching bin aspect ratio
            if bin_is_landscape:
                # For landscape bins, prefer landscape items (width > height)
                # This keeps strips short and allows more items per strip
                best = max(valid, key=lambda x: (x[0] - x[1], x[0]))
            else:
                # For portrait bins, prefer portrait items
                best = max(valid, key=lambda x: (x[1] - x[0], x[1]))

            width, height, rotated = best

            prepared_items.append({
                'item': item,
                'width': width,
                'height': height,
                'rotated': rotated
            })

        # Sort by height descending (NFDH), then by width descending
        prepared_items.sort(key=lambda x: (x['height'], x['width']), reverse=True)

        # Pack into bins using shelf algorithm
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
