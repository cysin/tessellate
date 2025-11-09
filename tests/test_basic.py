"""Basic tests for the tessellate library."""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tessellate import solve
from tessellate.core.models import Problem
from tessellate.core.validator import SolutionValidator


def test_simple_problem():
    """Test a simple packing problem."""
    problem_data = {
        "items": [
            {
                "id": "I001",
                "width": 600,
                "height": 400,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": True
            },
            {
                "id": "I002",
                "width": 500,
                "height": 300,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": True
            }
        ],
        "bins": [
            {
                "id": "B001",
                "width": 1220,
                "height": 2440,
                "thickness": 18,
                "material": "Oak",
                "available": -1
            }
        ],
        "parameters": {
            "kerf": 3.0,
            "utilizationThreshold": 0.75,
            "timeLimit": 5.0
        }
    }

    # Solve
    solution_dict = solve(problem_data, time_limit=5.0)

    # Verify solution structure
    assert "metadata" in solution_dict
    assert "bins" in solution_dict
    assert "unplaced" in solution_dict

    # Check that items were placed
    assert solution_dict["metadata"]["objectiveValue"] >= 1
    assert len(solution_dict["unplaced"]) == 0

    print("✓ Basic test passed!")
    print(f"  Bins used: {solution_dict['metadata']['objectiveValue']}")
    print(f"  Utilization: {solution_dict['metadata']['utilization']:.2%}")
    print(f"  Time: {solution_dict['metadata']['executionTime']:.3f}s")

    return True


if __name__ == "__main__":
    test_simple_problem()
