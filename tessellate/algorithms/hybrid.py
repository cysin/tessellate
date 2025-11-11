"""
Hybrid solver combining multiple packing algorithms.

Tries multiple approaches and returns the best solution.
"""

import time
from typing import List
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.algorithms.guillotine import GuillotinePacker, SplitRule
from tessellate.algorithms.maxrects import MaximalRectanglesAlgorithm
from tessellate.algorithms.skyline import SkylinePacker
from tessellate.algorithms.nfdh_packer import NFDHPacker, NFDHDecreasingArea
from tessellate.algorithms.nfdh_smart import SmartNFDHPacker
from tessellate.core.models import Problem, Solution
from tessellate.core.bounds import BoundsCalculator


class HybridSolver(PackingAlgorithm):
    """
    Hybrid solver that tries multiple algorithms and strategies.

    This is the main entry point for solving cutting stock problems.
    """

    def __init__(self, time_limit: float = 5.0):
        """
        Initialize hybrid solver.

        Args:
            time_limit: Maximum execution time in seconds
        """
        super().__init__(time_limit)
        self.bounds_calculator = BoundsCalculator()

    def get_name(self) -> str:
        return "Hybrid-MultiStrategy"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using multiple algorithms and return best solution.

        Args:
            problem: Problem instance

        Returns:
            Best solution found
        """
        start_time = time.time()

        # Calculate lower bounds for comparison
        bounds = self.bounds_calculator.calculate_for_problem(problem)
        total_lower_bound = sum(bounds.values()) if bounds else 1

        # Try multiple algorithms with different configurations
        # PRIORITY 1: Skyline algorithms - often produce better packing with rotation
        # PRIORITY 2: NFDH algorithms - shelf-based packing from gomory
        # PRIORITY 3: Guillotine algorithms - GUARANTEE guillotine constraints
        algorithms = [
            SkylinePacker(time_limit=self.time_limit, use_min_waste=True),
            SkylinePacker(time_limit=self.time_limit, use_min_waste=False),
            SmartNFDHPacker(time_limit=self.time_limit),
            NFDHPacker(time_limit=self.time_limit),
            NFDHDecreasingArea(time_limit=self.time_limit),
            GuillotinePacker(time_limit=self.time_limit, split_rule=SplitRule.SHORTER_LEFTOVER_AXIS),
            GuillotinePacker(time_limit=self.time_limit, split_rule=SplitRule.LONGER_LEFTOVER_AXIS),
            GuillotinePacker(time_limit=self.time_limit, split_rule=SplitRule.SHORTER_AXIS),
            # MaxRects is kept for fallback but does NOT guarantee guillotine
            MaximalRectanglesAlgorithm(time_limit=self.time_limit, lookahead_depth=2),
        ]

        best_solution = None
        best_score = (float('inf'), float('-inf'))  # (bins, -utilization)

        for i, algorithm in enumerate(algorithms):
            # Allocate time proportionally
            time_left = self.time_limit - (time.time() - start_time)
            if time_left <= 0.1:
                break  # Not enough time for another algorithm

            # Set time limit for this algorithm
            algorithm.time_limit = time_left / (len(algorithms) - i)

            try:
                solution = algorithm.solve(problem)

                # Score solution (lexicographic: bins first, then utilization)
                score = (solution.num_bins(), -solution.total_utilization())

                if score < best_score:
                    best_score = score
                    best_solution = solution
                    best_solution.metadata["algorithm"] = algorithm.get_name()

            except Exception as e:
                # Continue with other algorithms if one fails
                print(f"Algorithm {algorithm.get_name()} failed: {e}")
                continue

        # If no solution found, return empty solution
        if best_solution is None:
            best_solution = Solution()
            best_solution.metadata = {
                "algorithm": self.get_name(),
                "execution_time": time.time() - start_time,
                "error": "No algorithm produced a solution"
            }
        else:
            # Update execution time
            best_solution.metadata["execution_time"] = time.time() - start_time
            best_solution.metadata["lower_bound"] = total_lower_bound
            best_solution.metadata["gap_percent"] = (
                (best_solution.num_bins() - total_lower_bound) / total_lower_bound * 100
                if total_lower_bound > 0 else 0
            )

        return best_solution
