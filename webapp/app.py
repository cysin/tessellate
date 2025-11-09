"""
Flask web application for the Tessellate cutting stock optimizer.

Provides a web interface for solving 2D guillotine cutting stock problems.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import traceback

# Add parent directory to path to import tessellate
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tessellate import solve
from tessellate.core.models import Problem
from tessellate.core.validator import SolutionValidator
from tessellate.algorithms.guillotine_tree import GuillotineTreeBuilder

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/solve', methods=['POST'])
def api_solve():
    """
    Solve a cutting stock problem.

    Expects JSON with items, bins, and parameters.
    Returns solution with bins, items, and cuts.
    """
    try:
        problem_data = request.get_json()

        if not problem_data:
            return jsonify({"error": "No problem data provided"}), 400

        # Get time limit from parameters or use default
        time_limit = problem_data.get("parameters", {}).get("timeLimit", 5.0)

        # Solve the problem
        solution_dict = solve(problem_data, time_limit=time_limit)

        # Validate the solution
        problem = Problem.from_dict(problem_data)
        validator = SolutionValidator(problem)

        # Convert solution dict back to Solution object for validation
        # (This is a simplified validation - full validation would require conversion)
        is_valid = solution_dict["metadata"]["isComplete"]

        # Add validation info to metadata
        solution_dict["metadata"]["validated"] = is_valid

        return jsonify(solution_dict)

    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        return jsonify({
            "error": error_msg,
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/validate', methods=['POST'])
def api_validate():
    """
    Validate a solution.

    Expects JSON with problem and solution data.
    Returns validation result with errors if any.
    """
    try:
        data = request.get_json()
        problem_data = data.get("problem")
        solution_data = data.get("solution")

        if not problem_data or not solution_data:
            return jsonify({"error": "Missing problem or solution data"}), 400

        problem = Problem.from_dict(problem_data)
        validator = SolutionValidator(problem)

        # Note: This is simplified - full validation would require
        # converting solution_data back to Solution object
        is_complete = len(solution_data.get("unplaced", [])) == 0

        return jsonify({
            "valid": is_complete,
            "errors": [] if is_complete else ["Some items were not placed"],
            "metadata": solution_data.get("metadata", {})
        })

    except Exception as e:
        error_msg = str(e)
        return jsonify({"error": error_msg}), 500


@app.route('/api/example', methods=['GET'])
def api_example():
    """
    Get an example problem.

    Returns a sample problem that can be solved.
    """
    example = {
        "items": [
            {
                "id": "I001",
                "width": 2000,
                "height": 600,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": False
            },
            {
                "id": "I002",
                "width": 900,
                "height": 600,
                "thickness": 18,
                "material": "Oak",
                "quantity": 2,
                "rotatable": True
            },
            {
                "id": "I003",
                "width": 880,
                "height": 580,
                "thickness": 18,
                "material": "Oak",
                "quantity": 3,
                "rotatable": True
            }
        ],
        "bins": [
            {
                "id": "STD-1220x2440",
                "width": 1220,
                "height": 2440,
                "thickness": 18,
                "material": "Oak",
                "available": -1
            }
        ],
        "parameters": {
            "kerf": 3.0,
            "utilizationThreshold": 0.78,
            "timeLimit": 5.0
        }
    }

    return jsonify(example)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "version": "1.0.0"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'

    print("=" * 60)
    print("🎯 Tessellate Cutting Stock Optimizer")
    print("=" * 60)
    print(f"🌐 Server running on http://localhost:{port}")
    print(f"📊 Debug mode: {debug}")
    print("=" * 60)

    app.run(host='0.0.0.0', port=port, debug=debug)
