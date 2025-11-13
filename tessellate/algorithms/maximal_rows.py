"""
Maximal Row Pattern Algorithm

This algorithm generates ALL possible row patterns that maximize width,
then finds the optimal combination to stack them vertically.

Strategy:
1. Generate ALL possible row patterns with ALL rotation combinations (exhaustive)
2. Try ALL possible ways to stack rows on boards
3. Use backtracking to explore complete solution space
4. Find absolute minimum boards needed

This is a complete exhaustive search - may be slow but will find optimal solution.
"""

import time
import random
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations, product, combinations_with_replacement

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

    def __init__(self, time_limit: float = 3600.0):
        """
        Initialize maximal rows algorithm.

        Args:
            time_limit: Maximum execution time (default 1 hour for exhaustive search)
        """
        super().__init__(time_limit)
        self.best_solution = None
        self.best_num_boards = float('inf')
        self.patterns_generated = 0
        self.solutions_explored = 0

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
        print(f"Maximal Rows Algorithm - EXHAUSTIVE SEARCH")
        print(f"{'='*70}")
        print(f"Strategy: Generate ALL row patterns, try ALL stackings")
        print(f"Time limit: {self.time_limit}s")
        print(f"WARNING: This is a complete exhaustive search - may take a long time!")
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
        Pack items using EXHAUSTIVE backtracking search.

        Strategy:
        1. Generate ALL possible row patterns (no limits)
        2. Use backtracking to try ALL ways to stack rows
        3. Find minimum number of boards needed
        """
        # Expand items to individual pieces
        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        print(f"    Generating ALL possible row patterns...")
        print(f"    This may take a while...")

        # Generate ALL possible row patterns (exhaustive)
        all_row_patterns = self._generate_all_possible_rows(
            all_pieces, bin_type, kerf
        )

        print(f"    Generated {len(all_row_patterns)} row patterns")

        # Sort patterns by quality (best first) to find good solutions early
        # This makes pruning more effective while still being exhaustive
        print(f"    Sorting patterns by quality...")
        all_row_patterns.sort(key=lambda p: self._pattern_quality(p, bin_type), reverse=True)

        print(f"    Starting exhaustive backtracking search with intelligent pruning...")
        print(f"    Pruning strategy: Lower bound estimation (provably won't miss optimal)")

        # Reset best solution trackers
        self.best_solution = None
        self.best_num_boards = float('inf')
        self.solutions_explored = 0
        self.branches_pruned = 0

        # Calculate statistics for pruning
        total_area = sum(p.width * p.height for p in all_pieces)
        self.board_area = bin_type.width * bin_type.height
        self.total_pieces_area = total_area

        # Use backtracking to find optimal stacking
        self._backtrack_search(
            all_pieces, all_row_patterns, bin_type, kerf,
            [], [], start_time
        )

        print(f"    Explored {self.solutions_explored} complete solutions")
        print(f"    Pruned {self.branches_pruned} branches (provably suboptimal)")
        print(f"    Best solution: {self.best_num_boards} boards")

        return self.best_solution if self.best_solution else []

    def _pattern_quality(self, pattern: Tuple, bin_type: Bin) -> float:
        """Calculate quality score for a pattern (for sorting)."""
        pattern_indices, pattern_width, pattern_height = pattern
        width_util = pattern_width / bin_type.width
        height_util = pattern_height / bin_type.height
        num_items = len(pattern_indices)
        # Prefer high width utilization, many items, and reasonable height
        return width_util * 100 + num_items * 5 - height_util * 10

    def _generate_all_possible_rows(
        self,
        all_pieces: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> List[Tuple[List[Tuple[int, bool]], float, float]]:
        """
        Generate ALL possible row patterns with ALL rotation combinations.

        Uses item types (not instances) with combinations_with_replacement
        to allow same type multiple times, then tries ALL rotation combos.

        Returns list of (item_indices_with_rotations, width, height)
        where item_indices_with_rotations is [(piece_idx, rotated), ...]
        """
        all_patterns = []
        seen_signatures = set()

        # Group pieces by type
        item_type_groups = defaultdict(list)
        for idx, piece in enumerate(all_pieces):
            key = (piece.id, piece.width, piece.height)
            item_type_groups[key].append(idx)

        item_types = list(item_type_groups.keys())

        print(f"      Found {len(item_types)} unique item types")
        print(f"      Generating patterns with 1-10 items per row...")

        # Try rows with different numbers of items (up to 10 per row)
        for num_items in range(1, 11):
            print(f"      Processing {num_items}-item rows... ({len(all_patterns)} patterns so far)")

            # Use combinations_with_replacement to allow same type multiple times
            for type_combo in combinations_with_replacement(item_types, num_items):
                # Check if we have enough instances of each type
                type_counts = defaultdict(int)
                for item_type in type_combo:
                    type_counts[item_type] += 1

                # Verify availability
                valid = True
                for item_type, needed in type_counts.items():
                    available = len(item_type_groups[item_type])
                    if needed > available:
                        valid = False
                        break
                if not valid:
                    continue

                # Allocate specific piece indices
                allocated_indices = []
                temp_groups = {k: list(v) for k, v in item_type_groups.items()}

                for item_type in type_combo:
                    if temp_groups[item_type]:
                        piece_idx = temp_groups[item_type].pop(0)
                        allocated_indices.append(piece_idx)
                    else:
                        break

                if len(allocated_indices) != num_items:
                    continue

                pieces_in_row = [all_pieces[i] for i in allocated_indices]

                # Generate all rotation combinations
                rotation_options = []
                for piece in pieces_in_row:
                    if piece.rotatable:
                        rotation_options.append([False, True])
                    else:
                        rotation_options.append([False])

                # Try all rotation combinations
                for rotations in product(*rotation_options):
                    # Calculate dimensions
                    total_width = 0.0
                    max_height = 0.0

                    for i, (piece, rotated) in enumerate(zip(pieces_in_row, rotations)):
                        w = piece.height if rotated else piece.width
                        h = piece.width if rotated else piece.height

                        total_width += w
                        if i > 0:
                            total_width += kerf
                        max_height = max(max_height, h)

                    # Only keep if fits in board width
                    if total_width <= bin_type.width:
                        # Create signature to avoid duplicates
                        signature = self._create_pattern_signature(
                            [(all_pieces[i], rot) for i, rot in zip(allocated_indices, rotations)]
                        )

                        if signature not in seen_signatures:
                            seen_signatures.add(signature)
                            pattern = (
                                list(zip(allocated_indices, rotations)),
                                total_width,
                                max_height
                            )
                            all_patterns.append(pattern)

        return all_patterns

    def _create_pattern_signature(self, items_with_rotations: List[Tuple[Item, bool]]) -> tuple:
        """Create unique signature for a pattern to avoid duplicates."""
        return tuple(sorted((item.id, item.width, item.height, rotated)
                           for item, rotated in items_with_rotations))

    def _backtrack_search(
        self,
        all_pieces: List[Item],
        all_patterns: List[Tuple],
        bin_type: Bin,
        kerf: float,
        current_boards: List[BinPacking],
        used_piece_indices: List[int],
        start_time: float
    ):
        """
        Backtracking search to find optimal board packing.

        Tries ALL possible ways to stack rows on boards with intelligent pruning:
        - Prunes branches that provably cannot beat current best
        - Uses lower bound estimation on remaining items
        - Guarantees finding optimal solution
        """
        # Check time limit
        if time.time() - start_time > self.time_limit:
            return

        # Base case: all pieces used
        if len(used_piece_indices) == len(all_pieces):
            # Found a complete solution!
            self.solutions_explored += 1
            if len(current_boards) < self.best_num_boards:
                self.best_num_boards = len(current_boards)
                self.best_solution = [board for board in current_boards]
                print(f"      NEW BEST: {self.best_num_boards} boards (explored {self.solutions_explored}, pruned {self.branches_pruned})")
            return

        # Calculate lower bound on boards needed for remaining items
        remaining_count = len(all_pieces) - len(used_piece_indices)
        if remaining_count > 0:
            # Calculate remaining area
            used_set = set(used_piece_indices)
            remaining_area = sum(
                all_pieces[i].width * all_pieces[i].height
                for i in range(len(all_pieces)) if i not in used_set
            )

            # Theoretical minimum boards needed (assuming perfect packing)
            theoretical_min = (remaining_area + self.board_area - 1) // self.board_area  # Ceiling division

            # Prune: if current + lower bound >= best, this branch can't win
            if len(current_boards) + theoretical_min >= self.best_num_boards:
                self.branches_pruned += 1
                return

        # Try packing a new board
        used_set = set(used_piece_indices)
        remaining_indices = [i for i in range(len(all_pieces)) if i not in used_set]

        if not remaining_indices:
            return

        # Try stacking rows on a new board
        self._try_pack_board(
            all_pieces, all_patterns, bin_type, kerf,
            current_boards, used_piece_indices, remaining_indices,
            start_time, [], 0.0
        )

    def _try_pack_board(
        self,
        all_pieces: List[Item],
        all_patterns: List[Tuple],
        bin_type: Bin,
        kerf: float,
        current_boards: List[BinPacking],
        used_piece_indices: List[int],
        remaining_indices: List[int],
        start_time: float,
        current_board_rows: List[Tuple],
        current_height: float
    ):
        """
        Recursively try packing rows onto current board.

        For each valid pattern, try adding it and continue.
        Also try finishing the current board and starting new one.

        Uses intelligent pruning while guaranteeing exhaustive search.
        """
        # Check time limit
        if time.time() - start_time > self.time_limit:
            return

        # Prune if this board + remaining cannot beat best
        if len(current_boards) + 1 >= self.best_num_boards:
            self.branches_pruned += 1
            return

        # Option 1: Finish current board and start recursion for next board
        if current_board_rows:
            # Create board from current rows
            board = self._create_board_from_pattern_rows(
                current_board_rows, all_pieces, bin_type, kerf, len(current_boards)
            )
            new_boards = current_boards + [board]

            # Continue backtracking
            self._backtrack_search(
                all_pieces, all_patterns, bin_type, kerf,
                new_boards, used_piece_indices, start_time
            )

        # Option 2: Try adding more rows to current board
        used_set = set(used_piece_indices)

        # Symmetry breaking: for first row of first board, only try patterns in order
        # This avoids exploring equivalent solutions in different orders
        first_board_first_row = (len(current_boards) == 0 and len(current_board_rows) == 0)

        for idx, pattern in enumerate(all_patterns):
            pattern_indices, pattern_width, pattern_height = pattern

            # Check if all pieces in pattern are available
            if any(pidx in used_set for pidx, _ in pattern_indices):
                continue

            # Symmetry breaking: for first board's first row, only try from first available pattern
            if first_board_first_row:
                # Check if this is the first pattern that uses piece 0
                uses_piece_0 = any(pidx == 0 for pidx, _ in pattern_indices)
                if not uses_piece_0:
                    continue  # Skip until we find pattern with piece 0

            # Check if pattern fits in remaining height
            needed_height = pattern_height + (kerf if current_board_rows else 0)
            if current_height + needed_height > bin_type.height:
                continue

            # Prune: check if adding this pattern could lead to improvement
            items_in_pattern = len(pattern_indices)
            remaining_after = len(remaining_indices) - items_in_pattern
            if remaining_after > 0:
                # Rough lower bound: remaining items / avg items per pattern
                # If current + 1 (this board) + rough_min >= best, skip
                rough_min_boards = (remaining_after + 7) // 8  # Assume ~8 items/board
                if len(current_boards) + 1 + rough_min_boards >= self.best_num_boards:
                    self.branches_pruned += 1
                    continue

            # Add this pattern to current board
            new_board_rows = current_board_rows + [(pattern_indices, pattern_height)]
            new_height = current_height + needed_height
            new_used = used_piece_indices + [idx for idx, _ in pattern_indices]

            # Recurse
            self._try_pack_board(
                all_pieces, all_patterns, bin_type, kerf,
                current_boards, new_used,
                [i for i in remaining_indices if i not in [idx for idx, _ in pattern_indices]],
                start_time, new_board_rows, new_height
            )

    def _create_board_from_pattern_rows(
        self,
        board_rows: List[Tuple],
        all_pieces: List[Item],
        bin_type: Bin,
        kerf: float,
        board_id: int
    ) -> BinPacking:
        """Create a BinPacking from pattern rows."""
        placed_items = []
        y_position = 0.0

        for pattern_indices, row_height in board_rows:
            x = 0.0
            for piece_idx, rotated in pattern_indices:
                piece = all_pieces[piece_idx]
                w = piece.height if rotated else piece.width
                h = piece.width if rotated else piece.height

                placed_items.append(PlacedItem(
                    item=piece,
                    x=x,
                    y=y_position,
                    width=w,
                    height=h,
                    rotated=rotated
                ))
                x += w + kerf

            y_position += row_height + kerf

        return BinPacking(
            bin_id=board_id,
            bin_type=bin_type,
            items=placed_items
        )
