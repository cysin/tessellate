"""
Original Furniture Cutting Algorithm (原始开板算法)

Based on the Chinese furniture factory algorithm:
"由点成线→由线成面" (Point to Line → Line to Surface)

Key Concepts:
- 串排长度 (String Length): Horizontal arrangement of items
- 并排宽度 (Parallel Width): Vertical stacking of rows
- 叠放 (Stacking): Multiple boards use same cutting pattern
- Goal: Minimize number of cutting patterns (not number of boards!)

This differs from Western bin packing - the goal is production efficiency
through pattern reuse, not minimal material usage.
"""

import time
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from collections import defaultdict

from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


@dataclass
class CuttingPattern:
    """A cutting pattern that can be reused for multiple boards (开板图)."""
    rows: List[List[Tuple[Item, bool]]]  # List of rows, each row is list of (item, rotated)
    width: float  # Total pattern width
    height: float  # Total pattern height
    utilization: float
    boards_needed: int  # How many boards use this pattern (叠放数量)

    def __hash__(self):
        # For deduplication
        return hash((tuple(tuple((i.id, r) for i, r in row) for row in self.rows), self.width, self.height))


class OriginalAlgorithm(PackingAlgorithm):
    """
    Implementation of original Chinese furniture cutting algorithm.

    Optimizes for: Minimum number of cutting patterns (开板图)
    Not for: Minimum number of boards

    This maximizes production efficiency through pattern reuse.
    """

    def __init__(self, time_limit: float = 300.0):
        super().__init__(time_limit)
        self.utilization_threshold = 0.85  # 85% threshold for re-optimization

    def get_name(self) -> str:
        return "OriginalAlgorithm"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using original algorithm.

        Strategy:
        1. 串排长度: Group by width, arrange horizontally (long to short)
        2. 并排宽度: Stack rows vertically (wide to narrow)
        3. 叠放: Reuse patterns for multiple boards
        """
        start_time = time.time()

        print(f"\n{'='*70}")
        print(f"Original Furniture Cutting Algorithm (原始开板算法)")
        print(f"{'='*70}")
        print(f"Strategy: 串排长度 → 并排宽度 → 叠放")
        print(f"Goal: Minimize cutting patterns (not boards)")
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

            # Apply original algorithm
            patterns = self._generate_cutting_patterns(
                group_items, bin_type, problem.kerf
            )

            print(f"  Generated {len(patterns)} cutting patterns")
            print(f"  Total boards needed: {sum(p.boards_needed for p in patterns)}")

            # Convert patterns to BinPacking
            for pattern in patterns:
                for board_num in range(pattern.boards_needed):
                    bin_packing = self._pattern_to_bin(
                        pattern, bin_type, problem.kerf, len(all_bins)
                    )
                    all_bins.append(bin_packing)

        # Create solution
        solution = Solution(bins=all_bins, unplaced=all_unplaced)
        execution_time = time.time() - start_time
        solution.metadata["algorithm"] = self.get_name()
        solution.metadata["execution_time"] = execution_time
        solution.metadata["num_patterns"] = len(patterns) if 'patterns' in locals() else 0

        return solution

    def _generate_cutting_patterns(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> List[CuttingPattern]:
        """
        Generate cutting patterns using original algorithm.

        Step 1: 串排长度 - Horizontal arrangement by width groups
        Step 2: 并排宽度 - Vertical stacking of rows
        Step 3: 叠放 - Group identical patterns

        For rotatable items (混纹), try both orientations to maximize utilization.
        """
        patterns = []

        # Expand items to individual pieces with indices
        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        print(f"    Total pieces: {len(all_pieces)}")

        # Track which pieces have been used
        used_indices = set()

        # Generate patterns greedily
        while len(used_indices) < len(all_pieces):
            pattern = self._build_one_pattern_greedy(
                all_pieces, used_indices, bin_type, kerf
            )

            if pattern and pattern.rows:
                patterns.append(pattern)
            else:
                # Can't build more patterns, pack remaining items one by one
                break

        # Step 3: 叠放 - Group identical patterns
        patterns = self._consolidate_patterns(patterns)

        return patterns

    def _build_one_pattern_greedy(
        self,
        all_pieces: List[Item],
        used_indices: Set[int],
        bin_type: Bin,
        kerf: float
    ) -> Optional[CuttingPattern]:
        """
        Build one cutting pattern greedily using available pieces.

        Strategy:
        1. Group remaining pieces by possible row heights (with/without rotation)
        2. Stack rows from tall to short (并排宽度)
        3. Within each row, arrange long to short (串排长度)
        """
        remaining_indices = [i for i in range(len(all_pieces)) if i not in used_indices]
        if not remaining_indices:
            return None

        # Group remaining pieces by row height (considering rotation)
        # Each piece can appear in multiple groups if rotatable
        height_groups = defaultdict(list)
        for idx in remaining_indices:
            piece = all_pieces[idx]
            # Non-rotated
            height_groups[piece.height].append((idx, False))
            # Rotated (if rotatable)
            if piece.rotatable:
                height_groups[piece.width].append((idx, True))

        # Sort heights from tall to short
        sorted_heights = sorted(height_groups.keys(), reverse=True)

        # Build rows greedily
        rows = []
        current_y = 0.0
        pattern_used_indices = set()

        for row_height in sorted_heights:
            if current_y >= bin_type.height:
                break

            # Build one row at this height
            row, row_indices = self._build_one_row_greedy(
                all_pieces, remaining_indices, pattern_used_indices,
                height_groups[row_height], row_height, bin_type.width, kerf
            )

            if not row:
                continue

            # Check if row fits
            needed_height = row_height + (kerf if rows else 0)
            if current_y + needed_height > bin_type.height:
                break

            rows.append(row)
            current_y += needed_height
            pattern_used_indices.update(row_indices)

        if not rows:
            return None

        # Update used_indices
        used_indices.update(pattern_used_indices)

        # Calculate pattern stats
        total_width = max(
            sum(
                (all_pieces[idx].height if rot else all_pieces[idx].width) + kerf
                for idx, rot in row[:-1]
            ) + (all_pieces[row[-1][0]].height if row[-1][1] else all_pieces[row[-1][0]].width)
            if row else 0
            for row in rows
        )

        total_height = sum(
            (all_pieces[row[0][0]].width if row[0][1] else all_pieces[row[0][0]].height)
            for row in rows
        ) + kerf * (len(rows) - 1)

        item_area = sum(
            sum(all_pieces[idx].width * all_pieces[idx].height for idx, _ in row)
            for row in rows
        )
        pattern_area = bin_type.width * bin_type.height
        utilization = item_area / pattern_area

        # Convert to (item, rotated) format for compatibility
        rows_with_items = [
            [(all_pieces[idx], rot) for idx, rot in row]
            for row in rows
        ]

        return CuttingPattern(
            rows=rows_with_items,
            width=total_width,
            height=total_height,
            utilization=utilization,
            boards_needed=1
        )

    def _build_one_row_greedy(
        self,
        all_pieces: List[Item],
        remaining_indices: List[int],
        pattern_used_indices: Set[int],
        available_variants: List[Tuple[int, bool]],  # (piece_idx, rotated)
        row_height: float,
        max_length: float,
        kerf: float
    ) -> Tuple[List[Tuple[int, bool]], List[int]]:
        """
        Build one row greedily (串排长度).

        Returns: (row as list of (idx, rotated), list of used indices)
        """
        # Filter to pieces not yet used
        available = [
            (idx, rot)
            for idx, rot in available_variants
            if idx in remaining_indices and idx not in pattern_used_indices
        ]

        if not available:
            return [], []

        # Sort by horizontal length (long to short) - 长到短
        available.sort(
            key=lambda x: -(all_pieces[x[0]].height if x[1] else all_pieces[x[0]].width)
        )

        row = []
        row_indices = []
        current_length = 0.0

        for idx, rotated in available:
            # Horizontal length
            item_length = all_pieces[idx].height if rotated else all_pieces[idx].width

            needed_length = item_length + (kerf if row else 0)
            if current_length + needed_length <= max_length:
                row.append((idx, rotated))
                row_indices.append(idx)
                current_length += needed_length

        return row, row_indices

    def _build_one_pattern_with_rotation(
        self,
        height_groups: Dict[float, List[Tuple[Item, bool]]],
        sorted_heights: List[float],
        remaining_quantities: Dict[str, int],
        bin_type: Bin,
        kerf: float
    ) -> Optional[CuttingPattern]:
        """
        Build one cutting pattern considering rotation.

        串排长度: Arrange items horizontally within each row (same height)
        并排宽度: Stack rows vertically (tall to short)
        """
        rows = []
        current_y = 0.0

        for row_height in sorted_heights:
            if current_y >= bin_type.height:
                break

            # Get available pieces for this row height
            available_pieces = [
                (item, rotated)
                for item, rotated in height_groups[row_height]
                if remaining_quantities.get(item.id, 0) > 0
            ]

            if not available_pieces:
                continue

            # Build row with these pieces (串排长度)
            row = self._build_row_with_pieces(
                available_pieces, remaining_quantities, row_height,
                bin_type.width, kerf
            )

            if not row:
                continue

            # Check if row fits in remaining height
            needed_height = row_height + (kerf if rows else 0)
            if current_y + needed_height > bin_type.height:
                break

            rows.append(row)
            current_y += needed_height

        if not rows:
            return None

        # Calculate pattern dimensions and utilization
        total_width = max(
            sum(
                (item.height if rot else item.width) + kerf
                for item, rot in row[:-1]
            ) + (row[-1][0].height if row[-1][1] else row[-1][0].width)
            if row else 0
            for row in rows
        )

        total_height = sum(
            (row[0][0].width if row[0][1] else row[0][0].height)
            for row in rows
        ) + kerf * (len(rows) - 1)

        item_area = sum(
            sum(item.width * item.height for item, _ in row)
            for row in rows
        )
        pattern_area = bin_type.width * bin_type.height
        utilization = item_area / pattern_area

        return CuttingPattern(
            rows=rows,
            width=total_width,
            height=total_height,
            utilization=utilization,
            boards_needed=1
        )

    def _build_row_with_pieces(
        self,
        available_pieces: List[Tuple[Item, bool]],
        remaining_quantities: Dict[str, int],
        row_height: float,
        max_length: float,
        kerf: float
    ) -> List[Tuple[Item, bool]]:
        """
        Build one row from available piece variants (串排长度).

        Strategy:
        - Same row height
        - Sort by length (long to short)
        - Arrange horizontally to maximize width usage
        """
        if not available_pieces:
            return []

        # Remove duplicates - keep unique (item.id, rotated) combinations
        seen = set()
        unique_pieces = []
        for item, rotated in available_pieces:
            key = (item.id, rotated)
            if key not in seen and remaining_quantities.get(item.id, 0) > 0:
                seen.add(key)
                unique_pieces.append((item, rotated))

        # Sort by horizontal length (long to short) - 长到短
        unique_pieces.sort(
            key=lambda x: -(x[0].height if x[1] else x[0].width)
        )

        row = []
        current_length = 0.0
        used_item_ids = set()

        for item, rotated in unique_pieces:
            # Check if we still have this item available
            if item.id in used_item_ids:
                continue  # Already used one of this item in this row

            available = remaining_quantities.get(item.id, 0)
            if available <= 0:
                continue

            # Horizontal length when placed in row
            item_length = item.height if rotated else item.width

            needed_length = item_length + (kerf if row else 0)
            if current_length + needed_length <= max_length:
                row.append((item, rotated))
                current_length += needed_length
                used_item_ids.add(item.id)

        return row

    def _build_one_pattern(
        self,
        remaining_items: Dict[float, List[Item]],
        sorted_widths: List[float],
        bin_type: Bin,
        kerf: float
    ) -> Optional[CuttingPattern]:
        """
        Build one cutting pattern.

        串排长度: Arrange items horizontally (same width group)
        并排宽度: Stack rows vertically (wide to narrow)
        """
        rows = []
        current_y = 0.0

        for width in sorted_widths:
            if width not in remaining_items or not remaining_items[width]:
                continue

            # 串排长度: Build row with items of same width
            row = self._build_row(
                remaining_items[width], width, bin_type.width, kerf
            )

            if not row:
                continue

            # Check if row fits in remaining height
            row_height = width
            if current_y + row_height + (kerf if rows else 0) > bin_type.height:
                break

            rows.append(row)
            current_y += row_height + (kerf if rows else 0)

            # If we have enough rows, create pattern
            if len(rows) >= 2:  # At least 2 rows for efficiency
                break

        if not rows:
            return None

        # Calculate pattern dimensions and utilization
        total_width = max(
            sum((item.height if rot else item.width) + kerf for item, rot in row[:-1]) +
            (row[-1][0].height if row[-1][1] else row[-1][0].width)
            for row in rows
        )
        total_height = sum(
            (row[0][0].width if row[0][1] else row[0][0].height)
            for row in rows
        ) + kerf * (len(rows) - 1)

        item_area = sum(
            sum(item.width * item.height for item, _ in row)
            for row in rows
        )
        pattern_area = bin_type.width * bin_type.height
        utilization = item_area / pattern_area

        return CuttingPattern(
            rows=rows,
            width=total_width,
            height=total_height,
            utilization=utilization,
            boards_needed=1
        )

    def _build_row(
        self,
        available_items: List[Item],
        target_width: float,
        max_length: float,
        kerf: float
    ) -> List[Tuple[Item, bool]]:
        """
        Build one row (串排长度).

        Strategy:
        - Same width items
        - Sort by length (long to short)
        - Arrange horizontally
        - Try with/without rotation for rotatable items
        """
        if not available_items:
            return []

        # Sort by length (long to short) - 长到短
        sorted_items = sorted(available_items, key=lambda x: -x.width)

        row = []
        current_length = 0.0

        for item in sorted_items:
            # Try without rotation
            item_length = item.width
            item_width = item.height

            if item_width == target_width:
                needed_length = item_length + (kerf if row else 0)
                if current_length + needed_length <= max_length:
                    row.append((item, False))
                    current_length += needed_length
                    continue

            # Try with rotation if rotatable
            if item.rotatable:
                item_length = item.height
                item_width = item.width

                if item_width == target_width:
                    needed_length = item_length + (kerf if row else 0)
                    if current_length + needed_length <= max_length:
                        row.append((item, True))
                        current_length += needed_length

        return row

    def _consolidate_patterns(
        self,
        patterns: List[CuttingPattern]
    ) -> List[CuttingPattern]:
        """
        Consolidate identical patterns (叠放).

        Same cutting pattern can be used for multiple boards.
        This is the key to reducing number of cutting patterns!
        """
        pattern_map = defaultdict(int)

        for pattern in patterns:
            pattern_map[pattern] += 1

        consolidated = []
        for pattern, count in pattern_map.items():
            pattern.boards_needed = count
            consolidated.append(pattern)

        print(f"    Consolidated {len(patterns)} boards → {len(consolidated)} patterns")

        return consolidated

    def _pattern_to_bin(
        self,
        pattern: CuttingPattern,
        bin_type: Bin,
        kerf: float,
        bin_id: int
    ) -> BinPacking:
        """Convert cutting pattern to BinPacking."""
        placed_items = []
        y_position = 0.0

        for row in pattern.rows:
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
            bin_id=bin_id,
            bin_type=bin_type,
            items=placed_items
        )
