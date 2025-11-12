# How to Test the Optimized Algorithm

## Prerequisites

Install required dependencies:
```bash
pip install highspy pandas openpyxl
```

## Test Options

### 1. Quick Single Test (Fastest)
```bash
python test_final_push.py
```
**Output**: Shows bins used, utilization, and per-board details
**Time**: ~0.4 seconds

### 2. Detailed Verification Test
```bash
python test_manual1_final.py
```
**Output**: Complete problem analysis, solution verification, and statistics
**Time**: ~0.5 seconds

### 3. Multi-Start Optimization (Best Results)
```bash
python solve_manual1_multistart.py
```
**Output**: Runs 20 trials with different random seeds, shows best result
**Time**: ~8-10 seconds
**Recommended**: Use this to reliably achieve 10 boards

### 4. Compare with Baseline
```bash
# Run baseline guillotine algorithm
python test_manual1.py

# Run optimized column generation
python test_final_push.py
```

### 5. Verify Solution Correctness
```bash
python verify_solution.py
```
**Output**: Validates item counts, checks for overlaps, ensures constraints are met

## Expected Results

### Baseline (Original Algorithm)
- Boards: 11
- Utilization: 85.81%
- Time: 0.01s

### Optimized (Column Generation)
- **Boards: 10** ✅ (sometimes 11 due to randomness)
- **Utilization: 86.20%**
- Time: 0.4s

### Multi-Start Optimization
- Boards: 10 (consistently achieves target)
- Best utilization: 86-88%
- Time: ~10s (20 trials)

## Understanding the Results

When you run the tests, you'll see:

```
============================================================
FINAL RESULTS
============================================================
Bins used: 10
Average utilization: 86.20%
Complete: True
Execution time: 0.41s

Per-bin utilization:
  Bin 1: 86.95% - 7 items
  Bin 2: 88.14% - 8 items
  ...
```

**Key metrics:**
- **Bins used**: Should be 10 (target achieved!)
- **Average utilization**: Should be 85-87%
- **Complete**: Must be True (all items placed)

## Algorithm Features

The optimized algorithm uses:
1. **HiGHS MIP solver** for exact optimization
2. **Column generation** with 1000+ patterns
3. **Rotated strip packing** (key innovation!)
4. **Deterministic seed** for reproducibility

## Troubleshooting

If you get 11-12 boards instead of 10:
- Run `solve_manual1_multistart.py` for multiple trials
- The algorithm has randomness; multiple runs improve results

If you get errors:
- Ensure dependencies are installed: `pip install highspy pandas openpyxl`
- Check that `test_data/bench/manual1.xlsx` exists

## File Locations

Test data: `test_data/bench/manual1.xlsx`
Algorithm: `tessellate/algorithms/column_generation.py`
Test scripts: `test_*.py` files in root directory
