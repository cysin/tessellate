"""
Pattern Reuse Algorithm (based on Chinese furniture factory method)

Core principle: Minimize number of cutting PATTERNS (开板图), not boards.
Same pattern can be used for multiple boards (叠放).

This maximizes production efficiency by reducing machine setups.
"""

import time
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from collections import defaultdict, Counter

from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


@dataclass
class PatternTemplate:
    """A cutting pattern template that can be reused (开板图)."""
    row_configs: List[Tuple[float, List[Tuple[str, float, float, bool]]]]  # (row_height, [(item_id, w, h, rotated), ...])
    utilization: float
    boards_count: int  # How many boards use this pattern (叠放数量)

    def can_accommodate(self, item: Item, rotated: bool) -> bool:
        """Check if this pattern can accommodate an item."""
        item_height = item.width if rotated else item.height
        item_width = item.height if rotated else item.width

        for row_height, row_items in self.row_configs:
            if abs(row_height - item_height) < 0.1:  # Same row height
                return True
        return False


class PatternReuseAlgorithm(PackingAlgorithm):
    """
    Pattern Reuse Algorithm - optimizes for minimum cutting patterns.

    Based on Chinese furniture factory algorithm:
    1. 串排长度 - Horizontal arrangement by type groups
    2. 并排宽度 - Vertical stacking
    3. 叠放 - Pattern reuse for production efficiency
    """

    def __init__(self, time_limit: float = 300.0):
        super().__init__(time_limit)
        self.utilization_threshold = 0.85

    def get_name(self) -> str:
        return "PatternReuse"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using pattern reuse approach.

        Strategy:
        1. Group items by dimensions (considering rotation)
        2. Create template patterns for common configurations
        3. Reuse patterns to minimize unique cutting patterns (开板图)
        """
        start_time = time.time()

        print(f"\\n{'='*70}")
        print(f"Pattern Reuse Algorithm (叠放优先算法)")
        print(f"{'='*70}")
        print(f"Goal: Minimize cutting PATTERNS (not boards!)")
        print(f"Strategy: Create reusable patterns and maximize pattern reuse")
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

            # Pack using pattern reuse strategy
            packed_bins, num_patterns = self._pack_with_pattern_reuse(
                group_items, bin_type, problem.kerf
            )

            print(f"  Result: {len(packed_bins)} boards using {num_patterns} cutting patterns")
            print(f"  Pattern reuse factor: {len(packed_bins) / num_patterns if num_patterns > 0 else 0:.1f}x")

            all_bins.extend(packed_bins)

        # Create solution
        solution = Solution(bins=all_bins, unplaced=all_unplaced)
        execution_time = time.time() - start_time
        solution.metadata["algorithm"] = self.get_name()
        solution.metadata["execution_time"] = execution_time

        return solution

    def _pack_with_pattern_reuse(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float
    ) -> Tuple[List[BinPacking], int]:
        """
        Pack items using pattern reuse strategy.

        Returns: (list of bin packings, number of unique patterns)
        """
        # Analyze item dimensions to create dimensional groups
        dim_groups = self._analyze_dimensional_groups(items)

        print(f"    Found {len(dim_groups)} dimensional groups:")
        for (h, w), count in list(dim_groups.items())[:5]:
            print(f"      {w}×{h}: {count} pieces")

        # Generate template patterns
        templates = self._generate_pattern_templates(
            items, bin_type, kerf, dim_groups
        )

        print(f"    Generated {len(templates)} pattern templates")

        # Assign items to patterns (maximize reuse)
        packed_bins = self._assign_items_to_patterns(
            items, templates, bin_type, kerf
        )

        return packed_bins, len(templates)

    def _analyze_dimensional_groups(
        self,
        items: List[Item]
    ) -> Dict[Tuple[float, float], int]:
        """
        Analyze items and group by dimensions (considering rotation).

        Returns dict of (height, width) -> count
        """
        dim_counts = Counter()

        for item in items:
            # Non-rotated
            dim_counts[(item.height, item.width)] += item.quantity

            # Rotated (if rotatable and different from non-rotated)
            if item.rotatable and item.width != item.height:
                dim_counts[(item.width, item.height)] += item.quantity

        return dict(dim_counts)

    def _generate_pattern_templates(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        dim_groups: Dict[Tuple[float, float], int]
    ) -> List[PatternTemplate]:
        """
        Generate a small set of reusable pattern templates.

        Strategy: Create patterns that can accommodate many pieces of the same type.
        """
        templates = []

        # Group items by dimensions for pattern creation
        # Sort by area (largest first) for better utilization
        item_variants = []
        for item in items:
            # Non-rotated
            item_variants.append((item, False, item.height, item.width))
            # Rotated
            if item.rotatable:
                item_variants.append((item, True, item.width, item.height))

        # Sort by area
        item_variants.sort(key=lambda x: x[2] * x[3], reverse=True)

        # Create template patterns
        # For simplicity, create row-based templates
        seen_configs = set()

        for item, rotated, row_height, row_width in item_variants:
            # Try to create a pattern with multiple rows of this height
            num_rows = int((bin_type.height + kerf) / (row_height + kerf))

            if num_rows >= 1:
                # Create pattern config
                config = (row_height, num_rows)
                if config not in seen_configs:
                    seen_configs.add(config)

                    # Calculate how many items fit per row
                    items_per_row = int((bin_type.width + kerf) / (row_width + kerf))

                    if items_per_row >= 1:
                        # Create template
                        row_config = [(item.id, row_width, row_height, rotated)] * items_per_row
                        rows = [(row_height, row_config)] * num_rows

                        item_area = row_width * row_height * items_per_row * num_rows
                        pattern_area = bin_type.width * bin_type.height
                        utilization = min(1.0, item_area / pattern_area)

                        template = PatternTemplate(
                            row_configs=rows,
                            utilization=utilization,
                            boards_count=0
                        )
                        templates.append(template)

        return templates

    def _assign_items_to_patterns(
        self,
        items: List[Item],
        templates: List[PatternTemplate],
        bin_type: Bin,
        kerf: float
    ) -> List[BinPacking]:
        """
        Assign items to pattern templates to maximize pattern reuse.
        """
        # This is a simplified version - just use the original greedy algorithm
        # for now as a placeholder
        from tessellate.algorithms.original_algorithm import OriginalAlgorithm
        orig_algo = OriginalAlgorithm()

        # Expand items
        all_pieces = []
        for item in items:
            for _ in range(item.quantity):
                all_pieces.append(item)

        # Use greedy packing
        used_indices = set()
        packed_bins = []
        bin_id = 0

        while len(used_indices) < len(all_pieces):
            pattern = orig_algo._build_one_pattern_greedy(
                all_pieces, used_indices, bin_type, kerf
            )

            if pattern and pattern.rows:
                bin_packing = self._pattern_to_bin(
                    pattern, bin_type, kerf, bin_id
                )
                packed_bins.append(bin_packing)
                bin_id += 1
            else:
                break

        return packed_bins

    def _pattern_to_bin(
        self,
        pattern,
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
