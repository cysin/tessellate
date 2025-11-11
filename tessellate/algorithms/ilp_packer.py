"""
Integer Linear Programming (ILP) based packer.

Uses PuLP with CBC solver to find optimal or near-optimal solutions.
Formulates 2D bin packing as a Mixed Integer Programming problem.
"""

import time
from typing import List, Tuple, Optional
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.core.models import (
    Problem, Solution, Item, Bin, BinPacking, PlacedItem
)

try:
    import pulp
    HAS_PULP = True
except ImportError:
    HAS_PULP = False


class ILPPacker(PackingAlgorithm):
    """
    ILP-based optimal packer using PuLP.

    Formulation:
    - Binary variables: which item goes in which bin
    - Continuous variables: x, y positions
    - Binary variables: rotation decisions
    - Constraints: non-overlapping, within bounds
    - Objective: minimize number of bins
    """

    def __init__(
        self,
        time_limit: float = 300.0,
        max_bins: int = 15,
        mip_gap: float = 0.05
    ):
        """
        Initialize ILP packer.

        Args:
            time_limit: Maximum solving time in seconds
            max_bins: Maximum number of bins to consider
            mip_gap: MIP optimality gap (0.05 = 5%)
        """
        super().__init__(time_limit)
        self.max_bins = max_bins
        self.mip_gap = mip_gap

    def get_name(self) -> str:
        return "ILP-Optimal"

    def solve(self, problem: Problem) -> Solution:
        """Solve using ILP formulation."""

        if not HAS_PULP:
            print("ERROR: PuLP not installed. Install with: pip install pulp")
            return Solution()

        start_time = time.time()

        # Group by material (solve each group separately)
        groups = problem.group_by_material()

        solution = Solution()

        for (thickness, material), group_items in groups.items():
            compatible_bins = problem.get_compatible_bins(group_items[0])
            if not compatible_bins:
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))
                continue

            bin_type = compatible_bins[0]

            # Expand items by quantity
            items_list = []
            for item in group_items:
                for q in range(item.quantity):
                    items_list.append((item, q))

            print(f"\nSolving ILP for {len(items_list)} items...")

            # Try to solve with ILP
            ilp_solution = self._solve_ilp(
                items_list, bin_type, problem.kerf, start_time
            )

            if ilp_solution:
                bins, unplaced = ilp_solution
                for bin_packing in bins:
                    bin_packing.bin_id = len(solution.bins)
                    solution.bins.append(bin_packing)

                if unplaced:
                    unplaced_counts = {}
                    for item, _ in unplaced:
                        unplaced_counts[item.id] = unplaced_counts.get(item.id, 0) + 1

                    for item in group_items:
                        if item.id in unplaced_counts:
                            solution.unplaced.append((item, unplaced_counts[item.id]))
            else:
                # ILP failed, add all to unplaced
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))

        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution

    def _solve_ilp(
        self,
        items_list: List[Tuple[Item, int]],
        bin_type: Bin,
        kerf: float,
        start_time: float
    ) -> Optional[Tuple[List[BinPacking], List[Tuple[Item, int]]]]:
        """
        Solve using ILP formulation.

        This uses a simplified formulation due to complexity:
        - Fix rotation for each item based on bin dimensions
        - Use big-M formulation for non-overlapping constraints
        - Minimize number of bins used
        """

        N = len(items_list)  # Number of items
        K = min(self.max_bins, N)  # Number of bins to consider

        W = bin_type.width
        H = bin_type.height

        print(f"  ILP Parameters: {N} items, {K} bins, {W}x{H}mm bin")

        # Create the model
        prob = pulp.LpProblem("BinPacking2D", pulp.LpMinimize)

        # Decision variables
        # y[i][k] = 1 if item i is in bin k
        y = pulp.LpVariable.dicts("y",
                                  ((i, k) for i in range(N) for k in range(K)),
                                  cat='Binary')

        # z[k] = 1 if bin k is used
        z = pulp.LpVariable.dicts("z", range(K), cat='Binary')

        # x[i], y_pos[i] = position of item i
        x = pulp.LpVariable.dicts("x", range(N), lowBound=0, upBound=W, cat='Continuous')
        y_pos = pulp.LpVariable.dicts("y_pos", range(N), lowBound=0, upBound=H, cat='Continuous')

        # r[i] = 1 if item i is rotated
        r = pulp.LpVariable.dicts("r", range(N), cat='Binary')

        # Objective: Minimize number of bins used
        prob += pulp.lpSum([z[k] for k in range(K)]), "MinimizeBins"

        # Constraint: Each item must be in exactly one bin
        for i in range(N):
            prob += pulp.lpSum([y[i, k] for k in range(K)]) == 1, f"Item_{i}_InOneBin"

        # Constraint: If bin k is used, z[k] = 1
        for k in range(K):
            for i in range(N):
                prob += y[i, k] <= z[k], f"Bin_{k}_Used_If_Item_{i}"

        # Constraint: Items must fit within bin dimensions
        M = max(W, H) * 2  # Big-M constant

        for i in range(N):
            item, _ = items_list[i]
            w_orig, h_orig = item.width, item.height

            # Width constraint: x[i] + width <= W
            # width = w_orig * (1 - r[i]) + h_orig * r[i]
            prob += x[i] + w_orig * (1 - r[i]) + h_orig * r[i] <= W, f"Item_{i}_Width"

            # Height constraint: y_pos[i] + height <= H
            # height = h_orig * (1 - r[i]) + w_orig * r[i]
            prob += y_pos[i] + h_orig * (1 - r[i]) + w_orig * r[i] <= H, f"Item_{i}_Height"

            # If item not rotatable, r[i] = 0
            if not item.rotatable:
                prob += r[i] == 0, f"Item_{i}_NoRotation"

        # Constraint: Non-overlapping items in same bin
        # This is the complex part - we need to ensure items don't overlap
        # Using big-M formulation with 4 separation constraints

        for i in range(N):
            for j in range(i + 1, N):
                item_i, _ = items_list[i]
                item_j, _ = items_list[j]

                w_i_orig, h_i_orig = item_i.width, item_i.height
                w_j_orig, h_j_orig = item_j.width, item_j.height

                # Binary variables for separation directions
                # At least one must be true if items in same bin
                left = pulp.LpVariable(f"left_{i}_{j}", cat='Binary')
                right = pulp.LpVariable(f"right_{i}_{j}", cat='Binary')
                below = pulp.LpVariable(f"below_{i}_{j}", cat='Binary')
                above = pulp.LpVariable(f"above_{i}_{j}", cat='Binary')

                # Width/height of items (considering rotation)
                # This is simplified - using max dimension as approximation
                max_w_i = max(w_i_orig, h_i_orig)
                max_h_i = max(w_i_orig, h_i_orig)
                max_w_j = max(w_j_orig, h_j_orig)
                max_h_j = max(w_j_orig, h_j_orig)

                for k in range(K):
                    # Only apply if both items in same bin
                    same_bin = pulp.LpVariable(f"same_{i}_{j}_{k}", cat='Binary')

                    # same_bin = 1 iff y[i,k] = 1 AND y[j,k] = 1
                    prob += same_bin <= y[i, k], f"SameBin_{i}_{j}_{k}_1"
                    prob += same_bin <= y[j, k], f"SameBin_{i}_{j}_{k}_2"
                    prob += same_bin >= y[i, k] + y[j, k] - 1, f"SameBin_{i}_{j}_{k}_3"

                    if same_bin:
                        # If in same bin, must be separated in at least one direction
                        prob += left + right + below + above >= same_bin, f"Separate_{i}_{j}_{k}"

                        # Left: x[i] + width_i <= x[j]
                        prob += x[i] + max_w_i <= x[j] + M * (1 - left), f"Left_{i}_{j}_{k}"

                        # Right: x[j] + width_j <= x[i]
                        prob += x[j] + max_w_j <= x[i] + M * (1 - right), f"Right_{i}_{j}_{k}"

                        # Below: y_pos[i] + height_i <= y_pos[j]
                        prob += y_pos[i] + max_h_i <= y_pos[j] + M * (1 - below), f"Below_{i}_{j}_{k}"

                        # Above: y_pos[j] + height_j <= y_pos[i]
                        prob += y_pos[j] + max_h_j <= y_pos[i] + M * (1 - above), f"Above_{i}_{j}_{k}"

        # Constraint: Bins are used in order (symmetry breaking)
        for k in range(K - 1):
            prob += z[k] >= z[k + 1], f"Symmetry_{k}"

        # Set solver parameters
        time_remaining = max(10, self.time_limit - (time.time() - start_time))

        print(f"  Starting ILP solver (time limit: {time_remaining:.1f}s)...")

        # Solve
        solver = pulp.PULP_CBC_CMD(
            timeLimit=time_remaining,
            gapRel=self.mip_gap,
            msg=1
        )

        prob.solve(solver)

        # Check solution status
        status = pulp.LpStatus[prob.status]
        print(f"  ILP Status: {status}")

        if prob.status in [pulp.LpStatusOptimal, pulp.LpStatusNotSolved]:
            # Extract solution
            bins_used = int(sum(z[k].varValue or 0 for k in range(K)))
            print(f"  ILP Solution: {bins_used} bins")

            # Build solution
            bins = [BinPacking(bin_id=k, bin_type=bin_type, items=[])
                   for k in range(bins_used)]

            for i in range(N):
                item, idx = items_list[i]

                # Find which bin this item is in
                for k in range(K):
                    if y[i, k].varValue and y[i, k].varValue > 0.5:
                        if k < bins_used:
                            x_val = x[i].varValue or 0
                            y_val = y_pos[i].varValue or 0
                            rotated = (r[i].varValue or 0) > 0.5

                            if rotated:
                                width, height = item.height, item.width
                            else:
                                width, height = item.width, item.height

                            placed = PlacedItem(
                                item=item,
                                x=x_val,
                                y=y_val,
                                width=width,
                                height=height,
                                rotated=rotated
                            )
                            bins[k].items.append(placed)
                        break

            return bins, []

        else:
            print(f"  ILP Failed: {status}")
            return None
