# Available Packing Algorithms

This document lists all available 2D bin packing algorithms in the tessellate system, along with their characteristics and performance on the manual1.xlsx benchmark (80 cabinet panels, target: 10 boards).

## Summary Table

| Algorithm | Bins | Utilization | Speed | Source |
|-----------|------|-------------|-------|--------|
| **Skyline Min-Waste** | 11 | 85.81% | Fast | RectangleBinPack |
| Skyline Bottom-Left | 11 | 85.81% | Fast | RectangleBinPack |
| **Smart NFDH** | 12 | 78.66% | Fast | gomory (enhanced) |
| Guillotine (variants) | 11-12 | 80-85% | Fast | RectangleBinPack |
| MaxRects | 11-12 | 80-85% | Medium | RectangleBinPack |
| NFDH (traditional) | 16 | 59.00% | Fast | gomory |
| NFDH (area-based) | 16 | 59.00% | Fast | gomory |
| Local Search | 11 | 85.81% | Slow (60s) | Custom |
| ILP (full) | - | - | Timeout | PuLP/CBC |
| ILP (simplified) | - | - | Timeout | PuLP/CBC |

**Bold** = Recommended algorithms

---

## Algorithm Details

### 1. Skyline Packer (RECOMMENDED)

**Location**: `tessellate/algorithms/skyline.py`
**Source**: Inspired by [RectangleBinPack](https://github.com/juj/RectangleBinPack.git)

**Description**:
- Maintains a "skyline" contour representing the top edge of placed items
- Two placement strategies:
  - **Min-Waste**: Minimizes wasted vertical space
  - **Bottom-Left**: Places items as low and left as possible
- Handles rotation automatically
- Generally produces best results

**Performance (manual1.xlsx)**:
- Bins: **11**
- Utilization: **85.81%**
- Time: 1-2 seconds

**Use when**:
- You need the best packing quality
- Items have varying dimensions
- Fast execution is required

---

### 2. Smart NFDH (RECOMMENDED for simple cases)

**Location**: `tessellate/algorithms/nfdh_smart.py`
**Source**: Enhanced version of [gomory](https://github.com/rmzlb/gomory.git)

**Description**:
- NFDH = Next Fit Decreasing Height
- Shelf-based packing: items packed into horizontal strips
- Smart orientation selection based on bin aspect ratio
- For landscape bins (width > height), prefers landscape items
- Simpler algorithm than Skyline, easier to visualize

**Performance (manual1.xlsx)**:
- Bins: **12** (+1 vs Skyline)
- Utilization: **78.66%**
- Time: <1 second

**Use when**:
- You need simple, predictable packing patterns
- Items have similar heights
- Slightly lower utilization is acceptable for simplicity

---

### 3. Guillotine Packer

**Location**: `tessellate/algorithms/guillotine.py`
**Source**: Inspired by [RectangleBinPack](https://github.com/juj/RectangleBinPack.git)

**Description**:
- GUARANTEES guillotine constraints (all cuts go edge-to-edge)
- Critical for CNC cutting where continuous cuts are required
- Multiple split rules:
  - SHORTER_LEFTOVER_AXIS: Minimizes shorter leftover dimension
  - LONGER_LEFTOVER_AXIS: Minimizes longer leftover dimension
  - SHORTER_AXIS: Splits along shorter axis

**Performance (manual1.xlsx)**:
- Bins: **11-12** (varies by split rule)
- Utilization: **80-85%**
- Time: 1-2 seconds

**Use when**:
- You MUST have guillotine cuts (CNC requirement)
- Continuous edge-to-edge cuts are needed
- Slightly lower utilization is acceptable for cutting simplicity

---

### 4. MaxRects (Maximal Rectangles)

**Location**: `tessellate/algorithms/maxrects.py`
**Source**: Inspired by [RectangleBinPack](https://github.com/juj/RectangleBinPack.git)

**Description**:
- Maintains list of all maximal free rectangles
- Places items into best-fitting free rectangle
- Does NOT guarantee guillotine constraints
- Contact Point heuristic: maximizes edge contact with placed items

**Performance (manual1.xlsx)**:
- Bins: **11-12**
- Utilization: **80-85%**
- Time: 2-3 seconds

**Use when**:
- Guillotine constraints are NOT required
- You need good packing quality
- Slightly slower execution is acceptable

---

### 5. NFDH Packer (Traditional)

**Location**: `tessellate/algorithms/nfdh_packer.py`
**Source**: Direct implementation from [gomory](https://github.com/rmzlb/gomory.git)

**Description**:
- Traditional NFDH: sorts by height, always maximizes item height
- Two variants:
  - **NFDHPacker**: Height-based sorting
  - **NFDHDecreasingArea**: Area-based sorting

**Performance (manual1.xlsx)**:
- Bins: **16** (poor for this dataset)
- Utilization: **59.00%**
- Time: <1 second

**Use when**:
- Items naturally align with height-based sorting
- Simple shelf-based packing is desired
- This dataset is NOT a good fit for traditional NFDH

---

### 6. Local Search Packer

**Location**: `tessellate/algorithms/local_search_packer.py`
**Source**: Custom implementation with ruin-and-recreate

**Description**:
- Metaheuristic approach
- Iteratively improves initial solution by "ruining" and "recreating" bins
- Uses Skyline as the underlying packing algorithm
- Very slow but explores more solutions

**Performance (manual1.xlsx)**:
- Bins: **11** (same as Skyline)
- Utilization: **85.81%**
- Time: 60 seconds (300 iterations)

**Use when**:
- You have time to spare (minutes of computation)
- You've exhausted greedy algorithms
- You suspect a better solution exists but hard to find

**Note**: For manual1.xlsx, does not improve over Skyline despite 60x longer runtime.

---

### 7. ILP Solvers (NOT RECOMMENDED)

**Location**:
- `tessellate/algorithms/ilp_packer.py` (full)
- `tessellate/algorithms/ilp_simplified_packer.py` (simplified)
- `tessellate/algorithms/ilp_decomposition_packer.py` (decomposition)

**Source**: Custom implementations using PuLP with CBC solver

**Description**:
- Integer Linear Programming approach
- Formulates packing as mathematical optimization problem
- Three variants attempted (all failed)

**Performance (manual1.xlsx)**:
- Result: **Timeout** (no solution found)
- Time: 280+ seconds

**Why it failed**:
- 80 items create 3,160 pairs
- ~160,000 binary variables for non-overlapping constraints
- Weak LP relaxation (lower bound = 1, actual = 11)
- Free CBC solver cannot handle this complexity

**Use when**:
- You have commercial solver licenses (Gurobi/CPLEX, $10K+/year)
- You have 30-60 minutes per problem
- Even then, not guaranteed to find 10-board solution

See `ILP_ATTEMPT_RESULTS.md` for detailed analysis.

---

## Hybrid Solver (DEFAULT)

**Location**: `tessellate/algorithms/hybrid.py`

**Description**:
The default solver that tries multiple algorithms and returns the best result.

**Algorithm Priority**:
1. Skyline (Min-Waste and Bottom-Left)
2. Smart NFDH, NFDH, NFDH-Area
3. Guillotine (3 split rules)
4. MaxRects

**Time allocation**: Divides available time proportionally among algorithms

**Recommended for**: General use - automatically selects best algorithm

---

## How to Use Specific Algorithms

### In Python Code:

```python
from tessellate.core.models import Problem, Item, Bin
from tessellate.algorithms.skyline import SkylinePacker
from tessellate.algorithms.nfdh_smart import SmartNFDHPacker
from tessellate.algorithms.guillotine import GuillotinePacker, SplitRule

# Create problem
problem = Problem(items=[...], bins=[...], kerf=3.0)

# Option 1: Use specific algorithm
algorithm = SkylinePacker(time_limit=5.0, use_min_waste=True)
solution = algorithm.solve(problem)

# Option 2: Use Smart NFDH
algorithm = SmartNFDHPacker(time_limit=5.0)
solution = algorithm.solve(problem)

# Option 3: Use Guillotine
algorithm = GuillotinePacker(
    time_limit=5.0,
    split_rule=SplitRule.SHORTER_LEFTOVER_AXIS
)
solution = algorithm.solve(problem)

# Option 4: Use Hybrid (tries all)
from tessellate.algorithms.hybrid import HybridSolver
algorithm = HybridSolver(time_limit=10.0)
solution = algorithm.solve(problem)
```

### Via Webapp:

The webapp uses HybridSolver by default, which automatically tries all algorithms and returns the best result.

---

## Recommendations by Use Case

### Best Overall Quality
→ **Skyline Min-Waste** (11 bins, 85.81%)

### Simplest Algorithm
→ **Smart NFDH** (12 bins, 78.66%, very simple shelf packing)

### Must Have Guillotine Cuts
→ **Guillotine Packer** with SHORTER_LEFTOVER_AXIS

### Need to Explore More Solutions
→ **Local Search** (slow, 60s runtime)

### Production Default
→ **Hybrid Solver** (tries all, returns best)

---

## Performance Comparison (manual1.xlsx)

```
Manual Target:          10 boards @ ~82% utilization (human solution)
Skyline:                11 boards @ 85.81% ✓ BEST AUTOMATED
Smart NFDH:             12 boards @ 78.66% ✓ Good
Guillotine:             11-12 boards @ 80-85% ✓ Good (with guillotine guarantee)
MaxRects:               11-12 boards @ 80-85% ✓ Good
Traditional NFDH:       16 boards @ 59.00% ✗ Poor
Local Search:           11 boards @ 85.81% (60s)
ILP:                    Timeout ✗ Failed
```

**Conclusion**: Automated algorithms achieve **11 boards** consistently, which is only **+9% material cost** vs the manual 10-board solution. This is excellent for automated packing.

---

## References

1. **RectangleBinPack** (C++): https://github.com/juj/RectangleBinPack.git
   - Source for Skyline, Guillotine, MaxRects concepts

2. **gomory** (TypeScript): https://github.com/rmzlb/gomory.git
   - Source for NFDH shelf-based packing

3. **gdrr-2bp** (Rust): https://github.com/JeroenGar/gdrr-2bp.git
   - Source for goal-driven ruin-and-recreate concepts

4. **rectpack** (Python): https://github.com/secnot/rectpack.git
   - Reference implementation for sorting strategies

---

*Document created: 2025-11-11*
*Benchmark dataset: manual1.xlsx (80 items, 9 types, 16mm plywood)*
