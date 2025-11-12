# 2D Guillotine Cutting Stock Problem - Research Brief
## Standalone Problem Definition

**Problem Type:** NP-Hard Combinatorial Optimization
**Application:** Industrial Sheet Cutting, Manufacturing Optimization

---

## Problem in One Sentence

Given rectangular items with orientation constraints, find the minimum number of stock sheets needed to cut all items using only guillotine cuts, accounting for material removal (kerf), while maximizing utilization.

---

## 1. Input

### Items to Cut (n = 20-100 typically)
- **Dimensions:** width × height (e.g., 600 × 2000 mm)
- **Thickness:** e.g., 12, 18, 25 mm
- **Material:** e.g., Oak, Cherry, Walnut
- **Quantity:** 1-10 copies of each item
- **Orientation:** 30-60% cannot rotate (directional grain)

### Stock Sheets (Bins)
- **Standard size:** 1220 × 2440 mm (4×8 ft typical)
- **Must match** item thickness and material
- **Unlimited** availability (or limited)

### Parameters
- **Kerf** (blade width): 3 mm (material removed per cut)
- **Utilization threshold:** 78% minimum
- **Time limit:** 5 seconds for production use

---

## 2. Constraints (All Must Be Satisfied)

### C1: Guillotine Cuts Only ✂️
```
All cuts must be straight edge-to-edge lines

✓ VALID:              ✗ INVALID:
┌────┬────┐           ┌────┬────┐
│ I1 │ I2 │           │ I1 │ I2 │
├────┴────┤           │    ├────┤ ← Partial cut
│   I3    │           │ I3 │ I4 │
└─────────┘           └────┴────┘
```

### C2: Orientation Constraints 🧭
- Some items have **directional grain** (wood pattern)
- Cannot be rotated 90° (would look wrong)
- Typical: 30-60% of items non-rotatable

### C3: Kerf Loss (Blade Width) 🔪
- Cutting blade **removes 3mm** of material
- Must account for in all calculations
- Minimum spacing between items = kerf width

### C4: Material Matching 🎨
- Items must match bin **thickness** and **material type**
- Example: 18mm Oak items → 18mm Oak bins only
- Problem decomposes by material groups

### C5: Standard Bin Packing Constraints 📦
- ✓ All items must be placed
- ✓ No overlaps
- ✓ Within bin boundaries

---

## 3. Objectives (Priority Order)

### PRIMARY: Minimize Bins Used
```
Fewer bins = lower material cost

Solution A: 4 bins @ 85% util → REJECT
Solution B: 3 bins @ 78% util → ACCEPT ✓
```

### SECONDARY: Maximize Utilization
```
Target: ≥ 80%
Good: ≥ 75%

Utilization = (used area) / (total bin area)
```

### TERTIARY: Leftover Quality
```
Prefer rectangular leftovers over L-shaped
Larger pieces better (reusable)
```

### CONSTRAINT: Time Limit
```
Must solve in < 5 seconds for production
```

---

## 4. Mathematical Formulation

**Minimize:**
$$Z_1 = \sum_{j} u_j \quad \text{(number of bins used)}$$

**Subject to:**
- **Coverage:** Every item placed exactly once
- **Non-overlap:** Items don't overlap + kerf spacing
- **Boundaries:** Items within bin dimensions
- **Guillotine:** Valid cutting sequence exists
- **Orientation:** Non-rotatable items not rotated
- **Material:** Items only on matching bins
- **Utilization:** Each bin meets threshold (except possibly last)

**Where:**
- $u_j \in \{0,1\}$: bin $j$ is used
- $x_{ij} \in \{0,1\}$: item $i$ on bin $j$
- $r_i \in \{0,1\}$: item $i$ rotated
- $(x_i, y_i)$: position of item $i$

---

## 5. Example Problem

### Input
```
Items:
  I1: 2000×600×18mm Oak, qty=2, non-rotatable
  I2: 900×600×18mm Oak, qty=2, rotatable
  I3: 880×580×18mm Oak, qty=3, rotatable

Bin: 1220×2440×18mm Oak
Kerf: 3mm
Threshold: 78%
```

### Valid Solution
```
BIN 1 (85.2% utilization):
┌────────────┬─────────┬─────────┐
│ I1         │ I2      │ Leftover│
│ 2000×600   │ 900×600 │ 317×    │
│            │         │ 2440    │
├────────────┴─────────┤         │
│ I1                   │         │
│ 2000×600             │         │
└──────────────────────┴─────────┘

BIN 2 (79.1% utilization):
┌─────────┬─────────┬──────────┐
│ I2      │ I3      │ Leftover │
│ 900×600 │ 880×580 │          │
├─────────┼─────────┤          │
│ I3      │ I3      │          │
│ 880×580 │ 880×580 │          │
└─────────┴─────────┴──────────┘

Result:
✓ Bins used: 2
✓ Avg utilization: 82.2%
✓ All items placed: 8/8
✓ Constraints: All satisfied
```

---

## 6. Complexity

**Class:** NP-Hard (proven via reduction from 2D Bin Packing)

**Search Space:** ≈ 10^100+ for n=20 items (infeasible to enumerate)

**Lower Bound:**
$$LB = \left\lceil \frac{\text{total item area}}{\text{bin area}} \right\rceil$$

**Gap:** Heuristic solutions typically 5-20% above lower bound

---

## 7. Evaluation Metrics

### Primary
- **M1:** Number of bins used (minimize)
- **M2:** Utilization rate (maximize, target ≥80%)
- **M3:** Execution time (minimize, target <5s)

### Secondary
- **M4:** Gap to lower bound (%)
- **M5:** Utilization std deviation (consistency)
- **M6:** Leftover quality score (0-1)

### Composite Score
$$S = 0.40 \cdot \frac{LB}{bins} + 0.30 \cdot \frac{util}{0.80} + 0.15 \cdot \frac{5s}{time} + 0.15 \cdot Q_{leftover}$$

Target: $S \geq 0.90$

---

## 8. Test Instances

### Small (n ≤ 20)
- **Purpose:** Validation, correctness
- **Time limit:** 2 seconds
- **Example:** 8 items, optimal = 2 bins

### Medium (n ≤ 50)
- **Purpose:** Realistic production
- **Time limit:** 5 seconds
- **Example:** 23 items, target = 3-4 bins

### Large (n ≤ 100)
- **Purpose:** Scalability
- **Time limit:** 10 seconds
- **Example:** 100 items, target = 13-15 bins

**Benchmark Suite:** 50 instances (10 small + 20 medium + 15 large + 5 special)

---

## 9. Research Challenges

### Open Questions
1. **Approximation ratio:** Can we achieve ρ < 1.5 in polynomial time?
2. **Guillotine price:** How much worse is guillotine vs. non-guillotine?
3. **Orientation impact:** How much does non-rotatability hurt?
4. **Lookahead value:** Does considering future items help significantly?
5. **Multi-period:** How to optimize for unknown future leftover reuse?

### Algorithmic Goals
- **Quality:** 80-85% utilization deterministically
- **Speed:** O(n² log n) time complexity
- **Provable:** Approximation guarantee
- **Practical:** Real-time performance (<5s)

---

## 10. Related Problems

### Differences from Standard 2D Bin Packing

| Aspect | Standard 2D-BPP | This Problem |
|--------|----------------|--------------|
| Cuts | Any placement | **Guillotine only** ✓ |
| Rotation | Always allowed | **Some fixed** ✓ |
| Spacing | Can touch | **Kerf gap (3mm)** ✓ |
| Materials | Homogeneous | **Multiple types** ✓ |
| Time | Academic | **Real-time (<5s)** ✓ |

### Similar Problems
- **2D Cutting Stock Problem** (without guillotine)
- **Strip Packing** (one dimension unbounded)
- **Rectangle Packing** (no cutting aspect)
- **Pallet Loading** (weight constraints)

**Key Difference:** Combination of guillotine + orientation + kerf + real-time is novel

---

## 11. Practical Impact

### Industry Context
- **Application:** Furniture manufacturing, cabinetry, sheet metal
- **Scale:** 1000+ cutting plans per factory per year
- **Material costs:** 40-60% of total manufacturing

### Economic Value
- **Waste reduction:** 5-10% (from 25% to 15-20%)
- **Cost savings:** $40,000+ per factory per year
- **Time savings:** 90% reduction in planning time
- **ROI:** 3-4 months

### Requirements
- **Real-time:** Must solve in seconds (not minutes)
- **Quality:** 80%+ utilization expected
- **Deterministic:** Same input → same output
- **Robust:** Handle varied product mixes

---

## 12. How to Participate

### Step 1: Read Full Specification
- Download: `RESEARCH_PROBLEM_STANDALONE.md`
- 60 pages, complete formal definition

### Step 2: Download Benchmark
- 50 test instances with validation data
- Known lower bounds and best solutions

### Step 3: Implement Algorithm
- Any language/approach
- Must satisfy all constraints
- Must run within time limits

### Step 4: Validate & Submit
- Use provided validator
- Submit results + algorithm description
- Optional: source code, research paper

### Step 5: Leaderboard
- Ranked by composite score
- Academic credit + potential industrial deployment

---

## 13. Quick Reference

### Input Example (JSON)
```json
{
  "items": [
    {"id": "I1", "width": 600, "height": 2000, "thickness": 18,
     "material": "Oak", "quantity": 2, "rotatable": false}
  ],
  "bins": [
    {"id": "B1", "width": 1220, "height": 2440, "thickness": 18,
     "material": "Oak", "available": -1}
  ],
  "parameters": {
    "kerf": 3.0,
    "utilizationThreshold": 0.78,
    "timeLimit": 5.0
  }
}
```

### Output Example (JSON)
```json
{
  "metadata": {
    "objectiveValue": 2,
    "utilization": 0.822,
    "executionTime": 1.3
  },
  "bins": [
    {
      "binId": 1,
      "utilization": 0.852,
      "items": [
        {"itemId": "I1", "x": 0, "y": 0, "width": 2000,
         "height": 600, "rotated": false}
      ]
    }
  ]
}
```

---

## 14. Key Insights

### Why This Problem is Hard
1. **NP-Hard complexity** (no polynomial exact algorithm)
2. **Guillotine constraint** reduces flexibility
3. **Orientation constraints** reduce rotation options by 50-90%
4. **Kerf loss** complicates dimension calculations
5. **Real-time requirement** eliminates slow exact methods

### Why This Problem is Important
1. **Real industrial need** (not academic toy problem)
2. **Significant economic impact** ($40k+ savings/factory)
3. **Novel constraint combination** (research contribution)
4. **Benchmark opportunity** (standardized evaluation)
5. **Deployment potential** (production implementation)

### Success Criteria
- ✓ 80-85% utilization (good quality)
- ✓ <5 seconds execution (practical)
- ✓ Deterministic (reproducible)
- ✓ Handles 100 items (scalable)
- ✓ Satisfies all constraints (valid)

---

## 15. References

**Foundational:**
- Gilmore & Gomory (1961): Cutting stock problem
- Lodi et al. (2002): 2D packing survey
- Wäscher et al. (2007): Problem typology

**Guillotine:**
- Christofides & Whitlock (1977): Guillotine algorithms
- Beasley (1985): Unconstrained guillotine

**Heuristics:**
- Burke et al. (2004): Placement heuristics
- Alvarez-Valdes et al. (2007): Branch and bound

**Full Bibliography:** See `RESEARCH_PROBLEM_STANDALONE.md`

---

## 16. Contact

**Email:** research@example.com
**Repository:** [To be announced]
**Forum:** [To be announced]

**Questions?** See full specification for complete details.

---

**Problem Status:** Open for Research
**Difficulty:** Hard (NP-Hard + Real-world Constraints)
**Impact:** High (Industrial Deployment)

**Happy Optimizing! 🔬📐**

---

**Last Updated:** 2025-11-08
**Version:** 1.0 (Standalone Brief)
