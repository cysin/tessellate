"""
ULTRA-AGGRESSIVE Column Generation Algorithm

This is a highly tuned version with all parameters maxed out for deepest search.
Parameters:
- 1,000,000+ patterns
- Extended MIP time (hours)
- Very low utilization filter (40%)
- Massive pattern diversity (1000+ trials)
"""

import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict
import highspy
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)
from tessellate.algorithms.guillotine import GuillotinePacker, SplitRule


@dataclass
class Pattern:
    """A cutting pattern for a single bin."""
    items: List[PlacedItem]
    bin_type: Bin
    utilization: float
    total_area: float

    def get_item_count(self, item_id: str) -> int:
        return sum(1 for pi in self.items if pi.item.id == item_id)


class ColumnGenerationPackerUltra(PackingAlgorithm):
    """
    Ultra-aggressive column generation packer with all parameters maxed out.
    """

    def __init__(
        self,
        time_limit: float = 14400.0,  # 4 hours default
        num_patterns: int = 1_000_000,  # 1 million patterns
        min_utilization: float = 0.40,  # Very permissive
        mip_time_limit: float = 7200.0,  # 2 hours for MIP
        rotated_trials: int = 1000,  # Massive rotated pattern generation
        random_permutations: int = 1000,  # Many random attempts
    ):
        super().__init__(time_limit)
        self.num_patterns = num_patterns
        self.min_utilization = min_utilization
        self.mip_time_limit = mip_time_limit
        self.rotated_trials = rotated_trials
        self.random_permutations = random_permutations

    def get_name(self) -> str:
        return "ColumnGenerationUltra"

    def solve(self, problem: Problem) -> Solution:
        start_time = time.time()
        groups = problem.group_by_material()
        all_bins = []
        all_unplaced = []

        for (thickness, material), group_items in groups.items():
            print(f"\nSolving group: {material} {thickness}mm")
            print(f"  Items: {len(group_items)}, Total pieces: {sum(i.quantity for i in group_items)}")

            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    all_unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            patterns = self._generate_patterns(
                group_items, bin_type, problem.kerf, start_time
            )
            print(f"  Generated {len(patterns)} patterns")

            selected_patterns = self._solve_set_covering(
                group_items, patterns, start_time
            )
            print(f"  Selected {len(selected_patterns)} patterns")

            for pattern_idx in selected_patterns:
                pattern = patterns[pattern_idx]
                bin_packing = BinPacking(
                    bin_id=len(all_bins),
                    bin_type=pattern.bin_type,
                    items=pattern.items.copy()
                )
                all_bins.append(bin_packing)

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
        """Generate massive number of diverse patterns."""
        import random
        patterns = []
        seen_patterns = set()

        items_to_pack = []
        for item in items:
            for _ in range(item.quantity):
                items_to_pack.append(item)

        # EXPANDED: 20+ sort strategies
        sort_strategies = [
            ("area_desc", lambda x: -x.area()),
            ("area_asc", lambda x: x.area()),
            ("width_desc", lambda x: -x.width),
            ("height_desc", lambda x: -x.height),
            ("width_asc", lambda x: x.width),
            ("height_asc", lambda x: x.height),
            ("perimeter_desc", lambda x: -(x.width + x.height)),
            ("perimeter_asc", lambda x: x.width + x.height),
            ("aspect_ratio_high", lambda x: -max(x.width, x.height) / min(x.width, x.height)),
            ("aspect_ratio_low", lambda x: max(x.width, x.height) / min(x.width, x.height)),
            ("diagonal_desc", lambda x: -(x.width**2 + x.height**2)**0.5),
            ("diagonal_asc", lambda x: (x.width**2 + x.height**2)**0.5),
            ("most_square", lambda x: -abs(x.width - x.height)),
            ("least_square", lambda x: abs(x.width - x.height)),
            ("width_times_height", lambda x: -x.width * x.height),
            ("width_div_height", lambda x: -x.width / x.height if x.height > 0 else 0),
            ("height_div_width", lambda x: -x.height / x.width if x.width > 0 else 0),
            ("random1", lambda x: random.random()),
            ("random2", lambda x: random.random()),
            ("random3", lambda x: random.random()),
        ]

        # EXPANDED: ALL split rules
        split_rules = [
            SplitRule.SHORTER_LEFTOVER_AXIS,
            SplitRule.LONGER_LEFTOVER_AXIS,
            SplitRule.SHORTER_AXIS,
            SplitRule.LONGER_AXIS,
            SplitRule.HORIZONTAL,
            SplitRule.VERTICAL,
        ]

        # Generate patterns with all combinations
        for sort_name, sort_key in sort_strategies:
            if time.time() - start_time > self.time_limit * 0.6:
                break

            for split_rule in split_rules:
                if time.time() - start_time > self.time_limit * 0.6:
                    break

                sorted_items = sorted(items_to_pack, key=sort_key)

                packer = GuillotinePacker(time_limit=1.0, split_rule=split_rule)
                bins_result, _ = packer._pack_items_guillotine(
                    sorted_items, bin_type, kerf
                )

                for bin_packing in bins_result:
                    signature = self._pattern_signature_loose(bin_packing)
                    if signature not in seen_patterns or random.random() < 0.2:  # Allow more duplicates
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

                # EXPANDED: More partial pack sizes
                for limit in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25]:
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

        # EXPANDED: Many more random permutations
        for _ in range(self.random_permutations):
            if time.time() - start_time > self.time_limit * 0.6:
                break
            if len(patterns) >= self.num_patterns:
                break

            shuffled = items_to_pack.copy()
            random.shuffle(shuffled)

            for split_rule in split_rules:  # Try ALL split rules
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

        # Strip packing
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

        # CRITICAL: Rotated strip packing (MAXIMUM TRIALS)
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
        """Generate strip patterns (same height items)."""
        import random
        patterns = []
        common_height = items[0].height

        num_rows = int((bin_type.height + kerf) / (common_height + kerf))
        if num_rows == 0:
            return patterns

        row_capacity = bin_type.width

        # EXPANDED: More trials
        for _ in range(2000):  # 10x more
            if time.time() - start_time > self.time_limit * 0.6:
                break

            sampled = random.sample(items_to_pack, min(len(items_to_pack), 30))

            rows = [[] for _ in range(num_rows)]
            row_widths = [0.0] * num_rows

            sampled.sort(key=lambda x: -x.width)

            for item in sampled:
                placed = False
                for row_idx in range(num_rows):
                    if row_widths[row_idx] + item.width + (kerf if rows[row_idx] else 0) <= row_capacity:
                        rows[row_idx].append(item)
                        row_widths[row_idx] += item.width + (kerf if rows[row_idx] else 0)
                        placed = True
                        break

                if not placed:
                    break

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
        """Generate rotated strip patterns - ULTRA VERSION."""
        import random
        patterns = []
        common_width_after_rotation = items[0].height

        # ULTRA: Use configurable number of trials
        for trial in range(self.rotated_trials):
            if time.time() - start_time > self.time_limit * 0.6:
                break

            # Vary sample sizes more
            if trial < 100:
                num_items = min(len(items_to_pack), random.randint(10, 15))
            elif trial < 500:
                num_items = min(len(items_to_pack), random.randint(8, 20))
            else:
                num_items = min(len(items_to_pack), random.randint(5, 25))

            sampled = random.sample(items_to_pack, num_items)
            sampled.sort(key=lambda x: x.width)

            rows = []
            current_row = []
            current_row_width = 0
            current_y = 0

            for item in sampled:
                item_width_rot = item.height
                item_height_rot = item.width

                if current_row and current_row[0].width == item.width:
                    if current_row_width + kerf + item_width_rot <= bin_type.width:
                        current_row.append(item)
                        current_row_width += kerf + item_width_rot
                        continue

                row_height = item_height_rot
                if current_y + row_height <= bin_type.height:
                    if current_row:
                        rows.append((current_row, current_y, current_row[0].width))
                        current_y += current_row[0].width + kerf

                    if current_y + row_height <= bin_type.height:
                        current_row = [item]
                        current_row_width = item_width_rot
                    else:
                        break
                else:
                    break

            if current_row and current_y + current_row[0].width <= bin_type.height:
                rows.append((current_row, current_y, current_row[0].width))

            if rows:
                placed_items = []
                for row_items, y_start, row_height in rows:
                    x = 0
                    for item in row_items:
                        placed_items.append(PlacedItem(
                            item=item,
                            x=x,
                            y=y_start,
                            width=item.height,
                            height=item.width,
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
                    # VERY PERMISSIVE: Accept even low utilization patterns
                    if utilization >= self.min_utilization:
                        patterns.append(pattern)

        return patterns

    def _pattern_signature_loose(self, bin_packing: BinPacking) -> tuple:
        """Looser signature for more diversity."""
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
        """Solve set covering with extended MIP time."""
        if not patterns:
            return []

        # Use configurable min utilization
        good_patterns = [i for i, p in enumerate(patterns) if p.utilization >= self.min_utilization]

        if not good_patterns:
            good_patterns = list(range(len(patterns)))

        print(f"  Using {len(good_patterns)}/{len(patterns)} patterns (util >= {self.min_utilization:.0%})")

        h = highspy.Highs()
        h.setOptionValue("log_to_console", False)
        h.setOptionValue("mip_rel_gap", 0.0)
        # Use configurable MIP time limit
        h.setOptionValue("time_limit", self.mip_time_limit)

        num_patterns = len(good_patterns)

        bin_area = patterns[0].bin_type.area()
        obj_coeffs = [10000.0 - patterns[idx].total_area / bin_area for idx in good_patterns]

        col_lower = [0.0] * num_patterns
        col_upper = [100.0] * num_patterns

        constraint_matrix = []
        row_lower = []
        row_upper = []

        for item in items:
            coeffs = []
            for p_idx in good_patterns:
                pattern = patterns[p_idx]
                count = pattern.get_item_count(item.id)
                coeffs.append(float(count))

            constraint_matrix.append(coeffs)
            row_lower.append(float(item.quantity))
            row_upper.append(float(item.quantity))

        h.addVars(num_patterns, col_lower, col_upper)

        for i in range(num_patterns):
            h.changeColIntegrality(i, highspy.HighsVarType.kInteger)

        h.changeColsCost(0, num_patterns - 1, obj_coeffs)

        for i, coeffs in enumerate(constraint_matrix):
            h.addRow(row_lower[i], row_upper[i], len(coeffs),
                    list(range(num_patterns)), coeffs)

        h.run()

        model_status = h.getModelStatus()
        if model_status == highspy.HighsModelStatus.kInfeasible:
            print(f"  Warning: MIP infeasible, using greedy fallback")
            return self._greedy_pattern_selection(items, patterns)
        elif model_status not in [highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kTimeLimit, highspy.HighsModelStatus.kSolutionLimit]:
            print(f"  Warning: MIP solver status = {model_status}")

        solution = h.getSolution()
        col_values = solution.col_value

        selected = []
        for i, p_idx in enumerate(good_patterns):
            count = int(round(col_values[i]))
            for _ in range(count):
                selected.append(p_idx)

        # Validate
        item_coverage = defaultdict(int)
        for p_idx in selected:
            pattern = patterns[p_idx]
            for pi in pattern.items:
                item_coverage[pi.item.id] += 1

        is_valid = True
        for item in items:
            if item_coverage[item.id] != item.quantity:
                is_valid = False
                break

        if not is_valid:
            print(f"  Warning: MIP solution invalid, using greedy fallback")
            return self._greedy_pattern_selection(items, patterns)

        return selected

    def _greedy_pattern_selection(
        self,
        items: List[Item],
        patterns: List[Pattern]
    ) -> List[int]:
        """Greedy fallback."""
        remaining = {item.id: item.quantity for item in items}
        selected = []

        sorted_patterns = sorted(enumerate(patterns), key=lambda x: -x[1].utilization)

        while any(qty > 0 for qty in remaining.values()):
            best_pattern = None
            best_score = -1

            for p_idx, pattern in sorted_patterns:
                would_overproduce = False
                for item_id in remaining.keys():
                    count = pattern.get_item_count(item_id)
                    if count > remaining[item_id]:
                        would_overproduce = True
                        break

                if would_overproduce:
                    continue

                coverage = sum(
                    min(pattern.get_item_count(item_id), remaining[item_id])
                    for item_id in remaining.keys()
                )

                if coverage > 0:
                    score = coverage * pattern.utilization
                    if score > best_score:
                        best_score = score
                        best_pattern = p_idx

            if best_pattern is None:
                print(f"  Greedy: cannot satisfy remaining items")
                break

            selected.append(best_pattern)

            for item_id in remaining.keys():
                count = patterns[best_pattern].get_item_count(item_id)
                remaining[item_id] -= count

        return selected
