"""
Maximal Row Pattern Algorithm

This algorithm generates ALL possible row patterns that maximize width,
then finds the optimal combination to stack them vertically.

Strategy:
1. Generate ALL possible row combinations that fit in board width
2. For each row, try all rotation possibilities
3. Find optimal stacking of rows to minimize boards
4. Use dynamic programming or exhaustive search

This should achieve better results (potentially 10 boards) by exploring
all possible row arrangements.
"""

import time
import random
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations, product

from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


@dataclass
class RowPattern:
    """A row pattern with items and their orientations."""
    items: List[Tuple[Item, bool]]  # (item, rotated)
    width: float
    height: float

    def utilization(self, board_width: float) -> float:
        """Calculate width utilization of this row."""
        total_area = sum(
            (item.height if rotated else item.width) * (item.width if rotated else item.height)
            for item, rotated in self.items
        )
        row_area = board_width * self.height
        return total_area / row_area if row_area > 0 else 0.0


class MaximalRowsAlgorithm(PackingAlgorithm):
    """
    Maximal Rows Algorithm - generates all possible row patterns with rotation.

    This is a more exhaustive approach that should find better solutions
    by considering all possible row combinations and rotations.
    """

    def __init__(self, time_limit: float = 300.0, num_trials: int = 100, width_threshold: float = 0.70):
        """
        Initialize maximal rows algorithm.

        Args:
            time_limit: Maximum execution time
            num_trials: Number of different packing trials to attempt
            width_threshold: Minimum width utilization for high-quality rows (0.70 = 70%)
        """
        super().__init__(time_limit)
        self.num_trials = num_trials
        self.width_threshold = width_threshold

    def get_name(self) -> str:
        return "MaximalRows"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using maximal rows approach.

        Args:
            problem: Problem instance

        Returns:
            Solution with packed boards
        """
        start_time = time.time()

        print(f"\n{'='*70}")
        print(f"Maximal Rows Algorithm")
        print(f"{'='*70}")
        print(f"Strategy: Multi-trial row stacking with width threshold")
        print(f"Trials: {self.num_trials}, Width threshold: {self.width_threshold*100:.0f}%")
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

            # Pack items using maximal rows
            packed_bins = self._pack_with_maximal_rows(
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

    def _pack_with_maximal_rows(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack items using multi-trial approach with row stacking.

        Each trial builds a complete packing plan by:
        1. Selecting high-width rows (>threshold) greedily
        2. Packing remaining items with any valid rows
        3. Trying different orderings via multiple trials
        """
        # Expand items to individual pieces
        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        print(f"    Running {self.num_trials} trials to find best packing...")

        best_solution = None
        best_num_boards = float('inf')

        for trial in range(self.num_trials):
            if time.time() - start_time > self.time_limit:
                print(f"    Time limit reached at trial {trial}")
                break

            # Run one complete packing trial
            boards = self._run_one_trial(
                all_pieces, bin_type, kerf, start_time, trial
            )

            if boards and len(boards) < best_num_boards:
                best_num_boards = len(boards)
                best_solution = boards
                print(f"    Trial {trial}: {len(boards)} boards (NEW BEST)")

        print(f"    Best solution: {best_num_boards} boards from {trial+1} trials")
        return best_solution if best_solution else []

    def _run_one_trial(
        self,
        all_pieces: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float,
        trial_num: int
    ) -> List[BinPacking]:
        """
        Run one complete packing trial.

        Strategy:
        1. For each board, try to fill with high-width rows (>threshold)
        2. When high-width rows not available, use any valid rows
        3. Continue until all pieces packed
        """
        # Shuffle pieces for variation between trials (deterministic based on trial number)
        pieces = all_pieces.copy()
        random.seed(trial_num)
        random.shuffle(pieces)

        boards = []
        remaining = pieces

        while remaining:
            if time.time() - start_time > self.time_limit:
                break

            # Pack one board
            board_rows, items_used = self._pack_one_board_with_rows(
                remaining, bin_type, kerf, start_time
            )

            if not board_rows:
                # Can't pack anymore
                break

            # Create board
            bin_packing = self._create_bin_from_rows(board_rows, bin_type, kerf, len(boards))
            boards.append(bin_packing)

            # Remove used items
            for item in items_used:
                remaining.remove(item)

        # Only return if all items packed
        if not remaining:
            return boards
        else:
            return []  # Invalid solution

    def _pack_one_board_with_rows(
        self,
        available_pieces: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> Tuple[List[Tuple[RowPattern, List[Tuple[Item, bool]], float]], List[Item]]:
        """
        Pack one board by selecting rows that fit.

        Returns:
            (board_rows, items_used)
        """
        board_rows = []
        current_height = 0.0
        items_used = []
        remaining = available_pieces.copy()

        # Fill board with best available rows
        while remaining:
            # Use adaptive threshold: prefer high-width rows, but accept lower if needed
            best_row = self._find_best_row(
                remaining, bin_type, kerf, current_height,
                min_width_ratio=self.width_threshold
            )

            # If no high-width rows, try any width
            if not best_row:
                best_row = self._find_best_row(
                    remaining, bin_type, kerf, current_height,
                    min_width_ratio=0.0
                )

            if best_row:
                pattern, row_items, row_height = best_row

                # Check if fits in height
                needed_height = row_height + (kerf if board_rows else 0)
                if current_height + needed_height > bin_type.height:
                    break

                # Add row to board
                board_rows.append((pattern, row_items, current_height))
                current_height += row_height + kerf

                # Remove used items
                for item, _ in row_items:
                    remaining.remove(item)
                    items_used.append(item)
            else:
                # No valid rows can be formed
                break

        return board_rows, items_used

    def _find_best_row(
        self,
        available_pieces: List[Item],
        bin_type: Bin,
        kerf: float,
        current_height: float,
        min_width_ratio: float
    ) -> Optional[Tuple[RowPattern, List[Tuple[Item, bool]], float]]:
        """
        Find the best row from available pieces that meets width threshold.

        Returns:
            (pattern, items_with_rotations, row_height) or None
        """
        # Group identical items
        item_groups = defaultdict(list)
        for piece in available_pieces:
            key = (piece.id, piece.width, piece.height)
            item_groups[key].append(piece)

        unique_items = [items[0] for items in item_groups.values()]

        best_row = None
        best_score = -1

        # Try combinations of items (up to 8 items per row)
        max_items_per_row = min(len(unique_items), 8)

        for num_items in range(max_items_per_row, 0, -1):
            for item_combo in combinations(unique_items, num_items):
                # Check we have enough items
                combo_counts = {}
                for item in item_combo:
                    key = (item.id, item.width, item.height)
                    combo_counts[key] = combo_counts.get(key, 0) + 1

                # Verify availability
                available = True
                for key, needed_count in combo_counts.items():
                    if len(item_groups[key]) < needed_count:
                        available = False
                        break
                if not available:
                    continue

                # Try all rotation combinations
                rotation_options = []
                for item in item_combo:
                    if item.rotatable:
                        rotation_options.append([False, True])
                    else:
                        rotation_options.append([False])

                for rotations in product(*rotation_options):
                    # Calculate dimensions
                    total_width = 0.0
                    max_height = 0.0

                    for i, (item, rotated) in enumerate(zip(item_combo, rotations)):
                        w = item.height if rotated else item.width
                        h = item.width if rotated else item.height

                        total_width += w
                        if i > 0:
                            total_width += kerf
                        max_height = max(max_height, h)

                    # Check constraints
                    width_util = total_width / bin_type.width
                    if total_width > bin_type.width:
                        continue
                    if width_util < min_width_ratio:
                        continue

                    # Score: prefer high width utilization and more items
                    score = width_util * 100 + num_items * 2

                    if score > best_score:
                        best_score = score

                        # Build items list with actual instances
                        row_items = []
                        temp_groups = {k: list(v) for k, v in item_groups.items()}

                        for item, rotated in zip(item_combo, rotations):
                            key = (item.id, item.width, item.height)
                            actual_item = temp_groups[key].pop(0)
                            row_items.append((actual_item, rotated))

                        pattern = RowPattern(
                            items=list(zip(item_combo, rotations)),
                            width=total_width,
                            height=max_height
                        )

                        best_row = (pattern, row_items, max_height)

        return best_row

    def _create_bin_from_rows(
        self,
        board_rows: List[Tuple[RowPattern, List[Tuple[Item, bool]], float]],
        bin_type: Bin,
        kerf: float,
        bin_id: int
    ) -> BinPacking:
        """Create BinPacking from row patterns."""
        placed_items = []

        for pattern, items_used, y_position in board_rows:
            x = 0.0
            for item, rotated in items_used:
                placed_items.append(PlacedItem(
                    item=item,
                    x=x,
                    y=y_position,
                    width=item.height if rotated else item.width,
                    height=item.width if rotated else item.height,
                    rotated=rotated
                ))
                x += (item.height if rotated else item.width) + kerf

        return BinPacking(
            bin_id=bin_id,
            bin_type=bin_type,
            items=placed_items
        )
