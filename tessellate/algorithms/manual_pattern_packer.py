"""
Manual Pattern Packer - Replicates the manual1.jpg solution strategy.

Key insights from manual solution:
1. All items have uniform height (554mm)
2. Items vary only by width (336-864mm)
3. Bin fits exactly 2 horizontal strips (2 × 554mm ≈ 1220mm)
4. Two-column layout: Right column for most common item (736mm)
5. Pack horizontally in strips, left to right

This algorithm specifically optimizes for items with uniform height.
"""

import time
from typing import List, Tuple, Optional, Dict
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class ManualPatternPacker(PackingAlgorithm):
    """
    Packer that replicates the manual1.jpg solution strategy.

    Optimized for items with uniform height, uses horizontal strip packing
    with strategic column allocation.
    """

    def __init__(self, time_limit: float = 5.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "Manual-Pattern"

    def solve(self, problem: Problem) -> Solution:
        """Solve using manual pattern strategy."""

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

            # Check if items have uniform height (key assumption)
            heights = set(item.height for item in group_items)
            if len(heights) == 1:
                # Items have uniform height - use manual pattern
                bins = self._pack_uniform_height_pattern(
                    group_items, bin_type, problem.kerf, start_time
                )
            else:
                # Fallback to NFDH for non-uniform heights
                print(f"Warning: Items don't have uniform height, using fallback")
                bins = self._pack_fallback(group_items, bin_type, problem.kerf, start_time)

            for bin_packing in bins:
                bin_packing.bin_id = len(solution.bins)
                solution.bins.append(bin_packing)

        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution

    def _pack_uniform_height_pattern(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack items with uniform height using manual pattern strategy.

        Strategy:
        1. All items have uniform height - pack into horizontal strips
        2. Use bin packing algorithm (FFD or similar) to pack strips optimally
        3. Minimize number of strips, then pack strips into bins
        """

        bin_width = bin_type.width
        bin_height = bin_type.height

        # Get uniform height
        uniform_height = items[0].height
        strips_per_bin = int((bin_height + kerf) / (uniform_height + kerf))

        print(f"Manual Pattern: Uniform height={uniform_height}mm, "
              f"{strips_per_bin} strips per bin")

        # Prepare all items - use as-is (they're already in correct orientation)
        prepared_items = []
        for item in items:
            # Use items as-is - NO rotation
            width, height, rotated = item.width, item.height, False

            for q in range(item.quantity):
                prepared_items.append({
                    'item': item,
                    'width': width,
                    'height': height,
                    'rotated': rotated
                })

        # Sort by width descending for better packing
        prepared_items.sort(key=lambda x: x['width'], reverse=True)

        print(f"  Total items to pack: {len(prepared_items)}")
        print(f"  Item widths range: {prepared_items[-1]['width']}mm - {prepared_items[0]['width']}mm")

        # Try multiple packing strategies and pick the best
        strategies = [
            ('First-Fit-Decreasing', self._pack_ffd_strips),
            ('Best-Fit-Decreasing', self._pack_bfd_strips),
            ('Optimized-Mix', self._pack_optimized_mix),
        ]

        best_bins = None
        best_count = float('inf')

        for strategy_name, strategy_func in strategies:
            bins = strategy_func(
                prepared_items.copy(), bin_type, kerf, uniform_height,
                strips_per_bin, start_time
            )
            if bins:
                print(f"    {strategy_name}: {len(bins)} bins")
                if len(bins) < best_count:
                    best_bins = bins
                    best_count = len(bins)

        print(f"    Best: {best_count} bins")
        return best_bins if best_bins else []

    def _pack_ffd_strips(
        self,
        prepared_items: List[Dict],
        bin_type: Bin,
        kerf: float,
        strip_height: float,
        strips_per_bin: int,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack using First-Fit-Decreasing into strips.
        Items are already sorted by width descending.
        """
        bin_width = bin_type.width

        # Pack items into strips using FFD
        strips = []  # Each strip: {'items': [...], 'space_used': width}

        for item_data in prepared_items:
            item_width = item_data['width']
            placed = False

            # Try to fit in first strip with enough space
            for strip in strips:
                space_available = bin_width - strip['space_used']
                needed_space = item_width if strip['space_used'] == 0 else item_width + kerf

                if needed_space <= space_available:
                    strip['items'].append(item_data)
                    strip['space_used'] += needed_space
                    placed = True
                    break

            # Create new strip if needed
            if not placed:
                strips.append({'items': [item_data], 'space_used': item_width})

        # Pack strips into bins
        return self._pack_strips_into_bins(strips, bin_type, strip_height, strips_per_bin, kerf)

    def _pack_bfd_strips(
        self,
        prepared_items: List[Dict],
        bin_type: Bin,
        kerf: float,
        strip_height: float,
        strips_per_bin: int,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack using Best-Fit-Decreasing into strips.
        Items are already sorted by width descending.
        """
        bin_width = bin_type.width

        # Pack items into strips using BFD
        strips = []  # Each strip: {'items': [...], 'space_used': width}

        for item_data in prepared_items:
            item_width = item_data['width']

            # Find best-fit strip (minimum remaining space after placing)
            best_strip_idx = -1
            best_remaining_space = float('inf')

            for idx, strip in enumerate(strips):
                space_available = bin_width - strip['space_used']
                needed_space = item_width if strip['space_used'] == 0 else item_width + kerf

                if needed_space <= space_available:
                    remaining_after = space_available - needed_space
                    if remaining_after < best_remaining_space:
                        best_remaining_space = remaining_after
                        best_strip_idx = idx

            # Place in best strip or create new strip
            if best_strip_idx >= 0:
                strip = strips[best_strip_idx]
                needed_space = item_width if strip['space_used'] == 0 else item_width + kerf
                strip['items'].append(item_data)
                strip['space_used'] += needed_space
            else:
                strips.append({'items': [item_data], 'space_used': item_width})

        # Pack strips into bins
        return self._pack_strips_into_bins(strips, bin_type, strip_height, strips_per_bin, kerf)

    def _pack_optimized_mix(
        self,
        prepared_items: List[Dict],
        bin_type: Bin,
        kerf: float,
        strip_height: float,
        strips_per_bin: int,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack using optimized item mixing to minimize strips.

        Strategy: Try to find good combinations of items that fill strips better
        by mixing different size categories.
        """
        bin_width = bin_type.width

        # Group items by size
        large_items = [pi for pi in prepared_items if pi['width'] >= 700]
        medium_items = [pi for pi in prepared_items if 500 <= pi['width'] < 700]
        small_items = [pi for pi in prepared_items if pi['width'] < 500]

        # Sort each group by width descending
        large_items.sort(key=lambda x: x['width'], reverse=True)
        medium_items.sort(key=lambda x: x['width'], reverse=True)
        small_items.sort(key=lambda x: x['width'], reverse=True)

        strips = []

        # Try to create good mixed combinations
        while large_items or medium_items or small_items:
            current_strip = {'items': [], 'space_used': 0}

            # Strategy 1: Try large + large + small combinations
            if len(large_items) >= 2 and small_items:
                # Try: large + large + small
                test_width = large_items[0]['width'] + kerf + large_items[1]['width']
                remaining = bin_width - test_width

                # Find best fitting small item
                best_small_idx = -1
                for idx, small in enumerate(small_items):
                    needed = small['width'] + kerf
                    if needed <= remaining:
                        best_small_idx = idx
                        break

                if best_small_idx >= 0:
                    current_strip['items'].append(large_items.pop(0))
                    current_strip['items'].append(large_items.pop(0))
                    current_strip['items'].append(small_items.pop(best_small_idx))
                    current_strip['space_used'] = sum(item['width'] for item in current_strip['items']) + kerf * 2
                    strips.append(current_strip)
                    continue

            # Strategy 2: Try large + medium + small combinations
            if large_items and medium_items and small_items:
                # Try: large + medium + small
                test_width = large_items[0]['width'] + kerf + medium_items[0]['width']
                remaining = bin_width - test_width

                # Find best fitting small item
                best_small_idx = -1
                for idx, small in enumerate(small_items):
                    needed = small['width'] + kerf
                    if needed <= remaining:
                        best_small_idx = idx
                        break

                if best_small_idx >= 0:
                    current_strip['items'].append(large_items.pop(0))
                    current_strip['items'].append(medium_items.pop(0))
                    current_strip['items'].append(small_items.pop(best_small_idx))
                    current_strip['space_used'] = sum(item['width'] for item in current_strip['items']) + kerf * 2
                    strips.append(current_strip)
                    continue

            # Strategy 3: Try medium + medium + medium + small
            if len(medium_items) >= 3:
                test_width = medium_items[0]['width'] + kerf + medium_items[1]['width'] + kerf + medium_items[2]['width']
                if test_width <= bin_width:
                    current_strip['items'].append(medium_items.pop(0))
                    current_strip['items'].append(medium_items.pop(0))
                    current_strip['items'].append(medium_items.pop(0))
                    current_strip['space_used'] = test_width

                    # Try to add a small item
                    remaining = bin_width - test_width
                    for idx, small in enumerate(small_items):
                        needed = small['width'] + kerf
                        if needed <= remaining:
                            current_strip['items'].append(small_items.pop(idx))
                            current_strip['space_used'] += needed
                            break

                    strips.append(current_strip)
                    continue

            # Fallback: Use BFD for remaining items
            remaining = large_items + medium_items + small_items
            if not remaining:
                break

            # Pick first item and find best fits
            item = remaining.pop(0)
            if item in large_items:
                large_items.remove(item)
            elif item in medium_items:
                medium_items.remove(item)
            else:
                small_items.remove(item)

            current_strip['items'].append(item)
            current_strip['space_used'] = item['width']

            # Try to fill remaining space
            while True:
                remaining_space = bin_width - current_strip['space_used']
                remaining = large_items + medium_items + small_items
                if not remaining:
                    break

                # Find best-fit item
                best_idx = -1
                best_item = None
                best_fit = float('inf')
                best_list = None

                for item_list in [large_items, medium_items, small_items]:
                    for idx, it in enumerate(item_list):
                        needed = it['width'] + kerf
                        if needed <= remaining_space:
                            fit = remaining_space - needed
                            if fit < best_fit:
                                best_fit = fit
                                best_idx = idx
                                best_item = it
                                best_list = item_list

                if best_item:
                    best_list.remove(best_item)
                    current_strip['items'].append(best_item)
                    current_strip['space_used'] += best_item['width'] + kerf
                else:
                    break

            strips.append(current_strip)

        # Pack strips into bins
        return self._pack_strips_into_bins(strips, bin_type, strip_height, strips_per_bin, kerf)

    def _pack_strips_into_bins(
        self,
        strips: List[Dict],
        bin_type: Bin,
        strip_height: float,
        strips_per_bin: int,
        kerf: float
    ) -> List[BinPacking]:
        """Pack strips into 2D bins."""
        bins = []
        strip_idx = 0

        while strip_idx < len(strips):
            bin_packing = BinPacking(
                bin_id=len(bins),
                bin_type=bin_type,
                items=[]
            )

            # Pack up to strips_per_bin strips
            for local_strip_idx in range(strips_per_bin):
                if strip_idx >= len(strips):
                    break

                strip = strips[strip_idx]
                current_y = local_strip_idx * (strip_height + kerf)

                # Place all items in this strip
                current_x = 0
                for item_data in strip['items']:
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
                    current_x = x + item_data['width']

                strip_idx += 1

            if bin_packing.items:
                bins.append(bin_packing)

        return bins

    def _pack_two_column_layout(
        self,
        prepared_items: List[Dict],
        bin_type: Bin,
        kerf: float,
        strip_height: float,
        strips_per_bin: int,
        right_column_width: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack using two-column layout with improved left-column packing:
        - Right column: Reserved for items matching right_column_width
        - Left column: Use First-Fit-Decreasing for better utilization
        """

        bin_width = bin_type.width

        # Separate items
        right_column_items = [pi for pi in prepared_items if pi['width'] == right_column_width]
        left_column_items = [pi for pi in prepared_items if pi['width'] != right_column_width]

        # Sort left column items by width descending (largest first)
        left_column_items.sort(key=lambda x: x['width'], reverse=True)

        print(f"  Two-column layout:")
        print(f"    Right column ({right_column_width}mm): {len(right_column_items)} items")
        print(f"    Left column: {len(left_column_items)} items")

        # Calculate column widths
        right_col_width = right_column_width + kerf
        left_col_width = bin_width - right_col_width - kerf

        print(f"    Left column width: {left_col_width}mm")

        bins = []

        # Create bins structure - pre-allocate strips
        # Each strip can hold left items + one right item
        strips = []  # List of (left_items, right_item)

        # First, allocate all right column items to strips (one per strip)
        for right_item in right_column_items:
            strips.append({'left_items': [], 'right_item': right_item, 'left_space_used': 0})

        # Add extra strips for remaining left items if needed
        estimated_extra_strips = (len(left_column_items) * 2) // 3  # rough estimate
        for _ in range(estimated_extra_strips):
            strips.append({'left_items': [], 'right_item': None, 'left_space_used': 0})

        # Pack left column items using First-Fit-Decreasing
        for item_data in left_column_items:
            item_width = item_data['width']
            placed = False

            # Try to find a strip with enough space
            for strip in strips:
                space_available = left_col_width - strip['left_space_used']
                needed_space = item_width if strip['left_space_used'] == 0 else item_width + kerf

                if needed_space <= space_available:
                    strip['left_items'].append(item_data)
                    strip['left_space_used'] += needed_space
                    placed = True
                    break

            # If not placed, create a new strip
            if not placed:
                new_strip = {'left_items': [item_data], 'right_item': None, 'left_space_used': item_width}
                strips.append(new_strip)

        # Now pack strips into bins
        current_bin_index = 0
        strip_idx = 0

        while strip_idx < len(strips):
            if time.time() - start_time > self.time_limit:
                break

            bin_packing = BinPacking(
                bin_id=current_bin_index,
                bin_type=bin_type,
                items=[]
            )

            # Pack up to strips_per_bin strips in this bin
            for local_strip_idx in range(strips_per_bin):
                if strip_idx >= len(strips):
                    break

                strip = strips[strip_idx]
                current_y = local_strip_idx * (strip_height + kerf)

                # Pack left column items in this strip
                current_x = 0
                for item_data in strip['left_items']:
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
                    current_x = x + item_data['width']

                # Pack right column item if exists
                if strip['right_item'] is not None:
                    item_data = strip['right_item']
                    x = left_col_width + kerf

                    placed_item = PlacedItem(
                        item=item_data['item'],
                        x=x,
                        y=current_y,
                        width=item_data['width'],
                        height=item_data['height'],
                        rotated=item_data['rotated']
                    )
                    bin_packing.items.append(placed_item)

                strip_idx += 1

            if bin_packing.items:
                bins.append(bin_packing)
                current_bin_index += 1
            else:
                break

        return bins

    def _pack_simple_strips(
        self,
        prepared_items: List[Dict],
        bin_type: Bin,
        kerf: float,
        strip_height: float,
        strips_per_bin: int,
        start_time: float
    ) -> List[BinPacking]:
        """
        Simple horizontal strip packing (no column subdivision).
        """

        bin_width = bin_type.width

        # Sort by width descending
        prepared_items.sort(key=lambda x: x['width'], reverse=True)

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

            # Pack strips
            for strip_idx in range(strips_per_bin):
                if not prepared_items:
                    break

                current_y = strip_idx * (strip_height + kerf)
                current_x = 0

                # Pack items left to right in this strip
                while prepared_items:
                    item_data = prepared_items[0]
                    needed_width = item_data['width'] if current_x == 0 else item_data['width'] + kerf

                    if current_x + needed_width <= bin_width:
                        prepared_items.pop(0)
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
                        current_x = x + item_data['width']
                    else:
                        break

            if bin_packing.items:
                bins.append(bin_packing)
                current_bin_index += 1
            else:
                break

        return bins

    def _pack_fallback(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """Fallback to simple packing for non-uniform heights."""
        from tessellate.algorithms.nfdh_smart import SmartNFDHPacker
        packer = SmartNFDHPacker(time_limit=self.time_limit)
        # This is a hack - we need to create a mini problem
        from tessellate.core.models import Problem
        problem = Problem(items=items, bins=[bin_type], kerf=kerf)
        solution = packer.solve(problem)
        return solution.bins
