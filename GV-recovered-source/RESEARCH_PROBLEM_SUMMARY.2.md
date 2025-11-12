# 2D Guillotine Bin Packing Problem - Quick Reference
## Research Problem Summary

**Full Specification:** See `RESEARCH_PROBLEM_SPECIFICATION.md` (130 pages)

---

## Problem in One Sentence

**Given rectangular furniture components with grain direction constraints, find the minimum number of stock sheets needed to cut all components using only guillotine cuts, accounting for blade width loss, while maximizing material utilization.**

---

## Quick Facts

| Property | Value |
|----------|-------|
| **Problem Class** | NP-Hard Combinatorial Optimization |
| **Domain** | Furniture Manufacturing, Cutting Stock |
| **Input Size** | 20-100 rectangular products |
| **Constraints** | 6 hard constraints + 2 soft constraints |
| **Objectives** | Minimize sheets (primary), maximize utilization (secondary) |
| **Time Limit** | <5 seconds for production use |
| **Current Best** | 75-80% utilization, non-deterministic |
| **Target** | 80-85% utilization, deterministic |

---

## Problem Definition (Simplified)

### Input

**Products (n = 20-100):**
- Dimensions: width × height (mm)
- Thickness: 12, 18, or 25 mm
- Material: Oak, Cherry, Walnut, etc.
- Quantity: 1-10 pieces each
- Grain constraint: 30-60% cannot rotate

**Stock Sheets:**
- Standard size: 1220×2440 mm (4×8 ft)
- Must match product thickness and material
- Unlimited availability

**Parameters:**
- Saw kerf (blade width): 3mm
- Minimum utilization: 78%
- Minimum leftover size: 200mm

### Output

**Cutting Plan:**
- Number of sheets used (minimize!)
- For each sheet:
  - Product placements (x, y, rotated)
  - Cutting sequence (guillotine cuts)
  - Leftover pieces
  - Utilization percentage

### Success Criteria

✅ All products placed
✅ No overlaps
✅ Guillotine cuts only
✅ Grain constraints respected
✅ Utilization ≥ 78%
✅ Execution time <5s

---

## Key Constraints (Must Satisfy)

### C1. Guillotine Cuts Only

```
All cuts must be straight lines from edge to edge

VALID:                    INVALID:
┌────────┬────────┐       ┌────────┬────────┐
│   P1   │   P2   │       │   P1   │   P2   │
├────────┴────────┤       │        ├────────┤ ← Partial cut!
│       P3        │       │   P3   │   P4   │
└─────────────────┘       └────────┴────────┘
```

### C2. Grain Direction

```
Directional products CANNOT rotate 90°

Product: Cabinet Door (grain vertical)
✓ CORRECT:        ✗ WRONG:
┌─────┐           ┌─────────┐
│  │  │           │  ─────  │ ← Horizontal grain (defect!)
│  │  │           └─────────┘
│  │  │
└─────┘
```

### C3. Saw Kerf (Blade Width)

```
Blade removes 3mm of material per cut

Original space: 1000mm
Product width: 600mm
Kerf: 3mm
Remaining: 1000 - 600 - 3 = 397mm

┌──────────┬─┬─────┐
│ Product  │k│ Rem │
│  600mm   │3│ 397 │
└──────────┴─┴─────┘
```

### C4. Material Matching

Products can ONLY be placed on sheets with:
- Same thickness (18mm ≠ 25mm)
- Same material (Oak ≠ Cherry)

### C5. Non-Overlap

Products cannot overlap (obvious but critical)

### C6. Boundary Constraints

All products must fit within sheet boundaries

---

## Objective Functions (Priority Order)

### 1. Minimize Sheets (PRIMARY)

```
minimize: number of sheets used

Example:
Solution A: 4 sheets @ 85% util = REJECT
Solution B: 3 sheets @ 78% util = ACCEPT ✓
```

### 2. Maximize Utilization (SECONDARY)

```
maximize: (used area) / (total sheet area)

Target: ≥ 80%
Acceptable: ≥ 75%
Excellent: ≥ 85%

Example:
Products: 7.2 m² total
Sheets: 3 × 2.98 m² = 8.93 m²
Utilization: 7.2 / 8.93 = 80.6% ✓
```

### 3. Leftover Quality (TERTIARY)

```
Prefer: Rectangular leftovers > L-shaped

Good Leftover:          Poor Leftover:
┌────────┬─────────┐   ┌────────┬───┬─┐
│Products│ Leftover│   │Products│ L │S│
│        │(1220×600│   │        │ S │M│
│        │  Rect)  │   │        │ H │A│
└────────┴─────────┘   └────────┴───┴─┘
```

---

## Example Problem

### Input

```
Products:
  P1: 2000×600×18mm Oak, qty=2, directional=true
  P2: 900×600×18mm Oak, qty=2, directional=false
  P3: 880×580×18mm Oak, qty=3, directional=false

Sheet: 1220×2440×18mm Oak
Saw kerf: 3mm
Min utilization: 78%
```

### Valid Solution

```
Sheet 1 (Utilization: 85.2%)
┌─────────────────────────────────────┐
│ P1         │ P2        │            │
│ 2000×600   │ 900×600   │  Leftover  │
│ (0,0)      │ (603,0)   │  317×2440  │
├────────────┴───────────┤            │
│ P1                     │            │
│ 2000×600               │            │
│ (0,603)                │            │
└────────────────────────┴────────────┘

Sheet 2 (Utilization: 79.1%)
┌─────────────────────────────────────┐
│ P2         │ P3        │            │
│ 900×600    │ 880×580   │  Leftover  │
│ (0,0)      │ (903,0)   │            │
├────────────┼───────────┤            │
│ P3         │ P3        │            │
│ 880×580    │ 880×580   │            │
│ (0,603)    │ (883,603) │            │
└────────────┴───────────┴────────────┘

Metrics:
- Sheets used: 2 ✓
- Avg utilization: 82.2% ✓
- All products placed: 8/8 ✓
- Grain constraints: OK ✓
- Guillotine cuts: Valid ✓
```

---

## Mathematical Formulation (Brief)

**Variables:**
- $x_{ij} \in \{0,1\}$: product $i$ on sheet $j$
- $r_i \in \{0,1\}$: product $i$ rotated
- $(x_i, y_i)$: product $i$ position
- $z_j \in \{0,1\}$: sheet $j$ used

**Objective:**
$$\min \sum_j z_j$$

**Subject to:**
- Coverage: $\sum_j x_{ij} = q_i$ ∀ products
- Non-overlap: $x_{ij} = x_{kj} = 1 \implies$ no overlap
- Boundaries: $x_i + w_i \leq W_j$, $y_i + h_i \leq H_j$
- Guillotine: Valid cutting sequence exists
- Grain: $d_i = 1 \implies r_i = 0$
- Kerf: $\text{distance}(p_i, p_k) \geq k$

---

## Current Algorithms (Baseline)

| Algorithm | Utilization | Time | Deterministic |
|-----------|-------------|------|---------------|
| **Current (Random Greedy)** | 75-80% | 4-5s | No |
| First Fit Decreasing | 70-75% | 1-2s | Yes |
| Best Fit Decreasing | 75-80% | 2-3s | Yes |
| Maximal Rectangles | 78-83% | 2-4s | Yes |
| Genetic Algorithm | 80-85% | 30-60s | No |
| ILP (Exact) | Optimal | Hours | Yes (impractical) |

**Challenge:** Achieve 80-85% utilization in <5 seconds deterministically

---

## Test Datasets

### Small (Validation)
- 8 products
- Optimal: 2 sheets, 82.7% util
- Purpose: Algorithm correctness

### Medium (Realistic)
- 23 products
- Target: 3-4 sheets, ≥80% util
- Purpose: Production scenarios

### Large (Stress Test)
- 100 products
- Target: 13-15 sheets, ≥78% util
- Purpose: Scalability

**Full benchmark suite:** 50 instances with known best solutions

---

## Research Challenges

1. **Near-Optimal in Polynomial Time**
   - Can we achieve 85%+ in O(n² log n)?

2. **Deterministic High Quality**
   - Eliminate randomness while maintaining performance

3. **Lookahead vs. Speed**
   - How much lookahead is worth the computational cost?

4. **Leftover Optimization**
   - Optimize for unknown future jobs

5. **Scalability**
   - Current: n ≤ 100, Goal: n ≤ 500

---

## Success Metrics

### Primary
- **M1:** Number of sheets used (lower = better)
- **M2:** Utilization rate (higher = better, target ≥80%)
- **M3:** Execution time (faster = better, target <5s)

### Secondary
- **M4:** Leftover quality (0-1 score, higher = better)
- **M5:** Pattern consolidation ratio
- **M6:** Solution determinism (same input → same output)

### Composite Score
$$S = 0.40 \cdot \frac{k_{opt}}{k_{sol}} + 0.30 \cdot \frac{U_{sol}}{U_{target}} + 0.15 \cdot \frac{T_{target}}{T_{sol}} + 0.15 \cdot Q_{leftover}$$

Target: $S \geq 0.90$

---

## How to Participate

1. **Read full specification:** `RESEARCH_PROBLEM_SPECIFICATION.md`

2. **Download benchmark:** `gv_benchmark_suite.zip`

3. **Implement algorithm** meeting constraints

4. **Validate solution** using provided validator

5. **Submit results** with:
   - Algorithm description
   - Results on all 50 instances
   - Source code (optional)
   - Research paper (optional)

6. **Leaderboard ranking** based on composite score

---

## Expected Impact

**Academic:**
- Novel variant of 2D cutting stock problem
- Combines guillotine + orientation + kerf constraints
- Real-world industrial application

**Industrial:**
- Annual savings: $40,000+ per factory
- Waste reduction: 5-10%
- Planning time: 90% reduction
- ROI: 3-4 months

**Benchmark:**
- 50 realistic instances
- Standardized evaluation
- Reproducible research

---

## Key Differences from Standard 2D Bin Packing

| Aspect | Standard 2D-BPP | This Problem |
|--------|----------------|--------------|
| Cuts | Any placement | Guillotine only ✓ |
| Rotation | Always allowed | Grain constraint ✓ |
| Spacing | Items touch | Saw kerf (3mm gap) ✓ |
| Materials | Homogeneous | Multiple types ✓ |
| Leftovers | Discard | Track & reuse ✓ |
| Patterns | N/A | Consolidate batches ✓ |
| Time limit | Academic | <5s real-time ✓ |

---

## Quick Start for Researchers

```python
# 1. Read problem instance
instance = load_json("benchmark/medium_01.json")

# 2. Implement your algorithm
def your_algorithm(products, sheets, params):
    # Your optimization logic here
    return solution

# 3. Solve
solution = your_algorithm(
    instance["products"],
    instance["sheets"],
    instance["parameters"]
)

# 4. Validate
validation = validate_solution(instance, solution)
assert validation["valid"], validation["errors"]

# 5. Evaluate
metrics = calculate_metrics(instance, solution)
print(f"Utilization: {metrics['utilization']:.1f}%")
print(f"Sheets: {metrics['sheets_used']}")
print(f"Time: {metrics['execution_time']:.2f}s")

# 6. Submit to leaderboard
submit_results(solution, metrics)
```

---

## Reference Implementation

Baseline implementation provided:
- Language: Java 7+ (for compatibility)
- Algorithm: Greedy + Random (current system)
- Performance: 75-80% utilization, 4-5s
- Location: `src/com/gv/service/ViewServiceR2.java`

Researchers can:
- Use as starting point
- Compare against baseline
- Implement in any language

---

## Citation

If you use this problem in your research, please cite:

```bibtex
@techreport{GV2D-CSP-2025,
  title={2D Guillotine Bin Packing Problem for Furniture Manufacturing},
  author={GV Research Team},
  year={2025},
  institution={Industrial Optimization Research},
  note={Research Problem Specification v1.0}
}
```

---

## Contact & Resources

**Full Specification:** `RESEARCH_PROBLEM_SPECIFICATION.md` (130 pages)
**Implementation Guide:** `IMPLEMENTATION_GUIDE.md` (35 pages)
**Algorithm Design:** `IMPROVED_ALGORITHM_DESIGN.md` (130 pages)
**Comparison:** `ALGORITHM_COMPARISON.md` (22 pages)

**Questions?** See full specification or contact research coordinator.

---

**Last Updated:** 2025-11-08
**Status:** Open for Research Submissions
**Difficulty:** Hard (NP-Hard, real-world constraints)
**Reward:** Potential for high-impact industrial deployment

---

**Happy Optimizing! 🔬📐**
