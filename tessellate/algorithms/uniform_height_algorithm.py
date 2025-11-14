"""
Uniform Height Algorithm - Specialized for items with same height

Optimized for datasets where all items share the same height dimension.
Uses systematic 2-row packing to achieve high utilization.
"""

import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict

from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class UniformHeightAlgorithm(PackingAlgorithm):
    """
    Specialized algorithm for items with uniform height.

    When all items have the same height, we can create systematic
    2-row patterns that maximize utilization.
    """

    def get_name(self) -> str:
        return "UniformHeight"

    def solve(self, problem: Problem) -> Solution:
        """Solve using uniform height optimization."""
        start_time = time.time()

        print(f"\\n{'='*70}")
        print(f"Uniform Height Algorithm (统一高度优化算法)")
        print(f"{'='*70}")
        print(f"Specialized for items with same height dimension")
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

            # Pack using uniform height strategy
            packed_bins = self._pack_uniform_height(
                group_items, bin_type, problem.kerf
            )

            print(f"  Packed into {len(packed_bins)} boards")

            all_bins.extend(packed_bins)

        # Create solution
        solution = Solution(bins=all_bins, unplaced=all_unplaced)
        execution_time = time.time() - start_time
        solution.metadata["algorithm"] = self.get_name()
        solution.metadata["execution_time"] = execution_time

        return solution

    def _pack_uniform_height(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> List[BinPacking]:
        """
        Pack items with uniform height using 2-row systematic approach.

        Strategy:
        1. Since all items have same height, create 2-row patterns
        2. Sort items by width (longest first)
        3. Fill rows systematically to maximize width usage
        4. Create as few boards as possible
        """
        # Check if all items have the same height
        heights = set(item.height for item in items)

        if len(heights) == 1:
            # All same height - use NON-rotated 2-row packing
            common_height = list(heights)[0]
            print(f"    All items have height={common_height}mm")
            print(f"    Using 2-row systematic packing")

            num_rows_per_board = int((bin_type.height + kerf) / (common_height + kerf))
            print(f"    Can fit {num_rows_per_board} rows per board")

            return self._pack_same_height_2row(items, bin_type, kerf, common_height)
        else:
            # Mixed heights - fall back to greedy with rotation
            print(f"    Items have varying heights: {sorted(heights)}")
            print(f"    Using rotation-aware greedy packing")

            return self._pack_mixed_heights(items, bin_type, kerf)

    def _pack_same_height_2row(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        row_height: float
    ) -> List[BinPacking]:
        """
        Pack items with same height using 2-row patterns.

        This creates systematic patterns that should be highly reusable.
        """
        # Expand to individual pieces
        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        # Sort by width (longest first) for better bin packing
        all_pieces.sort(key=lambda x: -x.width)

        # Calculate how many rows fit per board
        num_rows = int((bin_type.height + kerf) / (row_height + kerf))
        num_rows = min(num_rows, 2)  # Use at most 2 rows for pattern simplicity

        print(f"    Total pieces: {len(all_pieces)}")
        print(f"    Using {num_rows}-row patterns")

        # Pack into boards
        boards = []
        piece_idx = 0

        while piece_idx < len(all_pieces):
            # Create one board with up to num_rows rows
            board_rows = []

            for row_num in range(num_rows):
                if piece_idx >= len(all_pieces):
                    break

                # Fill one row
                row = []
                row_width = 0.0

                while piece_idx < len(all_pieces):
                    piece = all_pieces[piece_idx]
                    needed_width = piece.width + (kerf if row else 0)

                    if row_width + needed_width <= bin_type.width:
                        row.append((piece, False))  # Not rotated
                        row_width += needed_width
                        piece_idx += 1
                    else:
                        break

                if row:
                    board_rows.append(row)

            # Create board from rows
            if board_rows:
                board = self._create_board(
                    board_rows, bin_type, kerf, len(boards)
                )
                boards.append(board)

        return boards

    def _pack_mixed_heights(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> List[BinPacking]:
        """Fallback for mixed heights - use original greedy algorithm."""
        from tessellate.algorithms.original_algorithm import OriginalAlgorithm
        algo = OriginalAlgorithm()

        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        used_indices = set()
        boards = []

        while len(used_indices) < len(all_pieces):
            pattern = algo._build_one_pattern_greedy(
                all_pieces, used_indices, bin_type, kerf
            )

            if pattern and pattern.rows:
                board = self._pattern_to_board(
                    pattern, bin_type, kerf, len(boards)
                )
                boards.append(board)
            else:
                break

        return boards

    def _create_board(
        self,
        rows: List[List[Tuple[Item, bool]]],
        bin_type: Bin,
        kerf: float,
        board_id: int
    ) -> BinPacking:
        """Create a BinPacking from rows."""
        placed_items = []
        y_position = 0.0

        for row in rows:
            x = 0.0
            for item, rotated in row:
                w = item.height if rotated else item.width
                h = item.width if rotated else item.height

                placed_items.append(PlacedItem(
                    item=item,
                    x=x,
                    y=y_position,
                    width=w,
                    height=h,
                    rotated=rotated
                ))
                x += w + kerf

            # Row height
            row_height = row[0][0].width if row[0][1] else row[0][0].height
            y_position += row_height + kerf

        return BinPacking(
            bin_id=board_id,
            bin_type=bin_type,
            items=placed_items
        )

    def _pattern_to_board(
        self,
        pattern,
        bin_type: Bin,
        kerf: float,
        board_id: int
    ) -> BinPacking:
        """Convert pattern to board."""
        return self._create_board(pattern.rows, bin_type, kerf, board_id)
