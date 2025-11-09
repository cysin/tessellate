"""
Solution validator for the 2D Guillotine Cutting Stock Problem.

Validates that solutions meet all constraints:
- All items placed
- No overlaps (with kerf spacing)
- Within bin boundaries
- Material matching
- Orientation constraints respected
- Utilization thresholds met
"""

from typing import List, Tuple
from tessellate.core.models import Solution, Problem, PlacedItem


class SolutionValidator:
    """Validates cutting stock solutions against problem constraints."""

    def __init__(self, problem: Problem):
        """
        Initialize validator with problem specification.

        Args:
            problem: Problem instance to validate against
        """
        self.problem = problem
        self.errors = []

    def validate(self, solution: Solution) -> Tuple[bool, List[str]]:
        """
        Validate a solution against all constraints.

        Args:
            solution: Solution to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        self.errors = []

        self._check_all_items_placed(solution)
        self._check_material_matching(solution)
        self._check_boundaries(solution)
        self._check_overlaps(solution)
        self._check_orientation_constraints(solution)
        self._check_utilization_thresholds(solution)

        return (len(self.errors) == 0, self.errors)

    def _check_all_items_placed(self, solution: Solution):
        """Verify all items are placed (coverage constraint)."""
        # Count placed items
        placed_counts = {}
        for bin_packing in solution.bins:
            for placed_item in bin_packing.items:
                item_id = placed_item.item.id
                placed_counts[item_id] = placed_counts.get(item_id, 0) + 1

        # Check against required quantities
        for item in self.problem.items:
            placed = placed_counts.get(item.id, 0)
            if placed < item.quantity:
                self.errors.append(
                    f"Item {item.id}: only {placed}/{item.quantity} placed"
                )
            elif placed > item.quantity:
                self.errors.append(
                    f"Item {item.id}: too many placed ({placed}/{item.quantity})"
                )

    def _check_material_matching(self, solution: Solution):
        """Verify items are only placed on compatible bins."""
        for bin_packing in solution.bins:
            bin_type = bin_packing.bin_type
            for placed_item in bin_packing.items:
                item = placed_item.item
                if item.thickness != bin_type.thickness:
                    self.errors.append(
                        f"Item {item.id} thickness {item.thickness} "
                        f"!= bin thickness {bin_type.thickness}"
                    )
                if item.material != bin_type.material:
                    self.errors.append(
                        f"Item {item.id} material {item.material} "
                        f"!= bin material {bin_type.material}"
                    )

    def _check_boundaries(self, solution: Solution):
        """Verify all items are within bin boundaries."""
        for bin_packing in solution.bins:
            bin_width = bin_packing.bin_type.width
            bin_height = bin_packing.bin_type.height
            for placed_item in bin_packing.items:
                if placed_item.x < 0 or placed_item.y < 0:
                    self.errors.append(
                        f"Item {placed_item.item.id} in bin {bin_packing.bin_id} "
                        f"has negative position ({placed_item.x}, {placed_item.y})"
                    )
                if placed_item.right() > bin_width + 0.01:  # Small tolerance for float
                    self.errors.append(
                        f"Item {placed_item.item.id} in bin {bin_packing.bin_id} "
                        f"exceeds bin width ({placed_item.right()} > {bin_width})"
                    )
                if placed_item.top() > bin_height + 0.01:
                    self.errors.append(
                        f"Item {placed_item.item.id} in bin {bin_packing.bin_id} "
                        f"exceeds bin height ({placed_item.top()} > {bin_height})"
                    )

    def _check_overlaps(self, solution: Solution):
        """Verify no items overlap (with kerf spacing)."""
        for bin_packing in solution.bins:
            items = bin_packing.items
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    if items[i].overlaps(items[j], self.problem.kerf):
                        self.errors.append(
                            f"Items {items[i].item.id} and {items[j].item.id} "
                            f"overlap in bin {bin_packing.bin_id} (kerf={self.problem.kerf})"
                        )

    def _check_orientation_constraints(self, solution: Solution):
        """Verify non-rotatable items are not rotated."""
        for bin_packing in solution.bins:
            for placed_item in bin_packing.items:
                item = placed_item.item
                if not item.rotatable and placed_item.rotated:
                    self.errors.append(
                        f"Item {item.id} is non-rotatable but was rotated "
                        f"in bin {bin_packing.bin_id}"
                    )

    def _check_utilization_thresholds(self, solution: Solution):
        """Verify bins meet minimum utilization threshold."""
        if len(solution.bins) <= 1:
            return  # Threshold doesn't apply to single bin

        for bin_packing in solution.bins:
            util = bin_packing.utilization()
            if util < self.problem.utilization_threshold - 0.01:  # Small tolerance
                self.errors.append(
                    f"Bin {bin_packing.bin_id} utilization {util:.2%} "
                    f"below threshold {self.problem.utilization_threshold:.2%}"
                )
