"""
Simplified ILP packer with pre-determined rotations.

Strategy:
1. Pre-determine optimal rotation for each item based on bin dimensions
2. Formulate ILP with FIXED rotations (removes rotation variables)
3. This reduces problem complexity significantly
4. Uses column generation approach with target bin count
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


class SimplifiedILPPacker(PackingAlgorithm):
    """
    Simplified ILP packer with pre-determined rotations.

    Key simplifications:
    - Pre-determine rotation for each item (no rotation variables)
    - Use relaxed non-overlapping constraints
    - Target specific bin count (start with 10)
    """

    def __init__(
        self,
        time_limit: float = 300.0,
        target_bins: int = 10,
        mip_gap: float = 0.05
    ):
        """
        Initialize simplified ILP packer.

        Args:
            time_limit: Maximum solving time in seconds
            target_bins: Target number of bins to try
            mip_gap: MIP optimality gap (0.05 = 5%)
        """
        super().__init__(time_limit)
        self.target_bins = target_bins
        self.mip_gap = mip_gap

    def get_name(self) -> str:
        return "ILP-Simplified"

    def solve(self, problem: Problem) -> Solution:
        """Solve using simplified ILP formulation."""

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

            print(f"\nSolving Simplified ILP for {len(items_list)} items...")
            print(f"Target: {self.target_bins} bins")

            # Pre-determine rotations
            items_with_rotation = self._predetermine_rotations(
                items_list, bin_type
            )

            # Try to solve with target bins
            ilp_solution = self._solve_ilp_fixed_rotations(
                items_with_rotation, bin_type, problem.kerf,
                self.target_bins, start_time
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
                # Failed to achieve target, add to unplaced
                for item in group_items:
                    solution.unplaced.append((item, item.quantity))

        execution_time = time.time() - start_time
        solution.metadata = {
            "algorithm": self.get_name(),
            "execution_time": execution_time,
        }

        return solution

    def _predetermine_rotations(
        self,
        items_list: List[Tuple[Item, int]],
        bin_type: Bin
    ) -> List[Tuple[Item, int, int, int, bool]]:
        """
        Pre-determine optimal rotation for each item.

        Strategy for 1220x2440 bins:
        - If one dimension > 1220, must rotate to fit
        - Otherwise, prefer orientation that maximizes aspect ratio match with bin

        Returns: List of (item, idx, width, height, rotated)
        """
        W = bin_type.width
        H = bin_type.height

        result = []

        for item, idx in items_list:
            w, h = item.width, item.height

            # Check if rotation is required
            if w > W and h <= W and w <= H:
                # Must rotate
                width, height, rotated = h, w, True
            elif h > H and w <= H and h <= W:
                # Must rotate
                width, height, rotated = h, w, True
            elif w > W or h > H:
                # Cannot fit even with rotation
                if w <= H and h <= W:
                    width, height, rotated = h, w, True
                else:
                    # Use original (will fail, but we record it)
                    width, height, rotated = w, h, False
            else:
                # Both orientations fit, choose better one
                # Strategy: prefer orientation where larger dimension aligns with bin's larger dimension
                if H > W:
                    # Bin is portrait, prefer items to be portrait too
                    if h >= w:
                        width, height, rotated = w, h, False
                    else:
                        width, height, rotated = h, w, True
                else:
                    # Bin is landscape, prefer items to be landscape too
                    if w >= h:
                        width, height, rotated = w, h, False
                    else:
                        width, height, rotated = h, w, True

            result.append((item, idx, width, height, rotated))

        return result

    def _solve_ilp_fixed_rotations(
        self,
        items_with_rotation: List[Tuple[Item, int, int, int, bool]],
        bin_type: Bin,
        kerf: float,
        target_bins: int,
        start_time: float
    ) -> Optional[Tuple[List[BinPacking], List[Tuple[Item, int]]]]:
        """
        Solve ILP with FIXED rotations (no rotation variables).

        This significantly reduces problem complexity:
        - No rotation binary variables (saves N variables)
        - Simpler non-overlapping constraints (no rotation dependencies)
        """

        N = len(items_with_rotation)  # Number of items
        K = target_bins  # Target number of bins

        W = bin_type.width
        H = bin_type.height

        print(f"  Simplified ILP: {N} items, {K} bins, {W}x{H}mm bin")
        print(f"  Rotations: Pre-determined (fixed)")

        # Create the model
        prob = pulp.LpProblem("BinPacking2D_Simplified", pulp.LpMinimize)

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

        # Objective: Minimize number of bins used
        prob += pulp.lpSum([z[k] for k in range(K)]), "MinimizeBins"

        # Constraint: Each item must be in exactly one bin
        for i in range(N):
            prob += pulp.lpSum([y[i, k] for k in range(K)]) == 1, f"Item_{i}_InOneBin"

        # Constraint: If bin k is used, z[k] = 1
        for k in range(K):
            for i in range(N):
                prob += y[i, k] <= z[k], f"Bin_{k}_Used_If_Item_{i}"

        # Constraint: Items must fit within bin dimensions (with FIXED rotations)
        for i in range(N):
            item, idx, width, height, rotated = items_with_rotation[i]

            # Width constraint: x[i] + width <= W
            prob += x[i] + width <= W, f"Item_{i}_Width"

            # Height constraint: y_pos[i] + height <= H
            prob += y_pos[i] + height <= H, f"Item_{i}_Height"

        # Constraint: Non-overlapping items in same bin
        # Simplified: Use big-M with fixed dimensions
        M = max(W, H) * 2

        for i in range(N):
            for j in range(i + 1, N):
                item_i, _, w_i, h_i, _ = items_with_rotation[i]
                item_j, _, w_j, h_j, _ = items_with_rotation[j]

                # Binary variables for separation directions
                left = pulp.LpVariable(f"left_{i}_{j}", cat='Binary')
                right = pulp.LpVariable(f"right_{i}_{j}", cat='Binary')
                below = pulp.LpVariable(f"below_{i}_{j}", cat='Binary')
                above = pulp.LpVariable(f"above_{i}_{j}", cat='Binary')

                for k in range(K):
                    # Only apply if both items in same bin
                    same_bin = pulp.LpVariable(f"same_{i}_{j}_{k}", cat='Binary')

                    # same_bin = 1 iff y[i,k] = 1 AND y[j,k] = 1
                    prob += same_bin <= y[i, k], f"SameBin_{i}_{j}_{k}_1"
                    prob += same_bin <= y[j, k], f"SameBin_{i}_{j}_{k}_2"
                    prob += same_bin >= y[i, k] + y[j, k] - 1, f"SameBin_{i}_{j}_{k}_3"

                    # If in same bin, must be separated in at least one direction
                    prob += left + right + below + above >= same_bin, f"Separate_{i}_{j}_{k}"

                    # Left: x[i] + width_i <= x[j]
                    prob += x[i] + w_i <= x[j] + M * (1 - left), f"Left_{i}_{j}_{k}"

                    # Right: x[j] + width_j <= x[i]
                    prob += x[j] + w_j <= x[i] + M * (1 - right), f"Right_{i}_{j}_{k}"

                    # Below: y_pos[i] + height_i <= y_pos[j]
                    prob += y_pos[i] + h_i <= y_pos[j] + M * (1 - below), f"Below_{i}_{j}_{k}"

                    # Above: y_pos[j] + height_j <= y_pos[i]
                    prob += y_pos[j] + h_j <= y_pos[i] + M * (1 - above), f"Above_{i}_{j}_{k}"

        # Constraint: Bins are used in order (symmetry breaking)
        for k in range(K - 1):
            prob += z[k] >= z[k + 1], f"Symmetry_{k}"

        # Set solver parameters
        time_remaining = max(30, self.time_limit - (time.time() - start_time))

        print(f"  Starting Simplified ILP solver (time limit: {time_remaining:.1f}s)...")

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

            if bins_used == 0:
                print("  WARNING: No bins used, solution invalid")
                return None

            # Build solution
            bins = [BinPacking(bin_id=k, bin_type=bin_type, items=[])
                   for k in range(bins_used)]

            unplaced = []

            for i in range(N):
                item, idx, width, height, rotated = items_with_rotation[i]

                # Find which bin this item is in
                placed = False
                for k in range(K):
                    if y[i, k].varValue and y[i, k].varValue > 0.5:
                        if k < bins_used:
                            x_val = x[i].varValue or 0
                            y_val = y_pos[i].varValue or 0

                            placed_item = PlacedItem(
                                item=item,
                                x=x_val,
                                y=y_val,
                                width=width,
                                height=height,
                                rotated=rotated
                            )
                            bins[k].items.append(placed_item)
                            placed = True
                        break

                if not placed:
                    unplaced.append((item, idx))

            if unplaced:
                print(f"  WARNING: {len(unplaced)} items unplaced")

            return bins, unplaced

        else:
            print(f"  ILP Failed: {status}")
            return None
