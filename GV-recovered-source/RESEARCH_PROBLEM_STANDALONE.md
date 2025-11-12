# 2D Guillotine Cutting Stock Problem with Orientation Constraints
## Research Problem Specification

**Problem Class:** NP-Hard Combinatorial Optimization
**Application Domain:** Industrial Cutting Stock, Manufacturing Optimization
**Version:** 1.0
**Date:** 2025-11-08

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Formal Mathematical Definition](#2-formal-mathematical-definition)
3. [Constraints](#3-constraints)
4. [Objective Functions](#4-objective-functions)
5. [Input Specification](#5-input-specification)
6. [Output Specification](#6-output-specification)
7. [Complexity Analysis](#7-complexity-analysis)
8. [Evaluation Metrics](#8-evaluation-metrics)
9. [Benchmark Instances](#9-benchmark-instances)
10. [Theoretical Questions](#10-theoretical-questions)
11. [References](#11-references)

---

## 1. Problem Statement

### 1.1 Problem Overview

Given a set of rectangular items with specified dimensions, quantities, and orientation constraints, and a set of stock rectangles (bins) with fixed dimensions, determine a cutting plan that minimizes the number of bins used while respecting all manufacturing constraints.

**Key Characteristics:**
- **Guillotine Constraint:** All cuts must be straight lines from edge to edge
- **Orientation Constraint:** Subset of items cannot be rotated
- **Kerf Loss:** Material removal of width $k$ at each cut
- **Material Matching:** Items can only be placed on bins with matching properties
- **Real-time Requirement:** Solution must be computed in seconds, not minutes

### 1.2 Motivation

This problem arises in industrial cutting operations where:
- Sheet materials (wood, metal, glass) must be cut into smaller rectangular pieces
- Cutting machines can only make straight guillotine cuts
- Some pieces have directional properties (wood grain, patterns, structural)
- Cutting blades remove material (kerf loss)
- Production requires fast planning (<5 seconds)

**Economic Impact:**
- Material costs: 40-60% of manufacturing expenses
- Waste reduction of 5-10% = significant cost savings
- Planning automation: 90% reduction in human time
- Typical problem size: 20-100 items per cutting plan

### 1.3 Problem Variant Classification

Using Wäscher et al. (2007) typology:

- **Dimension:** Two-dimensional
- **Assignment:** All items must be packed (output maximization not applicable)
- **Assortment:** Many different item types
- **Shape:** Rectangular items and bins
- **Additional Constraints:**
  - Guillotine cuts required
  - Orientation restrictions
  - Kerf loss
  - Material matching

**Closest Standard Problem:** 2D-CSP (Two-Dimensional Cutting Stock Problem) with guillotine constraint

**Novel Aspects:**
- Combination of guillotine + orientation + kerf rarely studied
- Real-time requirement (seconds vs. minutes)
- Multi-objective (bins vs. utilization vs. leftover quality)

---

## 2. Formal Mathematical Definition

### 2.1 Input Parameters

**Items (Pieces to Cut):**
- Set $I = \{1, 2, ..., n\}$ of item types
- For each item $i \in I$:
  - Width: $w_i \in \mathbb{R}^+$
  - Height: $h_i \in \mathbb{R}^+$
  - Thickness: $t_i \in \mathbb{R}^+$
  - Material type: $m_i \in M$ (discrete set)
  - Quantity: $q_i \in \mathbb{Z}^+$
  - Orientation flag: $o_i \in \{0, 1\}$ where:
    - $o_i = 0$: item can be rotated 90°
    - $o_i = 1$: item orientation is fixed

**Stock Bins (Sheets):**
- Set $B = \{1, 2, ..., b\}$ of bin types
- For each bin type $j \in B$:
  - Width: $W_j \in \mathbb{R}^+$
  - Height: $H_j \in \mathbb{R}^+$
  - Thickness: $T_j \in \mathbb{R}^+$
  - Material type: $M_j \in M$
  - Available quantity: $Q_j \in \mathbb{Z}^+ \cup \{\infty\}$

**System Parameters:**
- Kerf width: $k \in \mathbb{R}^+$ (blade thickness, typically 2-6 units)
- Utilization threshold: $\theta \in [0, 1]$ (minimum acceptable, typically 0.75-0.85)
- Time limit: $T_{max} \in \mathbb{R}^+$ (seconds, typically 5-30)

### 2.2 Decision Variables

- $x_{ij} \in \{0, 1\}$: Binary variable, 1 if item $i$ is assigned to bin instance $j$
- $r_i \in \{0, 1\}$: Binary variable, 1 if item $i$ is rotated 90°
- $p_i = (p_i^x, p_i^y) \in \mathbb{R}^2$: Position of item $i$ (bottom-left corner)
- $u_j \in \{0, 1\}$: Binary variable, 1 if bin instance $j$ is used

**Derived Values:**
- Placed width: $w_i' = \begin{cases} w_i & \text{if } r_i = 0 \\ h_i & \text{if } r_i = 1 \end{cases}$
- Placed height: $h_i' = \begin{cases} h_i & \text{if } r_i = 0 \\ w_i & \text{if } r_i = 1 \end{cases}$

### 2.3 Objective Function

**Primary Objective (Lexicographic Priority 1):**
$$\min Z_1 = \sum_{j=1}^{|B|} u_j$$

Minimize the total number of bins used.

**Secondary Objective (Lexicographic Priority 2):**
$$\max Z_2 = \frac{\sum_{i=1}^{n} q_i \cdot w_i \cdot h_i}{\sum_{j: u_j=1} W_j \cdot H_j}$$

Maximize the utilization rate (minimize waste).

**Multi-Objective Formulation:**
$$\min \left( Z_1, -Z_2 \right)$$

With lexicographic ordering: $Z_1$ has absolute priority over $Z_2$.

### 2.4 Constraints

**C1. Coverage Constraint (All Items Placed):**
$$\sum_{j} x_{ij} = q_i, \quad \forall i \in I$$

**C2. Material Matching:**
$$x_{ij} = 1 \implies t_i = T_j \land m_i = M_j$$

**C3. Boundary Constraints:**
$$x_{ij} = 1 \implies p_i^x + w_i' \leq W_j \land p_i^y + h_i' \leq H_j$$

**C4. Non-Overlap Constraint:**

For any two items $i, k$ placed on the same bin $j$:
$$x_{ij} = x_{kj} = 1, i \neq k \implies$$
$$\left( p_i^x + w_i' + k \leq p_k^x \right) \lor \left( p_k^x + w_k' + k \leq p_i^x \right) \lor$$
$$\left( p_i^y + h_i' + k \leq p_k^y \right) \lor \left( p_k^y + h_k' + k \leq p_i^y \right)$$

The kerf $k$ ensures minimum spacing.

**C5. Guillotine Cut Constraint:**

For each bin $j$ with $u_j = 1$, there exists a sequence of guillotine cuts $G_j = \{g_1, g_2, ..., g_l\}$ where:
- Each cut $g_i$ is either horizontal or vertical
- Each cut spans the entire width/height of its containing rectangle
- Recursive application isolates each item

Formally, the cutting tree $T_j$ for bin $j$ must satisfy:
- Root node = entire bin rectangle
- Each internal node has exactly 2 children (cut splits rectangle)
- Each leaf node contains exactly 1 item
- All cuts are orthogonal and edge-to-edge

**C6. Orientation Constraint:**
$$o_i = 1 \implies r_i = 0$$

Items with fixed orientation cannot be rotated.

**C7. Utilization Threshold:**
$$u_j = 1 \implies \frac{\sum_{i: x_{ij}=1} w_i \cdot h_i}{W_j \cdot H_j} \geq \theta \lor \left( \sum_{j'} u_{j'} = 1 \right)$$

Each used bin must meet utilization threshold, except if it's the only bin.

**C8. Bin Availability:**
$$\sum_{i: x_{ij}=1} 1 > 0 \implies \sum_{j': \text{type}(j')=\text{type}(j), u_{j'}=1} 1 \leq Q_{\text{type}(j)}$$

Cannot use more bins than available.

---

## 3. Constraints

### 3.1 Guillotine Cut Constraint (Detailed)

**Definition:** A guillotine cut is a straight line perpendicular to an edge that extends from one side of a rectangle to the opposite side, dividing it into exactly two smaller rectangles.

**Properties:**
1. All cuts are orthogonal (parallel to edges)
2. Each cut divides parent rectangle into 2 children
3. Cuts form a binary tree structure
4. No T-junctions or 4-way intersections allowed

**Valid Cutting Pattern Example:**
```
Level 0 (Root):
┌─────────────────────────┐
│      Entire Bin         │
└─────────────────────────┘

Level 1 (First Cut - Vertical):
┌───────────┬─────────────┐
│   Left    │   Right     │
│  Region   │  Region     │
└───────────┴─────────────┘

Level 2 (Two Horizontal Cuts):
┌─────┬─────┬───────┬─────┐
│ I1  │ I2  │  I3   │ I4  │
└─────┴─────┴───────┴─────┘

Cutting Tree:
        Root
       /    \
     R1      R2
    /  \    /  \
   I1  I2  I3  I4
```

**Invalid Pattern (Non-Guillotine):**
```
┌─────────────────┐
│   I1      I2    │
├─────┬─────┼─────┤  ← T-junction (invalid!)
│ I3  │ I4  │ I5  │
└─────┴─────┴─────┘
```

**Practical Significance:**
- Simplifies cutting operations
- Compatible with panel saws, CNC routers
- Reduces operator errors
- Industry standard in furniture/sheet manufacturing

### 3.2 Orientation Constraint (Detailed)

**Physical Motivation:**

Some items have directional properties:
- **Wood grain:** Visible pattern that looks wrong when rotated
- **Veneer patterns:** Decorative surfaces with oriented designs
- **Structural anisotropy:** Material strength differs by direction
- **Visual aesthetics:** Matching grain across components

**Constraint Formulation:**

Item $i$ has orientation flag $o_i$:
- $o_i = 0$: **Rotatable** - can be placed in either orientation
- $o_i = 1$: **Non-rotatable** - must maintain original orientation

**Impact on Solution Space:**

For $n$ items:
- Without orientation constraint: $2^n$ rotation possibilities
- With $k$ non-rotatable items: $2^{n-k}$ rotation possibilities
- Typical real-world: 30-60% items are non-rotatable
- Solution space reduction: ≈ 50-90%

**Example:**

```
Item: Cabinet Door (600 × 2000 mm)
Grain: Vertical
o_i = 1 (non-rotatable)

Correct Placement:        Incorrect (Forbidden):
┌───────┐                 ┌─────────────────┐
│   │   │                 │  ──────────────  │
│   │   │  Grain vertical │  ──────────────  │ Grain horizontal
│   │   │  ✓ ALLOWED      │  ──────────────  │ ✗ FORBIDDEN
│   │   │                 └─────────────────┘
└───────┘
```

### 3.3 Kerf Loss Constraint (Detailed)

**Physical Motivation:**

Cutting tools (saw blades, laser cutters, water jets) remove material of width $k$:
- Circular saw blades: 2-4 mm
- Panel saws: 3-6 mm
- Laser cutters: 0.1-0.5 mm
- Water jets: 0.5-1.5 mm

**Mathematical Impact:**

Each cut consumes $k$ units of material:
```
Original dimension: D
Item width: w
Kerf: k
Remaining: D - w - k

Example:
Bin width: 1220 mm
Item: 600 mm
Kerf: 3 mm
Remainder: 1220 - 600 - 3 = 617 mm
```

**Cumulative Effect:**

Multiple cuts accumulate kerf loss:
```
Horizontal arrangement of 4 items:
┌────┬─┬────┬─┬────┬─┬────┐
│ I1 │k│ I2 │k│ I3 │k│ I4 │
└────┴─┴────┴─┴────┴─┴────┘

Total kerf loss: 3 × k = 9-18 mm (for k=3-6 mm)
Percentage: 0.7-1.5% of 1220 mm bin width
```

**Constraint Enforcement:**

Minimum distance between any two items:
$$d(i, j) \geq k$$

In practice:
- Include kerf in all dimension calculations
- Account for kerf when computing remainders
- Validate final solution with kerf included

### 3.4 Material Matching Constraint

**Motivation:**

Items can only be cut from bins with matching properties:

**Thickness Matching:**
- Items and bins must have identical thickness
- Different thicknesses physically incompatible
- Example: 18mm items cannot be cut from 25mm sheets

**Material Type Matching:**
- Color/species must match
- Examples:
  - Oak items → Oak bins
  - Cherry items → Cherry bins
  - White items → White bins

**Impact on Problem Structure:**

Problem decomposes into independent subproblems:

```
Input: 50 items
  - 20 items: 18mm Oak
  - 15 items: 18mm Cherry
  - 10 items: 25mm Oak
  - 5 items: 12mm Oak

Decomposition: 4 independent problems
  Subproblem 1: 20 items on 18mm Oak bins
  Subproblem 2: 15 items on 18mm Cherry bins
  Subproblem 3: 10 items on 25mm Oak bins
  Subproblem 4: 5 items on 12mm Oak bins

Total bins = sum of bins across all subproblems
```

**Complexity Implication:**

Let $g$ = number of material groups

Total complexity: $O(g \cdot f(n/g))$ where $f$ is single-group complexity

Typically: $g = 2-5$ groups per job

---

## 4. Objective Functions

### 4.1 Primary Objective: Minimize Bin Count

**Formulation:**
$$Z_1 = \sum_{j=1}^{b} u_j$$

**Priority:** HIGHEST

**Rationale:**
- Direct material cost reduction
- Each bin represents fixed material cost
- Minimizing bins = minimizing raw material expenditure

**Example:**
```
Solution A: 4 bins, 85% average utilization
Solution B: 3 bins, 78% average utilization

Preferred: Solution B
Reason: Uses 25% fewer bins despite lower utilization
Cost savings: 1 bin × $50 = $50 per job
```

### 4.2 Secondary Objective: Maximize Utilization

**Formulation:**
$$Z_2 = \frac{\sum_{i=1}^{n} q_i \cdot w_i \cdot h_i}{\sum_{j: u_j=1} W_j \cdot H_j}$$

**Priority:** MEDIUM (only among solutions with same bin count)

**Interpretation:**
- $Z_2 = 1.0$: Perfect utilization (no waste)
- $Z_2 = 0.8$: 80% utilization, 20% waste
- $Z_2 = 0.75$: 75% utilization, 25% waste

**Targets:**
- Excellent: $Z_2 \geq 0.85$ (85% utilization)
- Good: $Z_2 \geq 0.80$ (80% utilization)
- Acceptable: $Z_2 \geq 0.75$ (75% utilization)
- Poor: $Z_2 < 0.75$ (>25% waste)

**Calculation Example:**
```
Items total area: 7,200,000 mm²
Bins used: 3 bins
Bin dimensions: 1220 × 2440 mm each
Bin area: 2,976,800 mm² each
Total bin area: 8,930,400 mm²

Utilization: 7,200,000 / 8,930,400 = 0.806 = 80.6%
Waste: 1,730,400 mm² = 19.4%
```

### 4.3 Tertiary Objective: Leftover Quality

**Definition:**

Leftover pieces (waste) can be characterized by:
- Size: larger is better (more reusable)
- Shape: rectangular is better than L-shaped
- Quantity: fewer pieces is better

**Quality Score:**
$$Q_{leftover} = \frac{1}{|L|} \sum_{l \in L} \left( \alpha \cdot \frac{\min(w_l, h_l)}{L_{min}} + \beta \cdot \frac{\min(w_l, h_l)}{\max(w_l, h_l)} \right)$$

Where:
- $L$ = set of leftover pieces
- $w_l, h_l$ = dimensions of leftover $l$
- $L_{min}$ = minimum reusable size (typically 200 mm)
- $\alpha, \beta$ = weights (typically 0.6, 0.4)

**Priority:** LOW (only when bins and utilization are equal)

**Rationale:**
- Larger, rectangular leftovers can be reused in future jobs
- Small, irregular pieces are effectively waste
- Optimizing leftover quality = building inventory for future

### 4.4 Quaternary Objective: Execution Time

**Target:** $T_{exec} < T_{max}$

Typical values:
- Small instances (n ≤ 20): $T_{max} = 2$ seconds
- Medium instances (n ≤ 50): $T_{max} = 5$ seconds
- Large instances (n ≤ 100): $T_{max} = 10$ seconds

**Priority:** CONSTRAINT (not optimization objective)

**Rationale:**
- Production environments require real-time planning
- Operators cannot wait minutes for results
- Must integrate into workflow (seconds, not minutes)

### 4.5 Lexicographic Multi-Objective Ordering

**Preference Relation:**

Solution $S_1$ is preferred over $S_2$ if and only if:

1. $bins(S_1) < bins(S_2)$, OR
2. $bins(S_1) = bins(S_2)$ AND $util(S_1) > util(S_2)$, OR
3. $bins(S_1) = bins(S_2)$ AND $util(S_1) = util(S_2)$ AND $Q_{left}(S_1) > Q_{left}(S_2)$, OR
4. All above equal AND $time(S_1) < time(S_2)$

**Example Comparison:**
```
Solution A: 3 bins, 82% util, Q=0.7, 2.3s
Solution B: 3 bins, 84% util, Q=0.6, 4.1s
Solution C: 4 bins, 88% util, Q=0.9, 1.2s

Ranking:
1. Solution B (same bins as A, higher util wins)
2. Solution A (same bins as B, lower util loses)
3. Solution C (more bins, worst despite highest util)
```

---

## 5. Input Specification

### 5.1 Input Format (JSON)

```json
{
  "items": [
    {
      "id": "string",
      "width": float,
      "height": float,
      "thickness": float,
      "material": "string",
      "quantity": integer,
      "rotatable": boolean
    }
  ],
  "bins": [
    {
      "id": "string",
      "width": float,
      "height": float,
      "thickness": float,
      "material": "string",
      "available": integer
    }
  ],
  "parameters": {
    "kerf": float,
    "utilizationThreshold": float,
    "timeLimit": float
  }
}
```

### 5.2 Input Constraints

**Dimension Bounds:**
- Item dimensions: $1 \leq w_i, h_i \leq 10000$ (mm or arbitrary units)
- Bin dimensions: $100 \leq W_j, H_j \leq 10000$
- Thickness: $0.1 \leq t_i, T_j \leq 100$
- Kerf: $0 \leq k \leq 10$

**Quantity Bounds:**
- Item quantity: $1 \leq q_i \leq 1000$
- Bin availability: $1 \leq Q_j \leq 1000$ or $Q_j = \infty$

**Problem Size:**
- Number of item types: $1 \leq n \leq 100$ (practical limit)
- Number of bin types: $1 \leq b \leq 10$ (typically 1-3)
- Total items (with quantities): $\sum q_i \leq 500$

### 5.3 Example Instance

```json
{
  "items": [
    {
      "id": "I001",
      "width": 2000,
      "height": 600,
      "thickness": 18,
      "material": "Oak",
      "quantity": 2,
      "rotatable": false
    },
    {
      "id": "I002",
      "width": 900,
      "height": 600,
      "thickness": 18,
      "material": "Oak",
      "quantity": 2,
      "rotatable": true
    },
    {
      "id": "I003",
      "width": 880,
      "height": 580,
      "thickness": 18,
      "material": "Oak",
      "quantity": 3,
      "rotatable": true
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
    "utilizationThreshold": 0.78,
    "timeLimit": 5.0
  }
}
```

**Instance Properties:**
- 7 total items (2+2+3)
- 1 bin type (unlimited availability)
- All items same material/thickness
- 2 non-rotatable items, 5 rotatable

**Expected Solution:**
- Optimal bins: 2
- Expected utilization: 80-85%
- Solvable in: <1 second

---

## 6. Output Specification

### 6.1 Solution Format (JSON)

```json
{
  "metadata": {
    "objectiveValue": integer,
    "utilization": float,
    "executionTime": float,
    "algorithmName": "string"
  },
  "bins": [
    {
      "binId": integer,
      "binType": "string",
      "width": float,
      "height": float,
      "utilization": float,
      "items": [
        {
          "itemId": "string",
          "x": float,
          "y": float,
          "width": float,
          "height": float,
          "rotated": boolean
        }
      ],
      "cuts": [
        {
          "type": "horizontal" | "vertical",
          "position": float,
          "start": {"x": float, "y": float},
          "end": {"x": float, "y": float}
        }
      ]
    }
  ],
  "unplaced": [
    {
      "itemId": "string",
      "quantity": integer
    }
  ]
}
```

### 6.2 Solution Validity

A solution is **valid** if and only if:

1. ✓ All items placed: `unplaced` array is empty
2. ✓ No overlaps: $\forall i \neq j$ on same bin, rectangles don't overlap + kerf
3. ✓ Within boundaries: All items within bin dimensions
4. ✓ Material matching: All items on correct bin type
5. ✓ Orientation respected: Non-rotatable items not rotated
6. ✓ Guillotine feasible: Valid cutting sequence exists
7. ✓ Utilization threshold: All bins (except possibly one) meet threshold

### 6.3 Solution Quality

A solution is **high-quality** if:

- ✓ Bins used ≤ theoretical lower bound + 20%
- ✓ Average utilization ≥ 80%
- ✓ No bin with utilization < 70% (except last)
- ✓ Execution time < time limit
- ✓ Deterministic (same input → same output)

---

## 7. Complexity Analysis

### 7.1 Complexity Classification

**Theorem:** The 2D Guillotine Cutting Stock Problem with Orientation Constraints is **NP-Hard**.

**Proof Sketch:**

Reduction from 2D Bin Packing (known NP-Hard):
1. 2D Bin Packing: Given rectangles and bins, minimize bins used
2. Our problem: Same + guillotine + orientation + kerf
3. Our problem ⊇ 2D Bin Packing (special case when no constraints)
4. Therefore: Our problem is NP-Hard (at least as hard)

**Decision Problem Version:**

Given items $I$, bins $B$, and integer $K$:
- **Question:** Does there exist a valid cutting plan using ≤ $K$ bins?
- **Complexity:** NP-Complete
- **Verification:** Polynomial time (O(n) to check all constraints)

### 7.2 Solution Space Size

**Lower Bound on Search Space:**

$$|\Omega| \geq \binom{n}{k_1, k_2, ..., k_b} \cdot 2^{r} \cdot (W \cdot H)^n$$

Where:
- $n$ = number of items
- $b$ = number of bins used
- $k_i$ = items on bin $i$
- $r$ = number of rotatable items
- $W \times H$ = bin dimensions (discretized)

**Example Calculation:**

For $n = 20$ items, $b = 3$ bins, $r = 12$ rotatable:
- Bin assignments: $\approx 3^{20} \approx 10^9$
- Rotations: $2^{12} = 4096$
- Positions: $(1220 \cdot 2440)^{20} \approx 10^{130}$ (discretized to 1mm)

**Total:** $\approx 10^{140+}$ possibilities

**Conclusion:** Exhaustive search infeasible for $n > 10$

### 7.3 Theoretical Bounds

**Lower Bound (Area-Based):**

$$LB_{area} = \left\lceil \frac{\sum_{i=1}^{n} q_i \cdot w_i \cdot h_i}{W \cdot H} \right\rceil$$

**Lower Bound (Dimension-Based):**

$$LB_{width} = \left\lceil \frac{\sum_{i: w_i > W/2} q_i}{1} \right\rceil$$

$$LB_{height} = \left\lceil \frac{\sum_{i: h_i > H/2} q_i}{1} \right\rceil$$

**Combined Lower Bound:**

$$LB = \max(LB_{area}, LB_{width}, LB_{height})$$

**Upper Bound (Trivial):**

$$UB = \sum_{i=1}^{n} q_i$$

(One bin per item - trivially valid but wasteful)

**Approximation Ratio:**

For any heuristic algorithm with solution $ALG$:
$$\rho = \frac{ALG}{OPT}$$

Known results:
- First Fit Decreasing: $\rho \leq 2$ (without guillotine)
- Best known with guillotine: $\rho \leq 2.7$ (Christofides & Whitlock, 1977)
- **Open question:** Can we achieve $\rho < 1.5$ with polynomial time?

---

## 8. Evaluation Metrics

### 8.1 Primary Metrics

**M1: Number of Bins Used**
$$M_1 = \sum_{j=1}^{b} u_j$$

Lower is better. Primary optimization target.

**M2: Utilization Rate**
$$M_2 = \frac{\sum_{i=1}^{n} q_i \cdot w_i \cdot h_i}{\sum_{j: u_j=1} W_j \cdot H_j} \times 100\%$$

Target: ≥ 80%. Benchmark: 75-85%.

**M3: Execution Time (seconds)**
$$M_3 = T_{execution}$$

Target: < 5s for n ≤ 50.

### 8.2 Secondary Metrics

**M4: Waste Percentage**
$$M_4 = (1 - M_2) \times 100\%$$

Target: ≤ 20%.

**M5: Gap to Lower Bound**
$$M_5 = \frac{M_1 - LB}{LB} \times 100\%$$

Lower is better. Measures optimality gap.

**M6: Utilization Standard Deviation**
$$M_6 = \sqrt{\frac{1}{|B|} \sum_{j=1}^{|B|} (u_j - M_2)^2}$$

Lower is better (more consistent utilization).

### 8.3 Constraint Compliance

**M7: Guillotine Validity**
$$M_7 = \frac{\text{bins with valid guillotine sequence}}{\text{total bins}} \times 100\%$$

Must be: 100%.

**M8: Orientation Compliance**
$$M_8 = \frac{\text{non-rotatable items placed correctly}}{\text{total non-rotatable items}} \times 100\%$$

Must be: 100%.

### 8.4 Composite Score

**Benchmark Scoring Function:**
$$S = 0.40 \cdot S_1 + 0.30 \cdot S_2 + 0.15 \cdot S_3 + 0.15 \cdot S_4$$

Where:
- $S_1 = \frac{LB}{M_1}$ (bins score, normalized by lower bound)
- $S_2 = \frac{M_2}{U_{target}}$ (utilization score, target = 0.80)
- $S_3 = \min(1, \frac{T_{target}}{M_3})$ (time score, target = 5s)
- $S_4 = Q_{leftover}$ (leftover quality score, 0-1)

**Interpretation:**
- $S \geq 0.95$: Excellent
- $S \geq 0.90$: Very Good
- $S \geq 0.85$: Good
- $S \geq 0.80$: Acceptable
- $S < 0.80$: Needs Improvement

---

## 9. Benchmark Instances

### 9.1 Instance Categories

**Small Instances (n ≤ 20):**
- Purpose: Correctness validation
- Time limit: 2 seconds
- Expected: Optimal or near-optimal

**Medium Instances (20 < n ≤ 50):**
- Purpose: Realistic production scenarios
- Time limit: 5 seconds
- Expected: High-quality heuristic solutions

**Large Instances (50 < n ≤ 100):**
- Purpose: Scalability testing
- Time limit: 10 seconds
- Expected: Good solutions within time limit

**Special Instances:**
- All items non-rotatable
- Mixed material types
- Extreme aspect ratios
- Dense packing challenges

### 9.2 Instance Generator

**Parameters:**
- $n$: Number of item types
- $density$: Difficulty level (easy, medium, hard)
- $rotation\_prob$: Probability item is rotatable

**Generation Algorithm:**

```python
def generate_instance(n, density="medium"):
    items = []

    # Size ranges based on density
    if density == "easy":
        size_range = (400, 1000)
        aspect_range = (0.5, 2.0)
        rotation_prob = 0.7
    elif density == "medium":
        size_range = (200, 2000)
        aspect_range = (0.3, 4.0)
        rotation_prob = 0.5
    else:  # hard
        size_range = (100, 2400)
        aspect_range = (0.1, 10.0)
        rotation_prob = 0.3

    for i in range(n):
        area = random.uniform(size_range[0]**2, size_range[1]**2)
        aspect = random.uniform(aspect_range[0], aspect_range[1])

        width = sqrt(area * aspect)
        height = area / width

        item = {
            "id": f"I{i+1:03d}",
            "width": round(width),
            "height": round(height),
            "thickness": random.choice([12, 18, 25]),
            "material": random.choice(["Oak", "Cherry", "Walnut"]),
            "quantity": random.randint(1, 5),
            "rotatable": random.random() < rotation_prob
        }
        items.append(item)

    return {
        "items": items,
        "bins": [{
            "id": "STD001",
            "width": 1220,
            "height": 2440,
            "thickness": 18,
            "material": "Oak",
            "available": -1
        }],
        "parameters": {
            "kerf": 3.0,
            "utilizationThreshold": 0.78,
            "timeLimit": 5.0
        }
    }
```

### 9.3 Known Optimal Solutions

**SMALL-01:**
- Items: 8
- Optimal bins: 2
- Optimal utilization: 82.7%
- Proof: Lower bound = 2, solution exists with 2 bins

**SMALL-02:**
- Items: 12
- Optimal bins: 3
- Optimal utilization: 85.1%
- Proof: Verified by exhaustive search

**(Additional instances with known optima to be published)**

### 9.4 Benchmark Suite

**Suite Name:** GCSP-BENCH-2025
**Total Instances:** 50
**Categories:**
- 10 small (n ≤ 20)
- 20 medium (20 < n ≤ 50)
- 15 large (50 < n ≤ 100)
- 5 special cases

**Download:** [URL to be announced]

**Format:** Each instance includes:
- `input.json` - Problem definition
- `metadata.json` - Instance properties
- `lower_bound.txt` - Theoretical lower bound
- `best_known.json` - Best known solution (if available)

---

## 10. Theoretical Questions

### 10.1 Open Research Questions

**Q1: Approximation Ratio**
- What is the best achievable approximation ratio in polynomial time?
- Can we prove $\rho < 1.5$ for some polynomial algorithm?
- Does adding guillotine constraint worsen approximation ratio?

**Q2: Fixed-Parameter Tractability**
- Is the problem FPT when parameterized by bin width?
- Is the problem FPT when parameterized by number of item types?

**Q3: Hardness of Approximation**
- Can we prove APX-hardness?
- What is the inapproximability threshold?

**Q4: Special Cases**
- Are there polynomial-time cases beyond trivial ones?
- Is problem solvable in polynomial time when:
  - All items have same aspect ratio?
  - Bins are square?
  - All items rotatable?

**Q5: Guillotine Impact**
- How much worse is guillotine vs. non-guillotine?
- Can we quantify the "price of guillotine"?

### 10.2 Algorithmic Challenges

**C1: Exact Methods**
- Can branch-and-bound solve instances with n = 50 in reasonable time?
- Can constraint programming outperform ILP?
- Can we use symmetry breaking to reduce search space?

**C2: Heuristic Quality**
- Can we design heuristic with provable approximation ratio < 2?
- Can we achieve 85%+ utilization deterministically?
- What is the role of lookahead depth?

**C3: Lower Bounds**
- Can we improve area-based lower bound?
- Can we incorporate guillotine constraint into lower bound?
- Can dual feasibility provide better bounds?

**C4: Real-Time Performance**
- What is the trade-off between quality and speed?
- Can we achieve 80% utilization in O(n log n) time?
- Can we use approximation algorithms with quality guarantees?

### 10.3 Practical Extensions

**E1: Online Version**
- Items arrive over time, must pack immediately
- No backtracking allowed
- Competitive ratio?

**E2: Stochastic Version**
- Item dimensions have uncertainty (±tolerance)
- Robust optimization approach?

**E3: Multi-Period**
- Leftover from job $t$ available for job $t+1$
- Optimize across multiple jobs?

**E4: Multi-Objective**
- Pareto frontier for bins vs. utilization
- How to efficiently enumerate Pareto solutions?

---

## 11. References

### 11.1 Foundational Papers

1. **Gilmore, P.C.; Gomory, R.E. (1961)**
   "A Linear Programming Approach to the Cutting Stock Problem"
   *Operations Research*, 9(6), 849-859
   DOI: 10.1287/opre.9.6.849

2. **Lodi, A.; Martello, S.; Monaci, M. (2002)**
   "Two-dimensional packing problems: A survey"
   *European Journal of Operational Research*, 141(2), 241-252
   DOI: 10.1016/S0377-2217(02)00123-6

3. **Wäscher, G.; Haußner, H.; Schumann, H. (2007)**
   "An improved typology of cutting and packing problems"
   *European Journal of Operational Research*, 183(3), 1109-1130
   DOI: 10.1016/j.ejor.2005.12.047

### 11.2 Guillotine Constraint

4. **Beasley, J.E. (1985)**
   "Algorithms for unconstrained two-dimensional guillotine cutting"
   *Journal of the Operational Research Society*, 36(4), 297-306

5. **Christofides, N.; Whitlock, C. (1977)**
   "An algorithm for two-dimensional cutting problems"
   *Operations Research*, 25(1), 30-44
   DOI: 10.1287/opre.25.1.30

6. **Herz, J.C. (1972)**
   "A recursive computational procedure for two-dimensional stock cutting"
   *IBM Journal of Research and Development*, 16(5), 462-469

### 11.3 Heuristic Methods

7. **Burke, E.K.; Kendall, G.; Whitwell, G. (2004)**
   "A New Placement Heuristic for the Orthogonal Stock-Cutting Problem"
   *Operations Research*, 52(4), 655-671
   DOI: 10.1287/opre.1040.0115

8. **Alvarez-Valdes, R.; Parreño, F.; Tamarit, J.M. (2007)**
   "A branch and bound algorithm for the strip packing problem"
   *OR Spectrum*, 31(2), 431-459

9. **Wei, L.; Hu, Q.; Lim, A.; Liu, Q. (2018)**
   "A best-fit branch-and-bound heuristic for the unconstrained two-dimensional non-guillotine cutting problem"
   *European Journal of Operational Research*, 270(2), 448-474

### 11.4 Exact Methods

10. **Furini, F.; Malaguti, E.; Thomopulos, D. (2016)**
    "Modeling two-dimensional guillotine cutting problems via integer programming"
    *INFORMS Journal on Computing*, 28(4), 736-751
    DOI: 10.1287/ijoc.2016.0710

11. **Côté, J.F.; Iori, M. (2018)**
    "The Meet-in-the-Middle Principle for Cutting and Packing Problems"
    *INFORMS Journal on Computing*, 30(4), 646-661

### 11.5 Industrial Applications

12. **Cui, Y.; Yang, Y. (2010)**
    "A heuristic for the one-dimensional cutting stock problem with usable leftover"
    *European Journal of Operational Research*, 204(2), 245-250

13. **Belov, G.; Scheithauer, G. (2006)**
    "A branch-and-cut-and-price algorithm for one-dimensional stock cutting and two-dimensional two-stage cutting"
    *European Journal of Operational Research*, 171(1), 85-106

---

## Appendix A: Mathematical Notation

| Symbol | Meaning |
|--------|---------|
| $I$ | Set of items |
| $B$ | Set of bins |
| $n$ | Number of item types |
| $b$ | Number of bin types |
| $w_i, h_i$ | Width, height of item $i$ |
| $W_j, H_j$ | Width, height of bin $j$ |
| $t_i, T_j$ | Thickness of item $i$, bin $j$ |
| $m_i, M_j$ | Material type of item $i$, bin $j$ |
| $q_i$ | Quantity of item $i$ |
| $o_i$ | Orientation flag (0=rotatable, 1=fixed) |
| $k$ | Kerf width |
| $\theta$ | Utilization threshold |
| $x_{ij}$ | Item $i$ assigned to bin $j$ |
| $r_i$ | Item $i$ rotated |
| $p_i$ | Position of item $i$ |
| $u_j$ | Bin $j$ is used |
| $LB$ | Lower bound on optimal solution |

---

## Appendix B: Guillotine Cut Formalization

**Cutting Tree Definition:**

A cutting plan is represented as a binary tree $T = (V, E)$ where:
- Each node $v \in V$ represents a rectangle
- Root = entire bin
- Each internal node has exactly 2 children (from guillotine cut)
- Each leaf = one item

**Cut Encoding:**

Each internal node has:
- Direction $d_v \in \{H, V\}$ (horizontal or vertical)
- Position $p_v \in [0, width_v]$ or $[0, height_v]$

**Valid Cutting Sequence:**

Function $\text{Valid}(T)$ returns true if:
1. Root dimensions = bin dimensions
2. For each internal node $v$:
   - Children dimensions sum to parent (accounting for kerf)
   - Cut is edge-to-edge (spans full width/height)
3. Each leaf contains exactly one item
4. Item dimensions match leaf dimensions

---

## Contact Information

**Problem Coordinator:** [To Be Assigned]
**Email:** research@example.com
**Benchmark Repository:** [URL to be announced]
**Discussion Forum:** [URL to be announced]

**Submission Guidelines:**
1. Solve benchmark instances
2. Validate solutions (validator provided)
3. Document algorithm
4. Submit results + code (optional)
5. Leaderboard publication

---

**Document Status:** Complete Research Specification
**Last Updated:** 2025-11-08
**Version:** 1.0 (Standalone)
**License:** Creative Commons BY 4.0

---

**END OF RESEARCH PROBLEM SPECIFICATION**
