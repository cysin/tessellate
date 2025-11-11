"""
Advanced packing strategies with multiple sorting heuristics.

This module implements advanced item sorting and placement strategies
to achieve better packing density.
"""

import time
from typing import List, Tuple, Callable
from tessellate.algorithms.base import PackingAlgorithm
from tessellate.algorithms.skyline import SkylinePacker
from tessellate.algorithms.guillotine import GuillotinePacker, SplitRule
from tessellate.core.models import Problem, Solution, Item


class AdvancedPacker(PackingAlgorithm):
    """
    Advanced packer that tries multiple sorting strategies
    to find the optimal packing.
    """

    def __init__(self, time_limit: float = 30.0):
        """
        Initialize advanced packer.

        Args:
            time_limit: Maximum execution time
        """
        super().__init__(time_limit)

    def get_name(self) -> str:
        return "Advanced-MultiSort"

    def solve(self, problem: Problem) -> Solution:
        """
        Solve using multiple sorting strategies.

        Args:
            problem: Problem instance

        Returns:
            Best solution found
        """
        start_time = time.time()

        # Define sorting strategies
        sorting_strategies = [
            ("area_desc", lambda item: (-item.area(), -item.width)),
            ("width_desc", lambda item: (-item.width, -item.height)),
            ("height_desc", lambda item: (-item.height, -item.width)),
            ("perimeter_desc", lambda item: (-(item.width + item.height), -item.width)),
            ("aspect_ratio", lambda item: (-abs(item.width - item.height), -item.area())),
            ("width_groups", lambda item: (-(item.width // 100), -item.height)),
            ("mixed_large_first", lambda item: (-max(item.width, item.height), -min(item.width, item.height))),
        ]

        # Define packing algorithms
        packing_algos = [
            ("Skyline-MW", lambda: SkylinePacker(time_limit=5.0, use_min_waste=True)),
            ("Skyline-BL", lambda: SkylinePacker(time_limit=5.0, use_min_waste=False)),
            ("Guillotine-SLA", lambda: GuillotinePacker(time_limit=5.0, split_rule=SplitRule.SHORTER_LEFTOVER_AXIS)),
            ("Guillotine-LLA", lambda: GuillotinePacker(time_limit=5.0, split_rule=SplitRule.LONGER_LEFTOVER_AXIS)),
        ]

        best_solution = None
        best_score = (float('inf'), float('inf'))

        attempts = 0
        for sort_name, sort_key in sorting_strategies:
            for algo_name, algo_factory in packing_algos:
                if time.time() - start_time > self.time_limit * 0.9:
                    break

                attempts += 1

                # Create modified problem with sorted items
                sorted_problem = self._create_sorted_problem(problem, sort_key)

                # Solve with this algorithm
                try:
                    solver = algo_factory()
                    solution = solver.solve(sorted_problem)

                    # Score: (num_bins, -utilization)
                    score = (solution.num_bins(), -solution.total_utilization())

                    if score < best_score:
                        best_score = score
                        best_solution = solution
                        best_solution.metadata["sort_strategy"] = sort_name
                        best_solution.metadata["packing_algo"] = algo_name
                        print(f"  Attempt {attempts}: {sort_name} + {algo_name} = {solution.num_bins()} bins, {solution.total_utilization():.2%}")

                except Exception as e:
                    continue

            if time.time() - start_time > self.time_limit * 0.9:
                break

        # Add metadata
        execution_time = time.time() - start_time
        if best_solution:
            best_solution.metadata["algorithm"] = self.get_name()
            best_solution.metadata["execution_time"] = execution_time
            best_solution.metadata["attempts"] = attempts

        return best_solution if best_solution else Solution()

    def _create_sorted_problem(
        self,
        problem: Problem,
        sort_key: Callable
    ) -> Problem:
        """
        Create a new problem with sorted items.

        Args:
            problem: Original problem
            sort_key: Function to sort items

        Returns:
            New problem with sorted items
        """
        # Expand items by quantity and sort
        expanded_items = []
        for item in problem.items:
            for _ in range(item.quantity):
                # Create a copy with quantity=1
                expanded_items.append(
                    Item(
                        id=item.id,
                        width=item.width,
                        height=item.height,
                        thickness=item.thickness,
                        material=item.material,
                        quantity=1,
                        rotatable=item.rotatable
                    )
                )

        # Sort expanded items
        expanded_items.sort(key=sort_key)

        # Group back by unique items
        item_groups = {}
        for item in expanded_items:
            key = (item.id, item.width, item.height, item.thickness, item.material)
            if key not in item_groups:
                item_groups[key] = Item(
                    id=item.id,
                    width=item.width,
                    height=item.height,
                    thickness=item.thickness,
                    material=item.material,
                    quantity=0,
                    rotatable=item.rotatable
                )
            item_groups[key].quantity += 1

        sorted_items = list(item_groups.values())

        # Create new problem
        return Problem(
            items=sorted_items,
            bins=problem.bins,
            kerf=problem.kerf
        )
