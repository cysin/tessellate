"""Base classes for packing algorithms."""

from abc import ABC, abstractmethod
from tessellate.core.models import Problem, Solution


class PackingAlgorithm(ABC):
    """Abstract base class for packing algorithms."""

    def __init__(self, time_limit: float = 5.0):
        """
        Initialize algorithm.

        Args:
            time_limit: Maximum execution time in seconds
        """
        self.time_limit = time_limit

    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        """
        Solve the packing problem.

        Args:
            problem: Problem instance

        Returns:
            Solution instance
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get algorithm name.

        Returns:
            Algorithm name string
        """
        pass
