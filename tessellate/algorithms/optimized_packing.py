"""
Optimized packing algorithm for special cases.

This handles the case where all items have the same height,
which allows for more efficient 1D-like packing strategies.
"""

import time
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)


class OptimizedSameHeightPacker(PackingAlgorithm):
    """
    Optimized packer for items with same height.

    Uses strip packing strategies when all items share the same height.
    """

    def __init__(self, time_limit: float = 300.0):
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "OptimizedSameHeight"

    def solve(self, problem: Problem) -> Solution:
        """Solve the packing problem."""
        start_time = time.time()

        # Group items by material
        groups = problem.group_by_material()

        all_bins = []
        all_unplaced = []

        for (thickness, material), group_items in groups.items():
            # Check if all items have the same height
            heights = set(item.height for item in group_items)
            if len(heights) == 1:
                # Use optimized same-height packing
                bins, unplaced = self._solve_same_height(
                    group_items, problem, start_time
                )
            else:
                # Fall back to simple packing
                bins, unplaced = self._solve_general(
                    group_items, problem, start_time
                )

            for bin_packing in bins:
                bin_packing.bin_id = len(all_bins)
                all_bins.append(bin_packing)

            all_unplaced.extend(unplaced)

        solution = Solution(bins=all_bins, unplaced=all_unplaced)
        solution.metadata["algorithm"] = self.get_name()
        solution.metadata["execution_time"] = time.time() - start_time

        return solution

    def _solve_same_height(
        self,
        items: List[Item],
        problem: Problem,
        start_time: float
    ) -> Tuple[List[BinPacking], List[Tuple[Item, int]]]:
        """
        Solve for items with same height using strip packing.

        When all items have the same height H, we can pack them in rows.
        This becomes a 1D bin packing problem with additional constraints.
        """
        # Get bin type
        compatible_bins = problem.get_compatible_bins(items[0])
        if not compatible_bins:
            return [], [(item, item.quantity) for item in items]

        bin_type = compatible_bins[0]
        kerf = problem.kerf

        # Common height
        common_height = items[0].height

        # Check if we can rotate items to use as rows
        use_rotation = all(item.rotatable for item in items)

        # Try different configurations
        best_solution = None
        best_bins = float('inf')

        # Config 1: Items as rows (original orientation)
        bins = self._pack_rows(items, bin_type, kerf, common_height, False)
        if len(bins) < best_bins:
            best_bins = len(bins)
            best_solution = bins

        # Config 2: Items rotated 90° (if allowed)
        if use_rotation:
            bins = self._pack_rows(items, bin_type, kerf, common_height, True)
            if len(bins) < best_bins:
                best_bins = len(bins)
                best_solution = bins

        # Config 3: Mixed strategy - pack as 2D with width optimization
        bins = self._pack_mixed_rows(items, bin_type, kerf, start_time)
        if len(bins) < best_bins:
            best_solution = bins

        return best_solution, []

    def _pack_rows(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        row_height: float,
        rotate: bool
    ) -> List[BinPacking]:
        """Pack items in rows."""
        # Create item list with quantities
        items_to_pack = []
        for item in items:
            for _ in range(item.quantity):
                items_to_pack.append(item)

        # Sort by width (descending) for better packing
        if not rotate:
            items_to_pack.sort(key=lambda x: -x.width)
        else:
            items_to_pack.sort(key=lambda x: -x.height)

        bins = []

        # Calculate how many rows fit in bin height
        effective_height = row_height if not rotate else items_to_pack[0].width
        num_rows = int((bin_type.height + kerf) / (effective_height + kerf))

        if num_rows == 0:
            return []

        while items_to_pack:
            # Create new bin
            bin_packing = BinPacking(bin_id=len(bins), bin_type=bin_type, items=[])

            # Pack items into rows
            for row_idx in range(num_rows):
                if not items_to_pack:
                    break

                # Start new row
                y = row_idx * (effective_height + kerf)
                x = 0

                # Pack items in this row
                row_items = []
                for item in items_to_pack[:]:
                    item_width = item.width if not rotate else item.height
                    item_height = item.height if not rotate else item.width

                    if x + item_width <= bin_type.width:
                        # Place item
                        placed = PlacedItem(
                            item=item,
                            x=x,
                            y=y,
                            width=item_width,
                            height=item_height,
                            rotated=rotate
                        )
                        bin_packing.items.append(placed)
                        row_items.append(item)
                        x += item_width + kerf

                # Remove placed items
                for item in row_items:
                    items_to_pack.remove(item)

            bins.append(bin_packing)

        return bins

    def _pack_mixed_rows(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> List[BinPacking]:
        """
        Pack using FFD (First Fit Decreasing) bin packing with row strategies.
        """
        import highspy

        # Create item list
        items_to_pack = []
        item_widths = []
        for item in items:
            for _ in range(item.quantity):
                items_to_pack.append(item)
                item_widths.append(item.width)

        n = len(items_to_pack)

        # Try to solve using MIP for optimal 1D bin packing
        # Variables: y[j] = 1 if bin j is used, x[i][j] = 1 if item i goes in bin j
        max_bins = n  # Upper bound

        h = highspy.Highs()
        h.setOptionValue("log_to_console", False)
        h.setOptionValue("time_limit", 10.0)  # Quick solve

        # Variables: x[i,j] for each item i and bin j, plus y[j] for bin usage
        num_vars = n * max_bins + max_bins

        # Objective: minimize sum of y[j]
        obj_coeffs = [0.0] * (n * max_bins) + [1.0] * max_bins

        # Bounds
        col_lower = [0.0] * num_vars
        col_upper = [1.0] * num_vars

        # Integer variables
        var_types = [highspy.HighsVarType.kInteger] * num_vars

        # Build model
        h.addVars(num_vars, col_lower, col_upper)
        h.changeColsIntegrality(0, num_vars - 1, var_types)
        h.changeColsCost(0, num_vars - 1, obj_coeffs)

        # Constraints
        # 1. Each item in exactly one bin
        for i in range(n):
            coeffs = [1.0] * max_bins
            indices = [i * max_bins + j for j in range(max_bins)]
            h.addRow(1.0, 1.0, len(indices), indices, coeffs)

        # 2. Bin capacity (width constraint per row)
        common_height = items_to_pack[0].height
        num_rows = int((bin_type.height + kerf) / (common_height + kerf))
        capacity_per_bin = bin_type.width * num_rows

        for j in range(max_bins):
            coeffs = [item_widths[i] for i in range(n)]
            coeffs.append(-capacity_per_bin)  # -capacity * y[j]
            indices = [i * max_bins + j for i in range(n)] + [n * max_bins + j]
            h.addRow(-1e10, 0.0, len(indices), indices, coeffs)

        # Solve
        h.run()
        model_status = h.getModelStatus()

        if model_status == highspy.HighsModelStatus.kOptimal or model_status == highspy.HighsModelStatus.kTimeLimit:
            solution = h.getSolution()
            col_values = solution.col_value

            # Extract bin assignments
            bins_dict = {}
            for i in range(n):
                for j in range(max_bins):
                    if col_values[i * max_bins + j] > 0.5:
                        if j not in bins_dict:
                            bins_dict[j] = []
                        bins_dict[j].append(items_to_pack[i])
                        break

            # Create bin packings with actual positions
            bins = []
            for j in sorted(bins_dict.keys()):
                bin_items = bins_dict[j]
                bin_packing = self._pack_items_in_rows(
                    bin_items, bin_type, kerf, common_height
                )
                bins.append(bin_packing)

            return bins

        # Fallback to simple FFD
        return self._pack_rows(items, bin_type, kerf, items[0].height, False)

    def _pack_items_in_rows(
        self,
        items: List[Item],
        bin_type: Bin,
        kerf: float,
        row_height: float
    ) -> BinPacking:
        """Pack a list of items into a single bin using rows."""
        bin_packing = BinPacking(bin_id=0, bin_type=bin_type, items=[])

        # Sort items by width descending
        sorted_items = sorted(items, key=lambda x: -x.width)

        # Calculate number of rows
        num_rows = int((bin_type.height + kerf) / (row_height + kerf))

        # Distribute items across rows
        row_idx = 0
        x = 0
        y = 0

        for item in sorted_items:
            if x + item.width > bin_type.width:
                # Move to next row
                row_idx += 1
                if row_idx >= num_rows:
                    # Bin full, shouldn't happen if MIP solution is correct
                    break
                x = 0
                y = row_idx * (row_height + kerf)

            # Place item
            placed = PlacedItem(
                item=item,
                x=x,
                y=y,
                width=item.width,
                height=row_height,
                rotated=False
            )
            bin_packing.items.append(placed)
            x += item.width + kerf

        return bin_packing

    def _solve_general(
        self,
        items: List[Item],
        problem: Problem,
        start_time: float
    ) -> Tuple[List[BinPacking], List[Tuple[Item, int]]]:
        """Fallback for general case."""
        from tessellate.algorithms.guillotine import GuillotinePacker
        packer = GuillotinePacker(time_limit=self.time_limit)
        solution = packer._solve_once(problem)
        return solution.bins, solution.unplaced
