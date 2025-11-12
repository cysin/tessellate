"""
Column Generation Algorithm for 2D Guillotine Cutting Stock Problem.

This implements a pattern-based approach inspired by Branch-and-Price:
1. Generate cutting patterns using heuristics
2. Solve set covering problem using MIP to select optimal patterns
3. Minimize bins first, then minimize waste
"""

import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import highspy
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)
from tessellate.algorithms.guillotine import GuillotinePacker, SplitRule


@dataclass
class Pattern:
    """A cutting pattern for a single bin."""
    items: List[PlacedItem]  # Items in this pattern
    bin_type: Bin
    utilization: float
    total_area: float  # Total area of items in pattern

    def get_item_count(self, item_id: str) -> int:
        """Count how many of a specific item are in this pattern."""
        return sum(1 for pi in self.items if pi.item.id == item_id)


class ColumnGenerationPacker(PackingAlgorithm):
    """
    Column Generation based packing algorithm.

    This algorithm:
    1. Generates many feasible cutting patterns using various heuristics
    2. Formulates a set covering MIP to select the minimum number of patterns
    3. Uses two-stage optimization: minimize bins, then minimize waste
    """

    def __init__(self, time_limit: float = 300.0, num_patterns: int = 1000):
        """
        Initialize column generation packer.

        Args:
            time_limit: Maximum execution time
            num_patterns: Number of patterns to generate
        """
        super().__init__(time_limit)
        self.num_patterns = num_patterns

    def get_name(self) -> str:
        return "ColumnGeneration"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using column generation approach.

        Args:
            problem: Problem instance

        Returns:
            Optimal or near-optimal solution
        """
        start_time = time.time()

        # Group items by material (each group is independent)
        groups = problem.group_by_material()

        # Solve each group independently
        all_bins = []
        all_unplaced = []

        for (thickness, material), group_items in groups.items():
            print(f"\nSolving group: {material} {thickness}mm")
            print(f"  Items: {len(group_items)}, Total pieces: {sum(i.quantity for i in group_items)}")

            # Get compatible bins
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    all_unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Generate patterns for this group
            patterns = self._generate_patterns(
                group_items, bin_type, problem.kerf, start_time
            )
            print(f"  Generated {len(patterns)} patterns")

            # Solve set covering problem
            selected_patterns = self._solve_set_covering(
                group_items, patterns, start_time
            )
            print(f"  Selected {len(selected_patterns)} patterns")

            # Convert patterns to bins
            for pattern_idx in selected_patterns:
                pattern = patterns[pattern_idx]
                bin_packing = BinPacking(
                    bin_id=len(all_bins),
                    bin_type=pattern.bin_type,
                    items=pattern.items.copy()
                )
                all_bins.append(bin_packing)

        # Create solution
        solution = Solution(bins=all_bins, unplaced=all_unplaced)
        execution_time = time.time() - start_time
        solution.metadata["algorithm"] = self.get_name()
        solution.metadata["execution_time"] = execution_time

        return solution

    def _generate_patterns(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[Pattern]:
        """
        Generate many cutting patterns using various heuristics.

        Args:
            items: Items to pack
            bin_type: Bin type
            kerf: Kerf width
            start_time: Start time for timeout

        Returns:
            List of unique patterns
        """
        import random
        patterns = []
        seen_patterns = set()

        # Create item list with quantities
        items_to_pack = []
        for item in items:
            for _ in range(item.quantity):
                items_to_pack.append(item)

        # Try different sorting strategies
        sort_strategies = [
            ("area_desc", lambda x: -x.area()),
            ("area_asc", lambda x: x.area()),
            ("width_desc", lambda x: -x.width),
            ("height_desc", lambda x: -x.height),
            ("width_asc", lambda x: x.width),
            ("height_asc", lambda x: x.height),
            ("perimeter_desc", lambda x: -(x.width + x.height)),
            ("aspect_ratio", lambda x: -abs(x.width - x.height)),
            ("diagonal", lambda x: -(x.width**2 + x.height**2)**0.5),
        ]

        # Try different split rules
        split_rules = [
            SplitRule.SHORTER_LEFTOVER_AXIS,
            SplitRule.LONGER_LEFTOVER_AXIS,
            SplitRule.SHORTER_AXIS,
            SplitRule.LONGER_AXIS,
            SplitRule.HORIZONTAL,
            SplitRule.VERTICAL,
        ]

        # Generate patterns with different combinations
        for sort_name, sort_key in sort_strategies:
            if time.time() - start_time > self.time_limit * 0.7:
                break

            for split_rule in split_rules:
                if time.time() - start_time > self.time_limit * 0.7:
                    break

                # Sort items
                sorted_items = sorted(items_to_pack, key=sort_key)

                # Use guillotine packer to generate patterns
                packer = GuillotinePacker(time_limit=1.0, split_rule=split_rule)
                bins_result, _ = packer._pack_items_guillotine(
                    sorted_items, bin_type, kerf
                )

                # Add each bin as a pattern
                for bin_packing in bins_result:
                    # Create signature for deduplication (use looser dedup)
                    signature = self._pattern_signature_loose(bin_packing)
                    if signature not in seen_patterns or random.random() < 0.1:
                        seen_patterns.add(signature)

                        pattern = Pattern(
                            items=bin_packing.items,
                            bin_type=bin_type,
                            utilization=bin_packing.utilization(),
                            total_area=sum(pi.width * pi.height for pi in bin_packing.items)
                        )
                        patterns.append(pattern)

                        if len(patterns) >= self.num_patterns:
                            return patterns

                # Also try partial packs (first N items only) for more diversity
                for limit in [3, 5, 7, 10]:
                    if len(sorted_items) > limit:
                        partial_items = sorted_items[:limit]
                        bins_result, _ = packer._pack_items_guillotine(
                            partial_items, bin_type, kerf
                        )
                        for bin_packing in bins_result:
                            signature = self._pattern_signature_loose(bin_packing)
                            if signature not in seen_patterns:
                                seen_patterns.add(signature)
                                pattern = Pattern(
                                    items=bin_packing.items,
                                    bin_type=bin_type,
                                    utilization=bin_packing.utilization(),
                                    total_area=sum(pi.width * pi.height for pi in bin_packing.items)
                                )
                                patterns.append(pattern)

        # Add some random permutations for diversity
        for _ in range(100):
            if time.time() - start_time > self.time_limit * 0.7:
                break
            if len(patterns) >= self.num_patterns:
                break

            shuffled = items_to_pack.copy()
            random.shuffle(shuffled)

            for split_rule in [SplitRule.SHORTER_LEFTOVER_AXIS, SplitRule.LONGER_LEFTOVER_AXIS]:
                packer = GuillotinePacker(time_limit=1.0, split_rule=split_rule)
                bins_result, _ = packer._pack_items_guillotine(
                    shuffled, bin_type, kerf
                )

                for bin_packing in bins_result:
                    signature = self._pattern_signature_loose(bin_packing)
                    if signature not in seen_patterns:
                        seen_patterns.add(signature)
                        pattern = Pattern(
                            items=bin_packing.items,
                            bin_type=bin_type,
                            utilization=bin_packing.utilization(),
                            total_area=sum(pi.width * pi.height for pi in bin_packing.items)
                        )
                        patterns.append(pattern)

        # Special strategy: if items have same height, try strip packing
        heights = set(item.height for item in items)
        if len(heights) == 1:
            strip_patterns = self._generate_strip_patterns(
                items, items_to_pack, bin_type, kerf, start_time
            )
            for pattern in strip_patterns:
                if len(patterns) >= self.num_patterns:
                    break
                signature = self._pattern_signature_loose(
                    BinPacking(0, bin_type, pattern.items)
                )
                if signature not in seen_patterns:
                    seen_patterns.add(signature)
                    patterns.append(pattern)

        # CRITICAL: If items are rotatable and have same dimension, try ROTATED strip packing
        if all(item.rotatable for item in items) and len(heights) == 1:
            rotated_patterns = self._generate_rotated_strip_patterns(
                items, items_to_pack, bin_type, kerf, start_time
            )
            print(f"  Generated {len(rotated_patterns)} ROTATED patterns")
            for pattern in rotated_patterns:
                if len(patterns) >= self.num_patterns:
                    break
                signature = self._pattern_signature_loose(
                    BinPacking(0, bin_type, pattern.items)
                )
                if signature not in seen_patterns:
                    seen_patterns.add(signature)
                    patterns.append(pattern)

        return patterns

    def _generate_strip_patterns(
        self,
        items: List[Item],
        items_to_pack: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[Pattern]:
        """
        Generate patterns using strip packing for same-height items.

        When all items have the same height, we can pack them in rows/strips.
        """
        import random
        patterns = []
        common_height = items[0].height

        # Calculate how many rows can fit
        num_rows = int((bin_type.height + kerf) / (common_height + kerf))
        if num_rows == 0:
            return patterns

        row_capacity = bin_type.width

        # Try different item combinations for a single bin
        for _ in range(200):
            if time.time() - start_time > self.time_limit * 0.7:
                break

            # Randomly select items to try to pack
            sampled = random.sample(items_to_pack, min(len(items_to_pack), 20))

            # Try to pack these items into rows using FFD
            rows = [[] for _ in range(num_rows)]
            row_widths = [0.0] * num_rows

            # Sort by width descending
            sampled.sort(key=lambda x: -x.width)

            for item in sampled:
                # Find row with enough space (first fit)
                placed = False
                for row_idx in range(num_rows):
                    if row_widths[row_idx] + item.width + (kerf if rows[row_idx] else 0) <= row_capacity:
                        rows[row_idx].append(item)
                        row_widths[row_idx] += item.width + (kerf if rows[row_idx] else 0)
                        placed = True
                        break

                if not placed:
                    break

            # Create pattern from these rows
            if any(rows):
                placed_items = []
                for row_idx, row_items in enumerate(rows):
                    x = 0
                    y = row_idx * (common_height + kerf)
                    for item in row_items:
                        placed_items.append(PlacedItem(
                            item=item,
                            x=x,
                            y=y,
                            width=item.width,
                            height=common_height,
                            rotated=False
                        ))
                        x += item.width + kerf

                if placed_items:
                    total_area = sum(pi.width * pi.height for pi in placed_items)
                    utilization = total_area / bin_type.area()
                    pattern = Pattern(
                        items=placed_items,
                        bin_type=bin_type,
                        utilization=utilization,
                        total_area=total_area
                    )
                    patterns.append(pattern)

        return patterns

    def _generate_rotated_strip_patterns(
        self,
        items: List[Item],
        items_to_pack: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[Pattern]:
        """
        Generate patterns with ROTATED items for same-height items.

        When all items have dimension AxB (e.g., 336x554, 400x554),
        rotating them gives BxA (554x336, 554x400), which allows
        packing in horizontal rows with varying row heights.
        """
        import random
        random.seed(42)  # Deterministic seed for reproducible results
        patterns = []
        common_width_after_rotation = items[0].height  # All become this width when rotated

        # Calculate how many horizontal strips (rows with varying heights) fit
        # We can stack rows vertically as long as total height <=bin_type.height

        # Try different item combinations for high-utilization patterns
        for trial in range(5000):  # Generate many patterns for better coverage
            if time.time() - start_time > self.time_limit * 0.7:
                break

            # Randomly select items to pack - try different sizes
            if trial < 500:
                num_items = min(len(items_to_pack), random.randint(8, 15))
            else:
                num_items = min(len(items_to_pack), random.randint(5, 20))
            sampled = random.sample(items_to_pack, num_items)

            # Sort by rotated height (original width) to enable efficient packing
            sampled.sort(key=lambda x: x.width)  # width becomes height after rotation

            # Pack into rows (First Fit Decreasing by height)
            rows = []  # Each row will have items with same rotated height
            current_row = []
            current_row_width = 0
            current_y = 0

            for item in sampled:
                item_width_rot = item.height  # 554mm
                item_height_rot = item.width  # Varies (336-864mm)

                # Check if this item fits in current row
                if current_row and current_row[0].width == item.width:
                    # Same height as current row
                    if current_row_width + kerf + item_width_rot <= bin_type.width:
                        current_row.append(item)
                        current_row_width += kerf + item_width_rot
                        continue

                # Start new row
                row_height = item_height_rot
                if current_y + row_height <= bin_type.height:
                    # Finish current row
                    if current_row:
                        rows.append((current_row, current_y, current_row[0].width))
                        current_y += current_row[0].width + kerf  # width is rotated height

                    # Start new row
                    if current_y + row_height <= bin_type.height:
                        current_row = [item]
                        current_row_width = item_width_rot
                    else:
                        break
                else:
                    break

            # Add last row
            if current_row and current_y + current_row[0].width <= bin_type.height:
                rows.append((current_row, current_y, current_row[0].width))

            # Create pattern from rows
            if rows:
                placed_items = []
                for row_items, y_start, row_height in rows:
                    x = 0
                    for item in row_items:
                        placed_items.append(PlacedItem(
                            item=item,
                            x=x,
                            y=y_start,
                            width=item.height,  # Rotated: 554mm
                            height=item.width,  # Rotated: original width
                            rotated=True
                        ))
                        x += item.height + kerf

                if placed_items:
                    total_area = sum(pi.width * pi.height for pi in placed_items)
                    utilization = total_area / bin_type.area()
                    pattern = Pattern(
                        items=placed_items,
                        bin_type=bin_type,
                        utilization=utilization,
                        total_area=total_area
                    )
                    if utilization >= 0.5:  # Accept rotated patterns with 50%+ utilization
                        patterns.append(pattern)

        return patterns

    def _pattern_signature(self, bin_packing: BinPacking) -> tuple:
        """Create a unique signature for a pattern for deduplication."""
        # Sort items by position for consistency
        items_sig = tuple(sorted([
            (pi.item.id, pi.x, pi.y, pi.width, pi.height, pi.rotated)
            for pi in bin_packing.items
        ]))
        return items_sig

    def _pattern_signature_loose(self, bin_packing: BinPacking) -> tuple:
        """Create a looser signature based on item composition, not positions."""
        # Count items by ID and dimensions
        from collections import Counter
        items_counter = Counter([
            (pi.item.id, pi.width, pi.height)
            for pi in bin_packing.items
        ])
        return tuple(sorted(items_counter.items()))

    def _solve_set_covering(
        self,
        items: List[Item],
        patterns: List[Pattern],
        start_time: float
    ) -> List[int]:
        """
        Solve set covering problem to select minimum patterns.

        Uses lexicographic optimization:
        1. Primary: minimize number of bins
        2. Secondary: maximize total utilization (minimize waste)

        Args:
            items: Required items
            patterns: Available patterns
            start_time: Start time for timeout

        Returns:
            List of selected pattern indices
        """
        if not patterns:
            return []

        # Filter out patterns with very low utilization
        # Allow lower utilization if we have rotated patterns which can be more efficient overall
        min_util = 0.65  # Require at least 65% utilization
        good_patterns = [i for i, p in enumerate(patterns) if p.utilization >= min_util]

        if not good_patterns:
            # Fall back to all patterns if filtering too aggressive
            good_patterns = list(range(len(patterns)))
            min_util = min(p.utilization for p in patterns)

        print(f"  Using {len(good_patterns)}/{len(patterns)} patterns (utilization >= {min_util:.1%})")

        # Create MIP model
        h = highspy.Highs()
        h.setOptionValue("log_to_console", False)
        h.setOptionValue("mip_rel_gap", 0.0)  # Require exact optimality
        h.setOptionValue("time_limit", max(60.0, self.time_limit - (time.time() - start_time)))

        num_patterns = len(good_patterns)

        # Lexicographic objective: minimize bins, then maximize utilization
        # Use weighted sum: primary objective has much larger weight
        # obj = 10000 * num_patterns - total_area (stronger weight on bin count)
        bin_area = patterns[0].bin_type.area()
        obj_coeffs = [10000.0 - patterns[idx].total_area / bin_area for idx in good_patterns]

        # Variable bounds
        col_lower = [0.0] * num_patterns
        col_upper = [100.0] * num_patterns

        # Variable types (integer)
        var_types = [highspy.HighsVarType.kInteger] * num_patterns

        # Constraints: each item must be covered exactly (no overproduction)
        constraint_matrix = []
        row_lower = []
        row_upper = []

        for item in items:
            # Count how many of this item each pattern provides
            coeffs = []
            for p_idx in good_patterns:
                pattern = patterns[p_idx]
                count = pattern.get_item_count(item.id)
                coeffs.append(float(count))

            constraint_matrix.append(coeffs)
            row_lower.append(float(item.quantity))  # Exactly this many
            row_upper.append(float(item.quantity))  # No overproduction

        # Build model
        h.addVars(num_patterns, col_lower, col_upper)
        h.changeColsIntegrality(0, num_patterns - 1, var_types)
        h.changeColsCost(0, num_patterns - 1, obj_coeffs)

        # Add constraints
        for i, coeffs in enumerate(constraint_matrix):
            h.addRow(row_lower[i], row_upper[i], len(coeffs),
                    list(range(num_patterns)), coeffs)

        # Solve
        h.run()

        # Get solution
        model_status = h.getModelStatus()
        # Check if we have a solution
        if model_status == highspy.HighsModelStatus.kInfeasible:
            print(f"  Warning: MIP infeasible, using greedy fallback")
            return self._greedy_pattern_selection(items, patterns)
        elif model_status not in [highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kTimeLimit, highspy.HighsModelStatus.kSolutionLimit]:
            print(f"  Warning: MIP solver status = {model_status}")
            # Try to get solution anyway

        solution = h.getSolution()
        col_values = solution.col_value

        # Extract selected patterns
        selected = []
        for i, p_idx in enumerate(good_patterns):
            count = int(round(col_values[i]))
            for _ in range(count):
                selected.append(p_idx)

        return selected

    def _greedy_pattern_selection(
        self,
        items: List[Item],
        patterns: List[Pattern]
    ) -> List[int]:
        """
        Greedy fallback for pattern selection.

        Args:
            items: Required items
            patterns: Available patterns

        Returns:
            List of selected pattern indices
        """
        # Track remaining quantities
        remaining = {item.id: item.quantity for item in items}
        selected = []

        # Sort patterns by utilization (descending)
        sorted_patterns = sorted(enumerate(patterns), key=lambda x: -x[1].utilization)

        while any(qty > 0 for qty in remaining.values()):
            # Find best pattern that covers at least one needed item
            best_pattern = None
            best_score = -1

            for p_idx, pattern in sorted_patterns:
                # Count how many needed items this pattern provides
                coverage = sum(
                    min(pattern.get_item_count(item_id), remaining[item_id])
                    for item_id in remaining.keys()
                )

                if coverage > 0:
                    # Score = coverage * utilization
                    score = coverage * pattern.utilization
                    if score > best_score:
                        best_score = score
                        best_pattern = p_idx

            if best_pattern is None:
                break

            # Select this pattern
            selected.append(best_pattern)

            # Update remaining
            for item_id in remaining.keys():
                count = patterns[best_pattern].get_item_count(item_id)
                remaining[item_id] -= count

        return selected

    def _solve_set_covering_min_waste(
        self,
        items: List[Item],
        patterns: List[Pattern],
        num_bins: int,
        start_time: float
    ) -> List[int]:
        """
        Solve set covering with fixed number of bins, maximizing area usage.

        This is Stage 2: given optimal bin count, minimize waste.

        Args:
            items: Required items
            patterns: Available patterns
            num_bins: Fixed number of bins to use
            start_time: Start time for timeout

        Returns:
            List of selected pattern indices
        """
        if not patterns:
            return []

        # Create MIP model
        h = highspy.Highs()
        h.setOptionValue("log_to_console", False)
        h.setOptionValue("time_limit", max(1.0, self.time_limit - (time.time() - start_time)))

        num_patterns = len(patterns)

        # Objective: maximize total area (minimize waste)
        obj_coeffs = [-p.total_area for p in patterns]  # Negative for maximization

        # Variable bounds
        col_lower = [0.0] * num_patterns
        col_upper = [float(num_bins)] * num_patterns

        # Variable types (integer)
        var_types = [highspy.HighsVarType.kInteger] * num_patterns

        # Constraints
        constraint_matrix = []
        row_lower = []
        row_upper = []

        # 1. Each item must be covered
        for item in items:
            coeffs = []
            for pattern in patterns:
                count = pattern.get_item_count(item.id)
                coeffs.append(float(count))

            constraint_matrix.append(coeffs)
            row_lower.append(float(item.quantity))
            row_upper.append(1e6)

        # 2. Total patterns = num_bins
        coeffs = [1.0] * num_patterns
        constraint_matrix.append(coeffs)
        row_lower.append(float(num_bins))
        row_upper.append(float(num_bins))

        # Build model
        h.addVars(num_patterns, col_lower, col_upper)
        h.changeColsIntegrality(0, num_patterns - 1, var_types)
        h.changeColsCost(0, num_patterns - 1, obj_coeffs)

        # Add constraints
        for i, coeffs in enumerate(constraint_matrix):
            h.addRow(row_lower[i], row_upper[i], len(coeffs),
                    list(range(num_patterns)), coeffs)

        # Solve
        h.run()

        # Get solution
        solution = h.getSolution()
        col_values = solution.col_value

        # Extract selected patterns
        selected = []
        for p_idx in range(num_patterns):
            count = int(round(col_values[p_idx]))
            for _ in range(count):
                selected.append(p_idx)

        return selected
