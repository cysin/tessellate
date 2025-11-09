"""
Scoring functions for placement decisions and solution quality.

Multi-criteria scoring for intelligent placement decisions.
"""

from typing import List, Tuple
import math
from tessellate.utils.geometry import Rectangle


class PlacementScorer:
    """Score placement positions using multiple criteria."""

    @staticmethod
    def score_placement(
        rect: Rectangle,
        item_width: float,
        item_height: float,
        bin_width: float,
        bin_height: float,
        weights: dict = None
    ) -> float:
        """
        Score a placement position using multiple criteria.

        Args:
            rect: Free rectangle being considered
            item_width: Width of item to place
            item_height: Height of item to place
            bin_width: Total bin width
            bin_height: Total bin height
            weights: Dictionary of weights for each criterion

        Returns:
            Composite score (higher is better)
        """
        if weights is None:
            weights = {
                "area_utilization": 0.35,
                "aspect_ratio": 0.25,
                "corner_distance": 0.20,
                "wastage": 0.20,
            }

        # Area utilization: how well does the item fill the free rectangle
        area_util = (item_width * item_height) / (rect.width * rect.height)

        # Aspect ratio matching: prefer rectangles with similar shape to item
        item_aspect = item_width / item_height if item_height > 0 else 1
        rect_aspect = rect.width / rect.height if rect.height > 0 else 1
        aspect_match = min(item_aspect, rect_aspect) / max(item_aspect, rect_aspect)

        # Corner distance: prefer bottom-left positions (for guillotine cuts)
        max_dist = math.sqrt(bin_width**2 + bin_height**2)
        corner_dist = math.sqrt(rect.x**2 + rect.y**2)
        corner_score = 1.0 - (corner_dist / max_dist)

        # Wastage: prefer placements with less leftover waste
        leftover_width = rect.width - item_width
        leftover_height = rect.height - item_height
        total_leftover = leftover_width * rect.height + leftover_height * item_width
        wastage_score = 1.0 - min(1.0, total_leftover / (rect.width * rect.height))

        # Weighted combination
        score = (
            weights["area_utilization"] * area_util +
            weights["aspect_ratio"] * aspect_match +
            weights["corner_distance"] * corner_score +
            weights["wastage"] * wastage_score
        )

        return score

    @staticmethod
    def best_short_side_fit(rect: Rectangle, item_width: float, item_height: float) -> float:
        """
        Best Short Side Fit heuristic score.

        Minimizes the leftover horizontal or vertical space.

        Args:
            rect: Free rectangle
            item_width: Item width
            item_height: Item height

        Returns:
            Score (lower is better, so return negative)
        """
        leftover_horizontal = rect.width - item_width
        leftover_vertical = rect.height - item_height
        return -min(leftover_horizontal, leftover_vertical)

    @staticmethod
    def best_long_side_fit(rect: Rectangle, item_width: float, item_height: float) -> float:
        """
        Best Long Side Fit heuristic score.

        Minimizes the leftover horizontal or vertical space (max).

        Args:
            rect: Free rectangle
            item_width: Item width
            item_height: Item height

        Returns:
            Score (lower is better, so return negative)
        """
        leftover_horizontal = rect.width - item_width
        leftover_vertical = rect.height - item_height
        return -max(leftover_horizontal, leftover_vertical)

    @staticmethod
    def best_area_fit(rect: Rectangle, item_width: float, item_height: float) -> float:
        """
        Best Area Fit heuristic score.

        Minimizes leftover area.

        Args:
            rect: Free rectangle
            item_width: Item width
            item_height: Item height

        Returns:
            Score (lower is better, so return negative)
        """
        leftover_area = rect.width * rect.height - item_width * item_height
        return -leftover_area

    @staticmethod
    def bottom_left(rect: Rectangle) -> float:
        """
        Bottom-Left heuristic score.

        Prefers positions closer to bottom-left corner.

        Args:
            rect: Free rectangle

        Returns:
            Score (lower is better, so return negative)
        """
        return -(rect.y * 1000 + rect.x)  # Prioritize y, then x


class SolutionScorer:
    """Score complete solutions."""

    @staticmethod
    def lexicographic_score(
        num_bins: int,
        utilization: float,
        lower_bound: int,
        target_utilization: float = 0.80
    ) -> Tuple[int, float]:
        """
        Lexicographic multi-objective score.

        Args:
            num_bins: Number of bins used
            utilization: Overall utilization
            lower_bound: Theoretical lower bound
            target_utilization: Target utilization

        Returns:
            Tuple for lexicographic comparison (bins, -utilization)
        """
        return (num_bins, -utilization)

    @staticmethod
    def composite_score(
        num_bins: int,
        utilization: float,
        execution_time: float,
        lower_bound: int,
        target_time: float = 5.0,
        target_util: float = 0.80
    ) -> float:
        """
        Composite benchmark score.

        Args:
            num_bins: Number of bins used
            utilization: Overall utilization
            execution_time: Execution time in seconds
            lower_bound: Theoretical lower bound
            target_time: Target time limit
            target_util: Target utilization

        Returns:
            Score between 0 and 1 (higher is better)
        """
        # Bins score (normalized by lower bound)
        bins_score = lower_bound / num_bins if num_bins > 0 else 0

        # Utilization score
        util_score = utilization / target_util

        # Time score (capped at 1.0)
        time_score = min(1.0, target_time / execution_time) if execution_time > 0 else 1.0

        # Weighted combination
        score = (
            0.40 * bins_score +
            0.30 * util_score +
            0.30 * time_score
        )

        return score
