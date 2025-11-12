# 2D Guillotine Bin Packing Problem for Furniture Manufacturing
## Research Problem Specification

**Version:** 1.0
**Date:** 2025-11-08
**Classification:** NP-Hard Combinatorial Optimization
**Application Domain:** Industrial Cutting Stock, Furniture Manufacturing
**Status:** Open Research Problem - Seeking Optimal/Near-Optimal Solutions

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Formal Problem Definition](#2-formal-problem-definition)
3. [Constraints and Rules](#3-constraints-and-rules)
4. [Objective Functions](#4-objective-functions)
5. [Input Specification](#5-input-specification)
6. [Output Specification](#6-output-specification)
7. [Complexity Analysis](#7-complexity-analysis)
8. [Evaluation Metrics](#8-evaluation-metrics)
9. [Test Datasets](#9-test-datasets)
10. [Current State-of-the-Art](#10-current-state-of-the-art)
11. [Research Challenges](#11-research-challenges)
12. [Benchmark Problems](#12-benchmark-problems)
13. [References](#13-references)

---

## 1. Problem Statement

### 1.1 Overview

Given a set of **rectangular products** (furniture components) with specified dimensions, quantities, and material properties, and a set of **stock sheets** (raw material boards) with fixed dimensions, determine an optimal cutting plan that:

1. **Minimizes the number of stock sheets used** (primary objective)
2. **Maximizes material utilization rate** (secondary objective)
3. **Respects all manufacturing constraints** (guillotine cuts, grain direction, saw kerf)
4. **Generates reusable leftover pieces** (tertiary objective)

### 1.2 Real-World Context

This problem arises in **furniture manufacturing** where wooden panels, plywood, MDF, or other sheet materials must be cut into components for:
- Custom wardrobes (closets)
- Kitchen cabinets
- Office furniture
- Bookshelves
- Interior design elements

**Economic Impact:**
- Material costs represent 40-60% of manufacturing expenses
- Typical waste with manual planning: 25-30%
- Target waste with optimization: 15-20%
- Processing time: Must be <5 seconds for 50 products (real-time requirement)

### 1.3 Problem Variants

This is a specific variant of the **2D Cutting Stock Problem (2D-CSP)** with:
- **Guillotine cuts** (orthogonal guillotine constraint)
- **Orientation constraints** (grain direction)
- **Blade width loss** (saw kerf)
- **Heterogeneous materials** (multiple colors/thicknesses)
- **Leftover reuse** (inventory management)
- **Pattern consolidation** (batch manufacturing)

---

## 2. Formal Problem Definition

### 2.1 Mathematical Formulation

**Given:**

- **Products**: Set $P = \{p_1, p_2, ..., p_n\}$ where each product $p_i$ has:
  - Width: $w_i \in \mathbb{R}^+$
  - Height: $h_i \in \mathbb{R}^+$
  - Thickness: $t_i \in \mathbb{R}^+$
  - Color/Material: $c_i \in C$ (discrete set)
  - Quantity: $q_i \in \mathbb{Z}^+$
  - Grain direction constraint: $d_i \in \{0, 1\}$ (0=rotatable, 1=fixed)

- **Stock Sheets**: Set $S = \{s_1, s_2, ..., s_m\}$ where each sheet $s_j$ has:
  - Width: $W_j \in \mathbb{R}^+$
  - Height: $H_j \in \mathbb{R}^+$
  - Thickness: $T_j \in \mathbb{R}^+$
  - Color/Material: $C_j \in C$
  - Available quantity: $Q_j \in \mathbb{Z}^+$ (potentially unlimited)

- **Parameters**:
  - Saw kerf (blade width): $k \in \mathbb{R}^+$ (typically 2-6mm)
  - Minimum utilization threshold: $\theta \in [0, 1]$ (typically 0.75-0.85)
  - Minimum leftover size: $L_{min} \in \mathbb{R}^+$ (typically 200mm)

**Decision Variables:**

- $x_{ij} \in \{0, 1\}$: Whether product $i$ is placed on sheet $j$
- $r_i \in \{0, 1\}$: Rotation of product $i$ (0=original, 1=90° rotated)
- $(x_i, y_i) \in \mathbb{R}^2$: Position of product $i$ bottom-left corner
- $z_j \in \{0, 1\}$: Whether sheet $j$ is used

**Objective Functions:**

Primary (Minimize):
$$\text{minimize} \sum_{j=1}^{m} z_j$$

Secondary (Maximize):
$$\text{maximize} \frac{\sum_{i=1}^{n} \sum_{j=1}^{m} x_{ij} \cdot w_i \cdot h_i}{\sum_{j=1}^{m} z_j \cdot W_j \cdot H_j}$$

### 2.2 Constraint Set

**C1. Product Placement (Coverage):**
$$\sum_{j=1}^{m} x_{ij} = q_i, \quad \forall i \in \{1, ..., n\}$$
All products must be placed exactly $q_i$ times.

**C2. Material Matching:**
$$x_{ij} = 1 \implies (t_i = T_j) \land (c_i = C_j)$$
Products can only be placed on sheets with matching thickness and color.

**C3. Boundary Constraints:**
$$x_{ij} = 1 \implies x_i + w_i' \leq W_j \land y_i + h_i' \leq H_j$$
where $w_i' = w_i$ if $r_i = 0$ else $h_i$, and $h_i' = h_i$ if $r_i = 0$ else $w_i$

**C4. Non-Overlap Constraint:**
$$x_{ij} = x_{kj} = 1, i \neq k \implies \text{no overlap between } p_i \text{ and } p_k$$

Formally (using disjunctive constraints):
$$x_i + w_i' + k \leq x_k \lor x_k + w_k' + k \leq x_i \lor y_i + h_i' + k \leq y_k \lor y_k + h_k' + k \leq y_i$$

**C5. Guillotine Cut Constraint:**
Each product placement must allow a straight edge-to-edge cut (guillotine cut) from one side of the sheet to the other, dividing it into two rectangles.

Formally: For any sheet $j$, there exists a sequence of guillotine cuts $G = \{g_1, g_2, ..., g_l\}$ where:
- Each $g_i$ is either a horizontal or vertical line
- Each $g_i$ spans the entire width or height of its containing rectangle
- Recursive application of $G$ isolates each product

**C6. Rotation Constraint:**
$$d_i = 1 \implies r_i = 0$$
Products with grain direction constraint cannot be rotated.

**C7. Saw Kerf Constraint:**
Minimum distance between any two products on the same sheet must be at least $k$:
$$x_{ij} = x_{kj} = 1 \implies \text{distance}(p_i, p_k) \geq k$$

**C8. Utilization Threshold:**
$$z_j = 1 \implies \frac{\sum_{i: x_{ij}=1} w_i \cdot h_i}{W_j \cdot H_j} \geq \theta \lor j = 1$$
Each used sheet (except first) must meet minimum utilization threshold.

**C9. Leftover Quality (Soft Constraint):**
Leftover pieces should be rectangular (not L-shaped) and $\geq L_{min}$ in both dimensions when possible.

---

## 3. Constraints and Rules

### 3.1 Guillotine Cut Constraint (Detailed)

**Definition:** All cuts must be **guillotine cuts** - straight orthogonal lines from one edge to the opposite edge.

**Visual Example:**

```
VALID Guillotine Pattern:
┌─────────────────────────┐
│         P1              │
├─────────────┬───────────┤  ← Horizontal guillotine cut
│     P2      │    P3     │
├─────┬───────┼─────┬─────┤  ← Vertical guillotine cuts
│ P4  │  P5   │ P6  │ P7  │
└─────┴───────┴─────┴─────┘

INVALID (Non-Guillotine):
┌─────────────────────────┐
│         P1              │
├─────────────┬───────────┤
│     P2      │    P3     │
│             ├─────┬─────┤  ← Invalid: cut doesn't span full width
│             │ P4  │ P5  │
└─────────────┴─────┴─────┘
```

**Implementation:**
- Cutting patterns must form a **binary tree structure**
- Each node represents a rectangle
- Each cut divides a rectangle into exactly 2 sub-rectangles
- Cuts alternate between horizontal and vertical (optional, but common)

**Why This Matters:**
- Simpler cutting sequences for shop floor
- Compatible with panel saws, CNC routers
- Reduces cutting errors
- Easier for workers to follow

### 3.2 Grain Direction Constraint (Detailed)

**Definition:** Some products have **directional grain** (wood grain, veneer pattern) that must be oriented consistently.

**Rules:**
- **Directional products** ($d_i = 1$): CANNOT be rotated 90°
  - Visible surfaces (doors, drawer fronts, cabinet faces)
  - Wood grain must run in specific direction
  - Veneer patterns that look wrong when rotated

- **Non-directional products** ($d_i = 0$): CAN be rotated 90°
  - Internal components (shelves, dividers, structural pieces)
  - Hidden surfaces
  - No visible grain pattern

**Visual Example:**

```
Directional Product (Cabinet Door with Vertical Grain):
┌─────────┐
│    │    │  ← Grain runs vertically
│    │    │     MUST maintain this orientation
│    │    │     Rotating 90° would be visible defect
│    │    │
└─────────┘

✓ CORRECT:        ✗ WRONG:
┌─────────┐       ┌───────────────┐
│    │    │       │  ────────────  │  Grain horizontal (defect!)
│    │    │       └───────────────┘
│    │    │
└─────────┘
```

**Statistics:**
- Typical orders: 30-50% directional products
- Impact: Reduces placement options by ~40%
- Critical for quality: Incorrect orientation = rejected product

### 3.3 Saw Kerf Constraint (Detailed)

**Definition:** Cutting blade removes material of width $k$ (typically 2-6mm).

**Impact on Dimensions:**
```
Original Sheet: 1220mm × 2440mm

After placing 600mm × 400mm product:
- Product occupies: 600mm × 400mm (actual product)
- Space consumed: (600 + k) × (400 + k)  [includes kerf]
- Remainder width: 1220 - 600 - k = 1220 - 600 - 3 = 617mm
- Remainder height: 2440 - 400 - k = 2440 - 400 - 3 = 2037mm
```

**Kerf Loss Accumulation:**
```
Example: Placing 5 products horizontally
┌────┬─┬────┬─┬────┬─┬────┬─┬────┐
│ P1 │k│ P2 │k│ P3 │k│ P4 │k│ P5 │
└────┴─┴────┴─┴────┴─┴────┴─┴────┘

Total kerf loss: 4 × k = 4 × 3mm = 12mm
Total waste: 12mm + leftover area
```

**Critical Consideration:**
- Must account for kerf in ALL dimension calculations
- Forgetting kerf = products don't fit during actual cutting
- Can accumulate to 5-10% material loss on highly fragmented layouts

### 3.4 Material Grouping Constraint

**Definition:** Products can ONLY be placed on sheets with matching:
1. **Thickness** (must match exactly)
2. **Color/Material type** (must match exactly)

**Example:**

```
Product Set:
- P1: 600×400×18mm, White Oak (qty: 2)
- P2: 900×600×18mm, White Oak (qty: 2)
- P3: 500×300×18mm, Cherry (qty: 3)
- P4: 800×400×25mm, White Oak (qty: 1)

Grouping:
Group 1 (18mm, White Oak): P1, P2  → Use 18mm White Oak sheets
Group 2 (18mm, Cherry): P3         → Use 18mm Cherry sheets
Group 3 (25mm, White Oak): P4      → Use 25mm White Oak sheets

Result: 3 separate optimization problems (cannot mix)
```

**Why:**
- Different thicknesses physically incompatible
- Different colors create visible quality defects
- Each group may have different stock sheet dimensions

### 3.5 Leftover Material Reuse

**Definition:** After cutting, leftover pieces $\geq L_{min}$ (typically 200mm×200mm) should be:
1. **Identified and catalogued**
2. **Available for future jobs** (inventory)
3. **Prioritized over new sheets** when applicable

**Leftover Types:**

```
Type 1: Edge Leftover (Most Common)
┌──────────────┬─────────┐
│   Products   │ Leftover│  ← Usable rectangular piece
│   (Used)     │ (L1)    │     Dimensions: W×H
└──────────────┴─────────┘

Type 2: Corner Leftover
┌──────────────┬─────────┐
│   Products   │   L1    │  ← Multiple leftover pieces
├──────────────┼─────────┤
│   Products   │   L2    │
└──────────────┴─────────┘

Type 3: L-Shaped Leftover (Less Desirable)
┌──────────────────────┐
│      Products        │
├──────────────┬───────┤
│   Products   │  L1   │  ← L-shaped (harder to reuse)
│              ├───────┤
│              │  L2   │
└──────────────┴───────┘
```

**Leftover Handling:**
- **Minimum size:** Both dimensions $\geq L_{min}$ (default: 200mm)
- **Preference:** Rectangular > L-shaped > Corner pieces
- **Quality score:** Larger, more rectangular = higher score
- **Inventory:** Add to available stock for next optimization

**Priority Rules:**
1. Try placing on existing leftovers first
2. Use new sheets only if leftovers insufficient
3. Optimize leftover generation quality (prefer rectangular)

### 3.6 Pattern Consolidation

**Definition:** When multiple sheets have **identical cutting patterns**, consolidate for batch manufacturing.

**Example:**

```
Before Consolidation:
Sheet 1: [P1 at (0,0), P2 at (603,0), P3 at (0,403)]
Sheet 2: [P1 at (0,0), P2 at (603,0), P3 at (0,403)]  ← Identical!
Sheet 3: [P1 at (0,0), P2 at (603,0), P3 at (0,403)]  ← Identical!
Sheet 4: [P4 at (0,0), P5 at (805,0)]  ← Different

After Consolidation:
Pattern A: [P1, P2, P3] × 3 sheets  ← Batch quantity = 3
Pattern B: [P4, P5] × 1 sheet
```

**Benefits:**
- **Manufacturing efficiency:** Set up cutting machine once, cut 3 sheets
- **Reduced errors:** Workers follow same pattern repeatedly
- **Faster production:** No machine reconfiguration
- **Quality control:** Consistent results across batch

**Implementation:**
- Generate hash/signature for each cutting pattern
- Group sheets with identical signatures
- Display batch quantity in output
- Provide single diagram for batch

---

## 4. Objective Functions

### 4.1 Primary Objective: Minimize Sheets Used

**Formula:**
$$\min Z = \sum_{j=1}^{m} z_j$$

where $z_j = 1$ if sheet $j$ is used, 0 otherwise.

**Priority:** HIGHEST
**Rationale:** Direct material cost reduction

**Example:**
```
Solution A: 4 sheets, 85% avg utilization
Solution B: 3 sheets, 78% avg utilization

Preferred: Solution B (fewer sheets despite lower utilization)
```

### 4.2 Secondary Objective: Maximize Utilization

**Formula:**
$$\max U = \frac{\sum_{i=1}^{n} q_i \cdot w_i \cdot h_i}{\sum_{j=1}^{m} z_j \cdot W_j \cdot H_j}$$

**Priority:** MEDIUM
**Rationale:** Minimize waste within used sheets

**Target:** $U \geq 0.80$ (80% utilization)
**Acceptable:** $U \geq 0.75$ (75% utilization)
**Excellent:** $U \geq 0.85$ (85% utilization)

**Calculation Example:**
```
Products total area: 7,200,000 mm²
Sheets used: 3 sheets × 1220mm × 2440mm = 8,933,760 mm²
Utilization: 7,200,000 / 8,933,760 = 80.6%
```

### 4.3 Tertiary Objective: Leftover Quality

**Formula:**
$$\max L = \sum_{l \in Leftovers} Q(l)$$

where $Q(l)$ is quality score:
$$Q(l) = \alpha \cdot S(l) + \beta \cdot R(l) + \gamma \cdot N(l)$$

- $S(l)$: Size score = $\frac{\min(w_l, h_l)}{L_{min}}$ (larger = better)
- $R(l)$: Rectangularity = $\frac{\min(w_l, h_l)}{\max(w_l, h_l)}$ (closer to 1 = better)
- $N(l)$: Count penalty = $\frac{1}{1 + \text{num\_pieces}}$ (fewer pieces = better)

**Weights:** $\alpha = 0.5, \beta = 0.3, \gamma = 0.2$

**Priority:** LOW (only when primary/secondary objectives are equal)

### 4.4 Quaternary Objective: Minimize Execution Time

**Target:** $T < 5$ seconds for $n \leq 50$ products
**Acceptable:** $T < 10$ seconds for $n \leq 100$ products
**Maximum:** $T < 30$ seconds for any input

**Priority:** CONSTRAINT (not optimization objective)

### 4.5 Multi-Objective Optimization

**Lexicographic Ordering:**
1. Minimize sheets used (highest priority)
2. Among equal sheet counts: maximize utilization
3. Among equal utilization: maximize leftover quality
4. Among equal quality: minimize execution time

**Trade-off Example:**
```
Solution A: 3 sheets, 82% util, 5 good leftovers, 2s time
Solution B: 3 sheets, 84% util, 2 poor leftovers, 8s time

Preferred: Solution B (higher utilization, same sheet count)
```

---

## 5. Input Specification

### 5.1 Product List Format

**Data Structure:**
```json
{
  "products": [
    {
      "id": "string",           // Unique product code (e.g., "A001")
      "name": "string",          // Descriptive name (e.g., "Side Panel")
      "width": float,            // Width in mm (e.g., 600.0)
      "height": float,           // Height in mm (e.g., 2000.0)
      "thickness": float,        // Thickness in mm (e.g., 18.0)
      "color": "string",         // Material color/type (e.g., "White Oak")
      "quantity": integer,       // Number of pieces needed (e.g., 2)
      "directional": boolean     // Grain direction constraint
    }
  ]
}
```

**Constraints:**
- $1 \leq width, height \leq 10000$ mm
- $1 \leq thickness \leq 100$ mm
- $1 \leq quantity \leq 999$ pieces
- All dimensions positive real numbers
- Total products: $1 \leq n \leq 100$ (practical limit)

**Example:**
```json
{
  "products": [
    {
      "id": "A001",
      "name": "侧板 (Side Panel)",
      "width": 2000,
      "height": 600,
      "thickness": 18,
      "color": "白橡木 (White Oak)",
      "quantity": 2,
      "directional": true
    },
    {
      "id": "A002",
      "name": "顶板 (Top Panel)",
      "width": 900,
      "height": 600,
      "thickness": 18,
      "color": "白橡木 (White Oak)",
      "quantity": 2,
      "directional": false
    }
  ]
}
```

### 5.2 Stock Sheet Catalog

**Data Structure:**
```json
{
  "sheets": [
    {
      "name": "string",          // Sheet size name (e.g., "4×8 ft")
      "width": float,            // Width in mm (e.g., 1220.0)
      "height": float,           // Height in mm (e.g., 2440.0)
      "thickness": float,        // Thickness in mm (e.g., 18.0)
      "color": "string",         // Material color/type
      "available": integer,      // Quantity available (-1 = unlimited)
      "cost": float              // Cost per sheet (optional)
    }
  ]
}
```

**Standard Sheet Sizes (China market):**
```
4×8 ft:  1220 × 2440 mm  (most common)
5×8 ft:  1530 × 2440 mm
4×9 ft:  1220 × 2750 mm
5×9 ft:  1530 × 2750 mm
4×10 ft: 1220 × 3060 mm
5×10 ft: 1530 × 3060 mm
```

### 5.3 Optimization Parameters

**Data Structure:**
```json
{
  "parameters": {
    "sawKerf": float,              // Blade width in mm (default: 3.0)
    "utilizationThreshold": float, // Minimum utilization (default: 0.78)
    "minLeftoverSize": float,      // Minimum leftover dimension (default: 200.0)
    "maxSheets": integer,          // Maximum sheets to use (optional)
    "timeLimit": integer,          // Max execution time in seconds (default: 30)
    "prioritizeLeftovers": boolean // Use existing leftovers first (default: true)
  }
}
```

**Typical Values:**
- Saw kerf: 2-6mm (depending on blade type)
- Utilization threshold: 0.75-0.85 (75-85%)
- Min leftover size: 200-300mm
- Time limit: 5-30 seconds

### 5.4 Optional: Leftover Inventory

**Data Structure:**
```json
{
  "leftovers": [
    {
      "id": "string",
      "width": float,
      "height": float,
      "thickness": float,
      "color": "string",
      "source": "string",  // Where it came from (optional)
      "age": integer       // Days in inventory (optional)
    }
  ]
}
```

**Priority:** Leftovers should be attempted before new sheets

---

## 6. Output Specification

### 6.1 Cutting Plan Format

**Data Structure:**
```json
{
  "solution": {
    "metadata": {
      "totalSheets": integer,
      "averageUtilization": float,
      "totalProductArea": float,
      "totalSheetArea": float,
      "totalWaste": float,
      "executionTime": float,      // seconds
      "algorithm": "string"
    },
    "sheets": [
      {
        "sheetId": integer,
        "sheetName": "string",
        "width": float,
        "height": float,
        "thickness": float,
        "color": "string",
        "utilization": float,
        "batchCount": integer,      // Number of identical sheets
        "placements": [
          {
            "productId": "string",
            "x": float,              // Bottom-left corner X
            "y": float,              // Bottom-left corner Y
            "width": float,          // Placed width (after rotation)
            "height": float,         // Placed height (after rotation)
            "rotated": boolean
          }
        ],
        "leftovers": [
          {
            "x": float,
            "y": float,
            "width": float,
            "height": float,
            "type": "string"         // "edge", "corner", "l-shaped"
          }
        ],
        "cuts": [                    // Optional: cutting sequence
          {
            "type": "string",        // "horizontal" or "vertical"
            "position": float,
            "startX": float,
            "startY": float,
            "endX": float,
            "endY": float
          }
        ]
      }
    ],
    "unplaced": [                    // Products that couldn't be placed
      {
        "productId": "string",
        "quantity": integer
      }
    ]
  }
}
```

### 6.2 Visualization Requirements

**Cutting Diagram:**
```
┌─────────────────────────────────────────────┐
│ Sheet 1: 1220×2440mm (82.3% utilization)   │
│                                             │
│ ┌─────────────┐  ┌──────────┐             │
│ │ A001        │  │  A002    │             │
│ │ 2000×600    │  │  900×600 │             │
│ │ (0,0)       │  │  (603,0) │             │
│ └─────────────┘  └──────────┘             │
│                                             │
│ ┌─────────────────────────────┐            │
│ │ Leftover: 1220×1834          │            │
│ │ (reusable)                   │            │
│ └─────────────────────────────┘            │
└─────────────────────────────────────────────┘
```

**Required Elements:**
- Sheet boundary with dimensions
- Product rectangles with:
  - Product ID
  - Dimensions
  - Position coordinates
  - Rotation indicator (if rotated)
- Leftover areas marked
- Utilization percentage
- Grain direction arrows (if applicable)

### 6.3 Success Criteria

**Valid Solution:**
- ✓ All products placed (unplaced array empty)
- ✓ No overlaps between products
- ✓ All products within sheet boundaries
- ✓ All products on matching material sheets
- ✓ Grain direction constraints respected
- ✓ Saw kerf accounted for in all calculations
- ✓ Guillotine cuts possible for all placements

**High-Quality Solution:**
- Average utilization ≥ 80%
- Fewer than 5% sheets below threshold utilization
- Leftovers ≥ 50% rectangular (not L-shaped)
- Pattern consolidation ratio ≥ 30%
- Execution time < 5 seconds for n ≤ 50

---

## 7. Complexity Analysis

### 7.1 Problem Classification

**NP-Hard** - Proven via reduction from bin packing problem

**Complexity Class:** NP-Complete (decision version)

**Proof Sketch:**
1. 2D Bin Packing is known NP-Hard
2. This problem includes 2D Bin Packing as special case
3. Additional constraints (guillotine, grain, kerf) make it harder
4. No polynomial-time exact algorithm exists (unless P=NP)

### 7.2 Decision Problem Version

**Question:** Given products $P$, sheets $S$, and integer $k$, does there exist a valid cutting plan using at most $k$ sheets?

**Answer:** YES or NO

**Verification:** Polynomial time (O(n) to verify all constraints)

### 7.3 Size of Solution Space

**Lower Bound:**
$$|\Omega| \geq \left(\frac{n!}{k!}\right) \cdot 2^n \cdot (W \cdot H)^n$$

Where:
- $n$ = number of products
- $k$ = number of sheets
- $2^n$ = rotation possibilities
- $(W \cdot H)^n$ = position possibilities (discretized)

**Example:** For $n=20$ products, $k=3$ sheets:
$$|\Omega| \approx \frac{20!}{3!} \cdot 2^{20} \cdot (1220 \cdot 2440)^{20} \approx 10^{100+}$$

**Conclusion:** Exhaustive search infeasible for $n > 10$

### 7.4 Special Cases

**Polynomial-Time Solvable:**
1. $n = 1$ (single product): O(1)
2. All products identical: O(n log n)
3. One-dimensional (height = 1): O(n log n)
4. Unlimited sheets, no utilization constraint: O(n²)

**Still NP-Hard:**
- Two-dimensional
- Limited sheets
- Utilization threshold
- Guillotine constraint
- Grain direction

---

## 8. Evaluation Metrics

### 8.1 Primary Metrics

**M1. Number of Sheets Used**
$$M_1 = \sum_{j=1}^{m} z_j$$
Lower is better. Primary optimization target.

**M2. Material Utilization Rate**
$$M_2 = \frac{\sum_{i=1}^{n} q_i \cdot w_i \cdot h_i}{\sum_{j=1}^{m} z_j \cdot W_j \cdot H_j} \times 100\%$$
Target: ≥ 80%. Benchmark: 75-85%.

**M3. Execution Time**
$$M_3 = T_{\text{execution}}$$
Target: < 5s for n ≤ 50, < 10s for n ≤ 100.

### 8.2 Secondary Metrics

**M4. Waste Percentage**
$$M_4 = (1 - M_2) \times 100\%$$
Target: ≤ 20%.

**M5. Leftover Quality Score**
$$M_5 = \frac{1}{|L|} \sum_{l \in L} \left( \alpha \cdot \frac{\min(w_l, h_l)}{L_{min}} + \beta \cdot \frac{\min(w_l, h_l)}{\max(w_l, h_l)} \right)$$
Range: [0, 1]. Higher is better.

**M6. Pattern Consolidation Ratio**
$$M_6 = \frac{\text{unique patterns}}{\text{total sheets}}$$
Range: [0, 1]. Lower is better (more consolidation).

**M7. Average Sheet Utilization**
$$M_7 = \frac{1}{|S|} \sum_{j=1}^{|S|} \frac{\sum_{i: x_{ij}=1} w_i \cdot h_i}{W_j \cdot H_j}$$
Target: ≥ 80%.

**M8. Utilization Standard Deviation**
$$M_8 = \sqrt{\frac{1}{|S|} \sum_{j=1}^{|S|} (u_j - M_7)^2}$$
Lower is better (more consistent).

### 8.3 Constraint Satisfaction Metrics

**M9. Guillotine Compliance**
$$M_9 = \frac{\text{sheets with valid guillotine cuts}}{\text{total sheets}} \times 100\%$$
Must be: 100%.

**M10. Grain Direction Compliance**
$$M_{10} = \frac{\text{directional products placed correctly}}{\text{total directional products}} \times 100\%$$
Must be: 100%.

**M11. Material Matching Accuracy**
$$M_{11} = \frac{\text{products on correct material}}{\text{total products}} \times 100\%$$
Must be: 100%.

### 8.4 Benchmark Scoring Function

**Composite Score:**
$$S = 0.40 \cdot S_1 + 0.30 \cdot S_2 + 0.15 \cdot S_3 + 0.15 \cdot S_4$$

Where:
- $S_1 = \frac{k_{\text{optimal}}}{k_{\text{solution}}}$ (sheets score)
- $S_2 = \frac{U_{\text{solution}}}{U_{\text{target}}}$ (utilization score)
- $S_3 = \min(1, \frac{T_{\text{target}}}{T_{\text{solution}}})$ (time score)
- $S_4 = M_5$ (leftover quality score)

**Interpretation:**
- $S \geq 0.95$: Excellent
- $S \geq 0.90$: Very Good
- $S \geq 0.85$: Good
- $S \geq 0.80$: Acceptable
- $S < 0.80$: Needs Improvement

---

## 9. Test Datasets

### 9.1 Small Instance (Validation)

**Name:** SMALL-01
**Products:** 8
**Sheet Size:** 1220 × 2440 mm
**Optimal Sheets:** 2 (known)
**Optimal Utilization:** 82.7%

```json
{
  "products": [
    {"id": "A001", "width": 2000, "height": 600, "thickness": 18,
     "color": "White Oak", "quantity": 2, "directional": true},
    {"id": "A002", "width": 900, "height": 600, "thickness": 18,
     "color": "White Oak", "quantity": 2, "directional": false},
    {"id": "A003", "width": 2000, "height": 900, "thickness": 5,
     "color": "White Oak", "quantity": 1, "directional": false},
    {"id": "A004", "width": 880, "height": 580, "thickness": 18,
     "color": "White Oak", "quantity": 3, "directional": false}
  ],
  "sheet": {"width": 1220, "height": 2440, "thickness": 18}
}
```

### 9.2 Medium Instance (Realistic)

**Name:** MEDIUM-01
**Products:** 23
**Sheet Size:** 1530 × 2440 mm
**Target Sheets:** 3-4
**Target Utilization:** ≥ 80%

```json
{
  "products": [
    {"id": "B001", "width": 700, "height": 400, "thickness": 18,
     "color": "Cherry", "quantity": 4, "directional": true},
    {"id": "B002", "width": 800, "height": 600, "thickness": 18,
     "color": "Cherry", "quantity": 4, "directional": true},
    {"id": "B003", "width": 2400, "height": 600, "thickness": 25,
     "color": "Cherry", "quantity": 1, "directional": false},
    {"id": "B004", "width": 780, "height": 580, "thickness": 18,
     "color": "Cherry", "quantity": 6, "directional": false},
    {"id": "B005", "width": 500, "height": 120, "thickness": 12,
     "color": "Cherry", "quantity": 8, "directional": false}
  ],
  "sheet": {"width": 1530, "height": 2440}
}
```

### 9.3 Large Instance (Stress Test)

**Name:** LARGE-01
**Products:** 100
**Sheet Size:** 1220 × 2440 mm
**Target Sheets:** 13-15
**Target Utilization:** ≥ 78%
**Time Limit:** 10 seconds

(Full dataset provided in separate file: `test_data_large_01.json`)

### 9.4 Special Cases

**SPECIAL-01: All Directional**
- 20 products, all with grain direction constraint
- Tests rotation handling

**SPECIAL-02: Mixed Thicknesses**
- 30 products across 3 thicknesses (12mm, 18mm, 25mm)
- Tests material grouping

**SPECIAL-03: Leftover Priority**
- 15 new products + 8 leftover pieces from previous job
- Tests leftover reuse logic

**SPECIAL-04: Extreme Aspect Ratios**
- Products with aspect ratios from 0.1 to 10
- Tests handling of elongated pieces

---

## 10. Current State-of-the-Art

### 10.1 Existing Approaches

**1. Greedy Heuristics (Current Implementation)**
- Algorithm: Random placement with 6 attempts
- Utilization: 75-80%
- Time: 4-5s for 50 products
- Pros: Simple, fast
- Cons: Non-deterministic, suboptimal, high variance

**2. First-Fit Decreasing (FFD)**
- Sort products by area/perimeter
- Place each in first available position
- Utilization: 70-75%
- Time: O(n²)
- Pros: Deterministic, fast
- Cons: Poor utilization, no lookahead

**3. Best-Fit Decreasing (BFD)**
- Sort products by area
- Place each in best-fitting rectangle
- Utilization: 75-80%
- Time: O(n² log n)
- Pros: Better than FFD
- Cons: Still greedy, local optima

**4. Guillotine + Maximal Rectangles**
- Track all free rectangular spaces
- Score placements using multiple heuristics
- Utilization: 78-83%
- Time: O(n² log n)
- Pros: Better space utilization
- Cons: Still heuristic, not optimal

**5. Genetic Algorithms (GA)**
- Evolve populations of solutions
- Utilization: 80-85%
- Time: 30-60s
- Pros: Good utilization
- Cons: Slow, non-deterministic

**6. Simulated Annealing (SA)**
- Accept worse solutions to escape local optima
- Utilization: 82-86%
- Time: 20-40s
- Pros: Better than greedy
- Cons: Slow, parameter-sensitive

**7. Integer Linear Programming (ILP)**
- Exact formulation, solve with CPLEX/Gurobi
- Utilization: Optimal (if solvable)
- Time: Exponential (impractical for n > 20)
- Pros: Optimal
- Cons: Too slow for production

**8. Column Generation**
- Generate patterns dynamically
- Utilization: Near-optimal
- Time: 10-30s for medium instances
- Pros: Good quality
- Cons: Complex, implementation difficulty

### 10.2 Performance Comparison

| Algorithm | Utilization | Time (50 products) | Deterministic | Notes |
|-----------|-------------|-------------------|---------------|-------|
| Random Greedy (Current) | 75-80% | 4-5s | No | Baseline |
| FFD | 70-75% | 1-2s | Yes | Fast but poor |
| BFD | 75-80% | 2-3s | Yes | Standard |
| Maximal Rectangles | 78-83% | 2-4s | Yes | Improved |
| Genetic Algorithm | 80-85% | 30-60s | No | Slow |
| Simulated Annealing | 82-86% | 20-40s | No | Parameter-sensitive |
| ILP (exact) | Optimal | Hours | Yes | Impractical |
| Column Generation | 85-90% | 10-30s | Yes | Complex |

### 10.3 Gap to Optimal

**Theoretical Bounds:**
- **Lower bound:** $LB = \lceil \frac{\sum A_i}{A_{\text{sheet}}} \rceil$ (area-based)
- **Upper bound:** Depends on algorithm
- **Gap:** Current: 5-10%, Best heuristics: 2-5%

**Example:**
```
Products total area: 7,200,000 mm²
Sheet area: 2,976,800 mm²
Lower bound: ⌈7,200,000 / 2,976,800⌉ = 3 sheets

Current solution: 4 sheets (33% above LB)
Good heuristic: 3 sheets (0% above LB, possibly optimal)
```

---

## 11. Research Challenges

### 11.1 Open Research Questions

**Q1. Near-Optimal Polynomial-Time Algorithm**
- Can we achieve 85%+ utilization in O(n² log n) time?
- What is the best achievable approximation ratio?

**Q2. Handling Multiple Objectives**
- How to balance sheet count vs. utilization vs. leftover quality?
- Multi-objective Pareto frontier exploration?

**Q3. Online/Dynamic Version**
- Products arrive over time, decisions must be made incrementally
- Can we maintain good utilization without full knowledge?

**Q4. Stochastic Version**
- Product dimensions have uncertainty (±2mm tolerance)
- How to create robust cutting plans?

**Q5. 3-Stage Guillotine**
- First cut: divide sheet into strips
- Second cut: divide strips into pieces
- Third cut: final sizing
- How to optimize this hierarchy?

### 11.2 Algorithmic Challenges

**C1. Guillotine Constraint Enforcement**
- How to efficiently enumerate all valid guillotine patterns?
- Can we use dynamic programming on guillotine trees?

**C2. Grain Direction + Guillotine**
- Interaction between rotation constraints and cut constraints
- Reduces solution space by ~60%

**C3. Leftover Quality Optimization**
- How to optimize for future jobs (unknown products)?
- Multi-period optimization framework?

**C4. Real-Time Requirements**
- Must solve in <5 seconds for production use
- Trade-off between quality and speed?

**C5. Scalability**
- Current: n ≤ 100 products
- Goal: n ≤ 500 products with similar performance

### 11.3 Practical Challenges

**P1. Robustness to Input Errors**
- Users may enter incorrect dimensions
- Algorithm should detect and flag infeasible inputs

**P2. Explainability**
- Why did algorithm choose this layout?
- How to communicate decisions to operators?

**P3. Adaptability**
- Different factories have different constraints
- Parameterizable algorithm framework?

**P4. Integration with MES/ERP**
- Real-time data exchange
- Automatic order import/export

---

## 12. Benchmark Problems

### 12.1 Standard Test Suite

**Suite Name:** GV-BENCH-2025
**Instances:** 50 problems
**Categories:**
1. Small (n ≤ 20): 10 instances
2. Medium (20 < n ≤ 50): 20 instances
3. Large (50 < n ≤ 100): 15 instances
4. Special cases: 5 instances

**Download:** `gv_benchmark_suite.zip` (provided separately)

### 12.2 Benchmark Format

Each instance includes:
```
instance_name/
├── input.json          # Problem definition
├── optimal.json        # Best known solution (if known)
├── lower_bound.txt     # Theoretical lower bound
├── description.md      # Problem description
└── visualization.svg   # Visual diagram
```

### 12.3 Submission Format

Researchers should provide:
```
solution/
├── algorithm_description.md  # Algorithm details
├── results.json              # Results on all instances
├── source_code/              # Implementation (optional)
└── paper.pdf                 # Research paper (optional)
```

### 12.4 Leaderboard Metrics

**Primary:** Average utilization across all instances
**Secondary:** Average execution time
**Tertiary:** Number of instances with optimal solutions

**Current Baseline:**
- Average utilization: 77.3%
- Average time: 4.2s
- Optimal solutions: 5/50 instances

**Target (State-of-the-Art):**
- Average utilization: ≥ 82%
- Average time: < 5s
- Optimal solutions: ≥ 15/50 instances

---

## 13. References

### 13.1 Foundational Papers

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

### 13.2 Guillotine Constraint

4. **Beasley, J.E. (1985)**
   "Algorithms for unconstrained two-dimensional guillotine cutting"
   *Journal of the Operational Research Society*, 36(4), 297-306

5. **Christofides, N.; Whitlock, C. (1977)**
   "An algorithm for two-dimensional cutting problems"
   *Operations Research*, 25(1), 30-44

### 13.3 Heuristic Methods

6. **Burke, E.K.; Kendall, G.; Whitwell, G. (2004)**
   "A New Placement Heuristic for the Orthogonal Stock-Cutting Problem"
   *Operations Research*, 52(4), 655-671

7. **Jylänki, J. (2010)**
   "A Thousand Ways to Pack the Bin - A Practical Approach to Two-Dimensional Rectangle Bin Packing"
   *http://clb.demon.fi/files/RectangleBinPack.pdf*

### 13.4 Metaheuristics

8. **Hopper, E.; Turton, B.C.H. (2001)**
   "An empirical investigation of meta-heuristic and heuristic algorithms for a 2D packing problem"
   *European Journal of Operational Research*, 128(1), 34-57

9. **Alvarez-Valdes, R.; Parreño, F.; Tamarit, J.M. (2008)**
   "A branch and bound algorithm for the strip packing problem"
   *OR Spectrum*, 31(2), 431-459

### 13.5 Exact Methods

10. **Côté, J.F.; Iori, M. (2018)**
    "The Meet-in-the-Middle Principle for Cutting and Packing Problems"
    *INFORMS Journal on Computing*, 30(4), 646-661

### 13.6 Industry Applications

11. **Cui, Y.; Yang, Y. (2010)**
    "A heuristic for the one-dimensional cutting stock problem with usable leftover"
    *European Journal of Operational Research*, 204(2), 245-250

12. **Furini, F.; Malaguti, E.; Thomopulos, D. (2016)**
    "Modeling two-dimensional guillotine cutting problems via integer programming"
    *INFORMS Journal on Computing*, 28(4), 736-751

---

## Appendix A: Mathematical Notation Summary

| Symbol | Meaning | Example |
|--------|---------|---------|
| $P$ | Set of products | $P = \{p_1, ..., p_n\}$ |
| $p_i$ | Product $i$ | $p_3$ |
| $w_i, h_i$ | Width, height of product $i$ | $w_1 = 600, h_1 = 2000$ |
| $t_i$ | Thickness of product $i$ | $t_1 = 18$ |
| $c_i$ | Color of product $i$ | $c_1 = \text{"White Oak"}$ |
| $q_i$ | Quantity of product $i$ | $q_1 = 2$ |
| $d_i$ | Directional flag | $d_i \in \{0, 1\}$ |
| $S$ | Set of stock sheets | $S = \{s_1, ..., s_m\}$ |
| $W_j, H_j$ | Width, height of sheet $j$ | $W_1 = 1220, H_1 = 2440$ |
| $k$ | Saw kerf (blade width) | $k = 3$ mm |
| $\theta$ | Utilization threshold | $\theta = 0.78$ |
| $x_{ij}$ | Product $i$ placed on sheet $j$ | $x_{12} = 1$ |
| $r_i$ | Rotation of product $i$ | $r_i \in \{0, 1\}$ |
| $(x_i, y_i)$ | Position of product $i$ | $(0, 0)$ |
| $z_j$ | Sheet $j$ used | $z_j \in \{0, 1\}$ |
| $L$ | Set of leftover pieces | $L = \{l_1, ..., l_k\}$ |
| $L_{min}$ | Minimum leftover size | $L_{min} = 200$ mm |

---

## Appendix B: Problem Instance Generator

Researchers can use this pseudocode to generate test instances:

```python
def generate_instance(n_products, difficulty="medium"):
    products = []

    # Size ranges based on difficulty
    if difficulty == "easy":
        size_range = (400, 1000)
        aspect_range = (0.5, 2.0)
        directional_prob = 0.2
    elif difficulty == "medium":
        size_range = (200, 2000)
        aspect_range = (0.3, 4.0)
        directional_prob = 0.4
    else:  # hard
        size_range = (100, 2400)
        aspect_range = (0.1, 10.0)
        directional_prob = 0.6

    for i in range(n_products):
        area = random.uniform(size_range[0]**2, size_range[1]**2)
        aspect = random.uniform(aspect_range[0], aspect_range[1])

        width = math.sqrt(area * aspect)
        height = area / width

        product = {
            "id": f"P{i+1:03d}",
            "width": round(width),
            "height": round(height),
            "thickness": random.choice([12, 18, 25]),
            "color": random.choice(["Oak", "Cherry", "Walnut"]),
            "quantity": random.randint(1, 5),
            "directional": random.random() < directional_prob
        }
        products.append(product)

    return {
        "products": products,
        "sheet": {
            "width": 1220,
            "height": 2440,
            "thickness": 18
        },
        "parameters": {
            "sawKerf": 3,
            "utilizationThreshold": 0.78,
            "minLeftoverSize": 200
        }
    }
```

---

## Appendix C: Solution Validator

Researchers should validate solutions using:

```python
def validate_solution(instance, solution):
    errors = []

    # Check all products placed
    for product in instance["products"]:
        count = count_placements(solution, product["id"])
        if count != product["quantity"]:
            errors.append(f"Product {product['id']}: expected {product['quantity']}, found {count}")

    # Check no overlaps
    for sheet in solution["sheets"]:
        if has_overlaps(sheet["placements"]):
            errors.append(f"Sheet {sheet['sheetId']} has overlapping products")

    # Check boundaries
    for sheet in solution["sheets"]:
        for placement in sheet["placements"]:
            if not within_bounds(placement, sheet):
                errors.append(f"Product {placement['productId']} exceeds sheet boundary")

    # Check guillotine constraint
    for sheet in solution["sheets"]:
        if not is_guillotine_valid(sheet["placements"]):
            errors.append(f"Sheet {sheet['sheetId']} violates guillotine constraint")

    # Check grain direction
    for sheet in solution["sheets"]:
        for placement in sheet["placements"]:
            product = get_product(instance, placement["productId"])
            if product["directional"] and placement["rotated"]:
                errors.append(f"Product {placement['productId']} rotated despite directional constraint")

    return {"valid": len(errors) == 0, "errors": errors}
```

---

## Contact Information

**Research Coordinator:** [To Be Assigned]
**Email:** [research@example.com]
**Benchmark Website:** [https://example.com/gv-benchmark]
**Discussion Forum:** [https://forum.example.com/2d-cutting]

**How to Submit Results:**
1. Solve benchmark instances
2. Validate solutions using provided validator
3. Submit to benchmark website
4. Results will be published on leaderboard

**How to Request Clarifications:**
- Open issue on GitHub: [https://github.com/example/gv-benchmark]
- Email research coordinator
- Post on discussion forum

---

**Document Status:** Complete and Ready for Distribution
**Last Updated:** 2025-11-08
**Version:** 1.0

---

**END OF RESEARCH PROBLEM SPECIFICATION**
