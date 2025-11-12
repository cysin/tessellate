"""
Test: Can we get HiGHS to actually solve a MIP with integer variables?
"""

import highspy

print("Testing HiGHS integrality...")

# Simple test: minimize x1 + x2 subject to x1 + x2 >= 3.5, x1,x2 integer
h = highspy.Highs()
h.setOptionValue("log_to_console", True)

# Add 2 integer variables
h.addVar(0, 10)  # x1
h.addVar(0, 10)  # x2

# Set as integer
h.changeColIntegrality(0, highspy.HighsVarType.kInteger)
h.changeColIntegrality(1, highspy.HighsVarType.kInteger)

# Objective: min x1 + x2
h.changeColCost(0, 1.0)
h.changeColCost(1, 1.0)

# Constraint: x1 + x2 >= 3.5
h.addRow(3.5, 100, 2, [0, 1], [1.0, 1.0])

print("\nSolving...")
h.run()

print(f"\nModel status: {h.getModelStatus()}")
sol = h.getSolution()
print(f"Solution: x1={sol.col_value[0]}, x2={sol.col_value[1]}")
print(f"Objective: {h.getInfo().objective_function_value}")

# Expected: x1=2, x2=2 (or x1=1, x2=3, etc) - should be INTEGERS
# If we get x1=1.75, x2=1.75, then integrality isn't working

if sol.col_value[0] == int(sol.col_value[0]) and sol.col_value[1] == int(sol.col_value[1]):
    print("\n✓ Variables are INTEGER - integrality is working!")
else:
    print(f"\n✗ Variables are FRACTIONAL - integrality NOT working!")
    print("This means HiGHS is ignoring the integer constraints.")
