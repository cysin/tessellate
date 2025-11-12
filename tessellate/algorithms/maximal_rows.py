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

    def __init__(self, time_limit: float = 300.0, max_row_patterns: int = 100000):
        """
        Initialize maximal rows algorithm.

        Args:
            time_limit: Maximum execution time
            max_row_patterns: Maximum number of row patterns to generate
        """
        super().__init__(time_limit)
        self.max_row_patterns = max_row_patterns

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
        print(f"Strategy: Generate ALL maximized-width row patterns")
        print(f"Max patterns: {self.max_row_patterns}")
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
        Pack items by generating all possible row patterns and finding optimal combination.
        """
        # Expand items to individual pieces
        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        print(f"    Generating row patterns...")

        # Generate ALL possible row patterns (no width constraint)
        all_patterns = self._generate_all_row_patterns(
            all_pieces, bin_type, kerf, start_time, min_width_ratio=0.0
        )

        print(f"    Generated {len(all_patterns)} row patterns")

        # Step 2: Find optimal combination of rows to pack all items
        boards = self._find_optimal_row_stacking(
            all_pieces, all_patterns, bin_type, kerf, start_time
        )

        return boards

    def _generate_all_row_patterns(
        self,
        pieces: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float,
        min_width_ratio: float = 0.70
    ) -> List[RowPattern]:
        """
        Generate ALL possible row patterns that maximize width usage.

        For each subset of items, tries all rotation combinations to find
        patterns that fit in board width and maximize utilization.
        """
        patterns = []
        seen_signatures = set()

        # Group identical items to avoid redundant combinations
        item_groups = defaultdict(list)
        for piece in pieces:
            key = (piece.id, piece.width, piece.height)
            item_groups[key].append(piece)

        unique_items = []
        item_counts = {}
        for key, items in item_groups.items():
            unique_items.append(items[0])
            item_counts[items[0].id] = len(items)

        print(f"      Unique item types: {len(unique_items)}")

        # Generate patterns by trying different item combinations
        # Start with larger combinations (more items per row = better utilization)
        for num_items in range(min(len(unique_items), 10), 0, -1):
            if time.time() - start_time > self.time_limit * 0.3:
                print(f"      Time limit reached during pattern generation")
                break

            if len(patterns) >= self.max_row_patterns:
                print(f"      Max patterns reached")
                break

            # Try combinations of items
            for item_combo in combinations(unique_items, num_items):
                if time.time() - start_time > self.time_limit * 0.3:
                    break

                # For each combination, try all rotation possibilities
                rotation_options = []
                for item in item_combo:
                    if item.rotatable:
                        rotation_options.append([False, True])
                    else:
                        rotation_options.append([False])

                # Generate all rotation combinations
                for rotations in product(*rotation_options):
                    # Calculate if this fits in width
                    total_width = 0.0
                    max_height = 0.0

                    for i, (item, rotated) in enumerate(zip(item_combo, rotations)):
                        item_width = item.height if rotated else item.width
                        item_height = item.width if rotated else item.height

                        total_width += item_width
                        if i > 0:
                            total_width += kerf
                        max_height = max(max_height, item_height)

                    # Check if fits in board width AND uses substantial width
                    # This focuses on patterns that truly "maximize width"
                    width_utilization = total_width / bin_type.width
                    if total_width <= bin_type.width and width_utilization >= min_width_ratio:
                        # Create pattern signature to avoid duplicates
                        signature = self._pattern_signature(item_combo, rotations)

                        if signature not in seen_signatures:
                            seen_signatures.add(signature)

                            pattern = RowPattern(
                                items=list(zip(item_combo, rotations)),
                                width=total_width,
                                height=max_height
                            )
                            patterns.append(pattern)

                            if len(patterns) >= self.max_row_patterns:
                                break

        # Sort patterns by utilization (best first)
        patterns.sort(key=lambda p: p.utilization(bin_type.width), reverse=True)

        return patterns

    def _pattern_signature(self, items: Tuple[Item, ...], rotations: Tuple[bool, ...]) -> tuple:
        """Create signature for pattern deduplication."""
        item_ids = tuple(sorted((item.id, rotated) for item, rotated in zip(items, rotations)))
        return item_ids

    def _find_optimal_row_stacking_hybrid(
        self,
        all_pieces: List[Item],
        high_width_patterns: List[RowPattern],
        medium_width_patterns: List[RowPattern],
        low_width_patterns: List[RowPattern],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Hybrid stacking: use high-width patterns first, fall back to medium/low-width for remaining items.
        """
        boards = []
        remaining_pieces = all_pieces.copy()

        print(f"    Stacking rows to pack {len(remaining_pieces)} items...")

        # Phase 1: Use high-width patterns
        phase = "high"
        active_patterns = high_width_patterns
        boards_in_phase = 0

        while remaining_pieces:
            if time.time() - start_time > self.time_limit:
                print(f"    Time limit reached")
                break

            # Pack one board
            board_rows = []
            current_height = 0.0
            board_remaining = remaining_pieces.copy()

            # Greedily select rows that fit in this board
            while board_remaining:
                best_pattern = None
                best_score = -1

                # Find best row pattern for remaining items
                for pattern in active_patterns:
                    # Check if pattern height fits
                    row_height = pattern.height
                    if current_height + row_height + (kerf if board_rows else 0) > bin_type.height:
                        continue

                    # Check if pattern items are available
                    items_available = True
                    items_used = []
                    temp_remaining = board_remaining.copy()

                    for pattern_item, rotated in pattern.items:
                        found = False
                        for i, avail_item in enumerate(temp_remaining):
                            if (avail_item.id == pattern_item.id and
                                avail_item.width == pattern_item.width and
                                avail_item.height == pattern_item.height):
                                items_used.append((avail_item, rotated))
                                temp_remaining.pop(i)
                                found = True
                                break

                        if not found:
                            items_available = False
                            break

                    if not items_available:
                        continue

                    # Score this pattern
                    utilization = pattern.utilization(bin_type.width)
                    num_items = len(pattern.items)
                    remaining_types = {}
                    for item in temp_remaining:
                        key = (item.id, item.width, item.height)
                        remaining_types[key] = remaining_types.get(key, 0) + 1
                    balance = len(remaining_types) if remaining_types else 0
                    score = (utilization * 100) + (num_items * 2) + (balance * 0.5)

                    if score > best_score:
                        best_score = score
                        best_pattern = (pattern, items_used, temp_remaining)

                if best_pattern:
                    pattern, items_used, temp_remaining = best_pattern
                    board_rows.append((pattern, items_used, current_height))
                    current_height += pattern.height + kerf
                    board_remaining = temp_remaining
                else:
                    # No more rows fit
                    break

            if board_rows:
                # Create board
                bin_packing = self._create_bin_from_rows(board_rows, bin_type, kerf, len(boards))
                boards.append(bin_packing)
                boards_in_phase += 1

                num_placed = sum(len(items_used) for _, items_used, _ in board_rows)
                remaining_pieces = board_remaining
                util = bin_packing.utilization()
                print(f"    Board {len(boards)} ({phase}): {util:.2%} utilization, {num_placed} items, {len(remaining_pieces)} remaining")
            else:
                # Can't pack with current patterns, try switching to next phase
                if phase == "high" and remaining_pieces:
                    print(f"    Switching to medium-width patterns for remaining {len(remaining_pieces)} items")
                    phase = "medium"
                    active_patterns = medium_width_patterns
                    boards_in_phase = 0
                    continue
                elif phase == "medium" and remaining_pieces:
                    print(f"    Switching to low-width patterns for remaining {len(remaining_pieces)} items")
                    phase = "low"
                    active_patterns = low_width_patterns
                    boards_in_phase = 0
                    continue
                else:
                    print(f"    Warning: {len(remaining_pieces)} items couldn't be packed")
                    break

        return boards

    def _find_optimal_row_stacking(
        self,
        all_pieces: List[Item],
        row_patterns: List[RowPattern],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Find optimal combination of row patterns to pack all items.

        This uses a greedy approach: repeatedly select rows that cover
        the most uncovered items with best utilization.
        """
        boards = []
        remaining_pieces = all_pieces.copy()

        print(f"    Stacking rows to pack {len(remaining_pieces)} items...")

        while remaining_pieces:
            if time.time() - start_time > self.time_limit:
                print(f"    Time limit reached")
                break

            # Pack one board
            board_rows = []
            current_height = 0.0
            board_remaining = remaining_pieces.copy()

            # Greedily select rows that fit in this board
            while board_remaining:
                best_pattern = None
                best_score = -1

                # Find best row pattern for remaining items
                for pattern in row_patterns:
                    # Check if pattern height fits
                    row_height = pattern.height
                    if current_height + row_height + (kerf if board_rows else 0) > bin_type.height:
                        continue

                    # Check if pattern items are available
                    items_available = True
                    items_used = []
                    temp_remaining = board_remaining.copy()

                    for pattern_item, rotated in pattern.items:
                        found = False
                        for i, avail_item in enumerate(temp_remaining):
                            if (avail_item.id == pattern_item.id and
                                avail_item.width == pattern_item.width and
                                avail_item.height == pattern_item.height):
                                items_used.append((avail_item, rotated))
                                temp_remaining.pop(i)
                                found = True
                                break

                        if not found:
                            items_available = False
                            break

                    if not items_available:
                        continue

                    # Score this pattern
                    # Factors: utilization, item count, and balance of remaining items
                    utilization = pattern.utilization(bin_type.width)
                    num_items = len(pattern.items)

                    # Bonus for leaving a balanced set of remaining items
                    # Count item types in remaining set
                    remaining_types = {}
                    for item in temp_remaining:
                        key = (item.id, item.width, item.height)
                        remaining_types[key] = remaining_types.get(key, 0) + 1

                    # Calculate balance (prefer leaving many different types)
                    balance = len(remaining_types) if remaining_types else 0

                    # Combined score: prioritize utilization, then item count, then balance
                    score = (utilization * 100) + (num_items * 2) + (balance * 0.5)

                    if score > best_score:
                        best_score = score
                        best_pattern = (pattern, items_used, temp_remaining)

                if best_pattern:
                    pattern, items_used, temp_remaining = best_pattern

                    # Add this row to the board
                    board_rows.append((pattern, items_used, current_height))
                    current_height += pattern.height + kerf
                    board_remaining = temp_remaining
                else:
                    # No more rows fit
                    break

            if board_rows:
                # Create BinPacking from rows
                bin_packing = self._create_bin_from_rows(board_rows, bin_type, kerf, len(boards))
                boards.append(bin_packing)

                # Update remaining pieces - board_remaining already has the unpacked items
                num_placed = sum(len(items_used) for _, items_used, _ in board_rows)
                remaining_pieces = board_remaining

                util = bin_packing.utilization()
                print(f"    Board {len(boards)}: {util:.2%} utilization, {num_placed} items, {len(remaining_pieces)} remaining")
            else:
                # Can't pack any more
                print(f"    Warning: {len(remaining_pieces)} items couldn't be packed")
                break

        return boards

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
