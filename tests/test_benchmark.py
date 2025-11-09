"""Test with benchmark instance."""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tessellate import solve


def test_benchmark_example():
    """Test with the benchmark example."""
    # Load benchmark
    benchmark_path = os.path.join(
        os.path.dirname(__file__), '..', 'benchmarks', 'example_small.json'
    )

    with open(benchmark_path, 'r') as f:
        benchmark = json.load(f)

    problem_data = benchmark['problem']
    expected = benchmark['metadata']

    print(f"\n{'='*60}")
    print(f"Testing: {benchmark['name']}")
    print(f"Description: {benchmark['description']}")
    print(f"{'='*60}")

    # Solve
    solution = solve(problem_data, time_limit=5.0)

    # Display results
    print(f"\nResults:")
    print(f"  Bins used: {solution['metadata']['objectiveValue']} (expected: {expected['optimal_bins']})")
    print(f"  Utilization: {solution['metadata']['utilization']:.2%} (expected: {expected['expected_utilization']:.2%})")
    print(f"  Execution time: {solution['metadata']['executionTime']:.3f}s")
    print(f"  Algorithm: {solution['metadata']['algorithmName']}")

    if 'gap_percent' in solution['metadata']:
        print(f"  Gap to LB: {solution['metadata']['gap_percent']:.1f}%")

    # Check quality
    assert solution['metadata']['objectiveValue'] <= expected['optimal_bins'] + 1, \
        "Solution uses too many bins"
    assert solution['metadata']['utilization'] >= 0.70, \
        "Utilization too low"
    assert len(solution['unplaced']) == 0, \
        "Some items were not placed"

    # Show bin details
    print(f"\nBin Details:")
    for i, bin_data in enumerate(solution['bins']):
        print(f"  Bin {i+1}: {len(bin_data['items'])} items, {bin_data['utilization']:.2%} utilization")

    print(f"\n✓ Benchmark test passed!")
    return True


if __name__ == "__main__":
    test_benchmark_example()
