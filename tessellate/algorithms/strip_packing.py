"""
Simple Strip Packing Algorithm

This algorithm packs items in horizontal rows (strips/shelves):
1. Pack items in rows, maximizing width usage
2. Stack rows vertically, maximizing height
3. Try different row combinations with rotation
4. Select the arrangement with best utilization

Characteristics:
- Fast and simple (no complex guillotine logic)
- Works very well for items with similar heights
- Supports rotation for better packing
- Deterministic results
"""

import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from itertools import combinations

from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


@dataclass
class Row:
    """A horizontal row of items."""
    items: List[Tuple[Item, bool]]  # (item, rotated)
    width: float
    height: float
    y_position: float = 0.0

    def add_item(self, item: Item, rotated: bool, kerf: float) -> bool:
        """Try to add an item to this row."""
        item_width = item.height if rotated else item.width
        item_height = item.width if rotated else item.height

        # Check if item fits in width
        needed_width = self.width + (kerf if self.items else 0) + item_width

        if needed_width <= 0:  # Not initialized yet
            self.items.append((item, rotated))
            self.width = item_width
            self.height = item_height
            return True
        else:
            # Check if we have space
            # We'll check against bin width later
            self.items.append((item, rotated))
            self.width += kerf + item_width
            self.height = max(self.height, item_height)
            return True

    def fits_in_bin(self, bin_width: float) -> bool:
        """Check if this row fits in bin width."""
        return self.width <= bin_width


class StripPackingAlgorithm(PackingAlgorithm):
    """
    Simple strip packing algorithm.

    Arranges items in horizontal rows from top to bottom.
    Tries different combinations and rotations to maximize utilization.
    """

    def __init__(self, time_limit: float = 300.0, max_trials: int = 100):
        """
        Initialize strip packing algorithm.

        Args:
            time_limit: Maximum execution time
            max_trials: Number of different row arrangements to try
        """
        super().__init__(time_limit)
        self.max_trials = max_trials

    def get_name(self) -> str:
        return "StripPacking"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using strip packing approach.

        Args:
            problem: Problem instance

        Returns:
            Solution with packed boards
        """
        start_time = time.time()

        print(f"\n{'='*70}")
        print(f"Strip Packing Algorithm")
        print(f"{'='*70}")
        print(f"Strategy: Row-by-row packing with rotation")
        print(f"Max trials: {self.max_trials}")
        print()

        # Group items by material
        groups = problem.group_by_material()

        all_bins = []
        all_unplaced = []

        for (thickness, material), group_items in groups.items():
            print(f"Processing group: {material} {thickness}mm")
            print(f"  Items: {len(group_items)}, Total pieces: {sum(i.quantity for i in group_items)}")

            # Get compatible bins
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    all_unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Pack items using strip packing
            packed_bins = self._strip_pack_items(
                group_items, bin_type, problem.kerf, start_time
            )

            print(f"  Packed into {len(packed_bins)} boards")

            all_bins.extend(packed_bins)

        # Create solution
        solution = Solution(bins=all_bins, unplaced=all_unplaced)
        execution_time = time.time() - start_time
        solution.metadata["algorithm"] = self.get_name()
        solution.metadata["execution_time"] = execution_time

        return solution

    def _strip_pack_items(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack items using strip packing approach.

        Tries different row arrangements to find best utilization.
        """
        # Expand items to individual pieces
        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        print(f"    Total pieces to pack: {len(all_pieces)}")

        boards = []
        remaining_pieces = all_pieces.copy()

        # Pack board by board
        while remaining_pieces:
            if time.time() - start_time > self.time_limit:
                print("    Time limit reached")
                break

            # Try different packing strategies for this board
            best_packing = None
            best_util = 0.0

            # Strategy 1: Sort by height (tallest first)
            trial_packing = self._pack_one_board(
                remaining_pieces.copy(),
                bin_type,
                kerf,
                sort_key=lambda x: -x.height
            )
            if trial_packing and trial_packing.utilization() > best_util:
                best_util = trial_packing.utilization()
                best_packing = trial_packing

            # Strategy 2: Sort by width (widest first)
            trial_packing = self._pack_one_board(
                remaining_pieces.copy(),
                bin_type,
                kerf,
                sort_key=lambda x: -x.width
            )
            if trial_packing and trial_packing.utilization() > best_util:
                best_util = trial_packing.utilization()
                best_packing = trial_packing

            # Strategy 3: Sort by area (largest first)
            trial_packing = self._pack_one_board(
                remaining_pieces.copy(),
                bin_type,
                kerf,
                sort_key=lambda x: -x.area()
            )
            if trial_packing and trial_packing.utilization() > best_util:
                best_util = trial_packing.utilization()
                best_packing = trial_packing

            # Strategy 4: Try with rotation preference
            trial_packing = self._pack_one_board_with_rotation(
                remaining_pieces.copy(),
                bin_type,
                kerf
            )
            if trial_packing and trial_packing.utilization() > best_util:
                best_util = trial_packing.utilization()
                best_packing = trial_packing

            if best_packing and best_packing.items:
                boards.append(best_packing)
                # Remove packed items (simply remove first N items since we packed from beginning)
                num_packed = len(best_packing.items)
                remaining_pieces = remaining_pieces[num_packed:]
                print(f"    Board {len(boards)}: {best_util:.2%} utilization, {num_packed} items, {len(remaining_pieces)} remaining")
            else:
                # Can't pack any more
                print(f"    Warning: {len(remaining_pieces)} items couldn't be packed")
                break

        return boards

    def _pack_one_board(
        self,
        pieces: List[Item],
        bin_type: Bin,
        kerf: float,
        sort_key
    ) -> Optional[BinPacking]:
        """
        Pack items into one board using row-by-row approach.
        """
        # Sort items
        pieces.sort(key=sort_key)

        rows = []
        current_row = Row(items=[], width=0, height=0)
        current_y = 0.0

        for item in pieces:
            # Try to add to current row (no rotation)
            item_width = item.width
            item_height = item.height

            needed_width = current_row.width + (kerf if current_row.items else 0) + item_width

            if needed_width <= bin_type.width and current_y + item_height <= bin_type.height:
                # Fits in current row
                current_row.items.append((item, False))
                current_row.width = needed_width
                current_row.height = max(current_row.height, item_height)
            else:
                # Start new row
                if current_row.items:
                    current_row.y_position = current_y
                    rows.append(current_row)
                    current_y += current_row.height + kerf

                # Check if item fits in new row
                if item_width <= bin_type.width and current_y + item_height <= bin_type.height:
                    current_row = Row(items=[(item, False)], width=item_width, height=item_height)
                else:
                    # Item doesn't fit at all
                    break

        # Add last row
        if current_row.items and current_y + current_row.height <= bin_type.height:
            current_row.y_position = current_y
            rows.append(current_row)

        # Convert rows to BinPacking
        if not rows:
            return None

        placed_items = []
        for row in rows:
            x = 0.0
            for item, rotated in row.items:
                placed_items.append(PlacedItem(
                    item=item,
                    x=x,
                    y=row.y_position,
                    width=item.height if rotated else item.width,
                    height=item.width if rotated else item.height,
                    rotated=rotated
                ))
                x += (item.height if rotated else item.width) + kerf

        return BinPacking(
            bin_id=0,
            bin_type=bin_type,
            items=placed_items
        )

    def _pack_one_board_with_rotation(
        self,
        pieces: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Optional[BinPacking]:
        """
        Pack items with intelligent rotation selection.

        For each item, tries both orientations and picks the one that fits better.
        """
        # Sort by area (largest first)
        pieces.sort(key=lambda x: -x.area())

        rows = []
        current_row = Row(items=[], width=0, height=0)
        current_y = 0.0

        for item in pieces:
            if not item.rotatable:
                # No rotation allowed
                rotated = False
                item_width = item.width
                item_height = item.height
            else:
                # Try both orientations, pick better fit
                # Normal orientation
                w1, h1 = item.width, item.height
                # Rotated orientation
                w2, h2 = item.height, item.width

                # Pick orientation that better fits remaining row width
                remaining_row_width = bin_type.width - current_row.width - (kerf if current_row.items else 0)

                if w1 <= remaining_row_width and w2 <= remaining_row_width:
                    # Both fit, pick one that uses width more efficiently
                    if w1 > w2:
                        rotated = False
                        item_width, item_height = w1, h1
                    else:
                        rotated = True
                        item_width, item_height = w2, h2
                elif w1 <= remaining_row_width:
                    rotated = False
                    item_width, item_height = w1, h1
                elif w2 <= remaining_row_width:
                    rotated = True
                    item_width, item_height = w2, h2
                else:
                    # Neither fits in current row, pick narrower for new row
                    if w1 <= w2:
                        rotated = False
                        item_width, item_height = w1, h1
                    else:
                        rotated = True
                        item_width, item_height = w2, h2

            needed_width = current_row.width + (kerf if current_row.items else 0) + item_width

            if needed_width <= bin_type.width and current_y + item_height <= bin_type.height:
                # Fits in current row
                current_row.items.append((item, rotated))
                current_row.width = needed_width
                current_row.height = max(current_row.height, item_height)
            else:
                # Start new row
                if current_row.items:
                    current_row.y_position = current_y
                    rows.append(current_row)
                    current_y += current_row.height + kerf

                # Check if item fits in new row
                if item_width <= bin_type.width and current_y + item_height <= bin_type.height:
                    current_row = Row(items=[(item, rotated)], width=item_width, height=item_height)
                else:
                    # Item doesn't fit
                    break

        # Add last row
        if current_row.items and current_y + current_row.height <= bin_type.height:
            current_row.y_position = current_y
            rows.append(current_row)

        # Convert rows to BinPacking
        if not rows:
            return None

        placed_items = []
        for row in rows:
            x = 0.0
            for item, rotated in row.items:
                placed_items.append(PlacedItem(
                    item=item,
                    x=x,
                    y=row.y_position,
                    width=item.height if rotated else item.width,
                    height=item.width if rotated else item.height,
                    rotated=rotated
                ))
                x += (item.height if rotated else item.width) + kerf

        return BinPacking(
            bin_id=0,
            bin_type=bin_type,
            items=placed_items
        )
