"""
Tessellate - 2D Guillotine Cutting Stock Optimization Library

A world-class library for solving the 2D Guillotine Cutting Stock Problem
with orientation constraints, kerf loss, and real-time performance requirements.

Author: Claude Code
Version: 1.0.0
License: MIT
"""

from tessellate.core.models import Item, Bin, PlacedItem, Solution, Problem
from tessellate.algorithms.hybrid import HybridSolver
from tessellate.core.validator import SolutionValidator

__version__ = "1.0.0"
__all__ = [
    "Item",
    "Bin",
    "PlacedItem",
    "Solution",
    "Problem",
    "HybridSolver",
    "SolutionValidator",
]


def solve(problem_data: dict, time_limit: float = 5.0) -> dict:
    """
    Main entry point for solving cutting stock problems.

    Args:
        problem_data: Dictionary containing items, bins, and parameters
        time_limit: Maximum execution time in seconds

    Returns:
        Solution dictionary with bins, items, and metadata
    """
    problem = Problem.from_dict(problem_data)
    solver = HybridSolver(time_limit=time_limit)
    solution = solver.solve(problem)
    return solution.to_dict()
