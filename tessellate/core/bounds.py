"""
Lower bound calculations for the cutting stock problem.

Provides theoretical lower bounds on the optimal number of bins needed.
"""

import math
from typing import List
from tessellate.core.models import Item, Bin, Problem


class BoundsCalculator:
    """Calculate theoretical lower bounds for bin packing."""

    @staticmethod
    def area_lower_bound(items: List[Item], bin_type: Bin) -> int:
        """
        Calculate area-based lower bound.

        Args:
            items: List of items to pack
            bin_type: Bin type to pack into

        Returns:
            Lower bound on number of bins
        """
        total_area = sum(item.width * item.height * item.quantity for item in items)
        bin_area = bin_type.width * bin_type.height
        return math.ceil(total_area / bin_area)

    @staticmethod
    def dimension_lower_bound(items: List[Item], bin_type: Bin) -> int:
        """
        Calculate dimension-based lower bound.

        Items larger than half the bin dimension can't share that dimension.

        Args:
            items: List of items to pack
            bin_type: Bin type to pack into

        Returns:
            Lower bound based on dimensions
        """
        width_threshold = bin_type.width / 2
        height_threshold = bin_type.height / 2

        # Count items that must have dedicated bin space in each dimension
        large_width_count = sum(
            item.quantity
            for item in items
            if item.width > width_threshold and (not item.rotatable or item.height > width_threshold)
        )

        large_height_count = sum(
            item.quantity
            for item in items
            if item.height > height_threshold and (not item.rotatable or item.width > height_threshold)
        )

        return max(large_width_count, large_height_count)

    @staticmethod
    def combined_lower_bound(items: List[Item], bin_type: Bin) -> int:
        """
        Calculate combined lower bound (maximum of all bounds).

        Args:
            items: List of items to pack
            bin_type: Bin type to pack into

        Returns:
            Best lower bound
        """
        area_lb = BoundsCalculator.area_lower_bound(items, bin_type)
        dim_lb = BoundsCalculator.dimension_lower_bound(items, bin_type)
        return max(area_lb, dim_lb, 1)  # At least 1 bin

    @staticmethod
    def calculate_for_problem(problem: Problem) -> dict:
        """
        Calculate lower bounds for each material group in the problem.

        Args:
            problem: Problem instance

        Returns:
            Dictionary mapping (thickness, material) to lower bound
        """
        bounds = {}
        groups = problem.group_by_material()

        for (thickness, material), items in groups.items():
            # Find compatible bin
            compatible_bins = [
                b for b in problem.bins
                if b.thickness == thickness and b.material == material
            ]

            if compatible_bins:
                bin_type = compatible_bins[0]  # Use first compatible bin
                lb = BoundsCalculator.combined_lower_bound(items, bin_type)
                bounds[(thickness, material)] = lb

        return bounds
