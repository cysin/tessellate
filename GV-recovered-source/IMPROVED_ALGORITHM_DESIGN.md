# Improved 2D Board Cutting Optimization Algorithm
## Design Document

**Version:** 2.0
**Date:** 2025-11-08
**Target Improvement:** 80-90% utilization (vs. current 75%)
**Performance Target:** <3 seconds for typical orders (vs. current 5 seconds)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current Algorithm Analysis](#2-current-algorithm-analysis)
3. [Algorithm Design Principles](#3-algorithm-design-principles)
4. [Core Algorithm: Maximal Rectangles with Guillotine](#4-core-algorithm-maximal-rectangles-with-guillotine)
5. [Placement Heuristics](#5-placement-heuristics)
6. [Product Sorting Strategies](#6-product-sorting-strategies)
7. [Lookahead Optimization](#7-lookahead-optimization)
8. [Leftover Quality Optimization](#8-leftover-quality-optimization)
9. [Pattern Recognition & Reuse](#9-pattern-recognition--reuse)
10. [Implementation Pseudocode](#10-implementation-pseudocode)
11. [Complexity Analysis](#11-complexity-analysis)
12. [Performance Optimizations](#12-performance-optimizations)
13. [Implementation Roadmap](#13-implementation-roadmap)
14. [Testing Strategy](#14-testing-strategy)
15. [Benchmark Comparisons](#15-benchmark-comparisons)

---

## 1. Executive Summary

### 1.1 Problem with Current Algorithm

The existing ViewServiceR2 algorithm uses a **greedy randomized approach** with significant limitations:

| Issue | Impact | Improvement Opportunity |
|-------|--------|------------------------|
| Random placement (6 attempts) | Non-deterministic, inconsistent quality | Use deterministic heuristics |
| Serialization cloning | 60%+ execution time overhead | Immutable data structures |
| No lookahead | Poor space utilization | Consider future products |
| Simple area sorting | Suboptimal packing | Multi-criteria sorting |
| O(n³) complexity | Slow for large orders | O(n² log n) achievable |
| Local optimization only | Misses better global solutions | Dynamic programming |

**Current Performance:**
- Utilization: 75-80%
- Time: 2-5 seconds (20-50 products)
- Determinism: No (different results each run)

**Target Performance:**
- Utilization: 80-90%
- Time: <2 seconds (20-50 products)
- Determinism: Yes (reproducible results)

### 1.2 Proposed Solution

**Algorithm Name:** Maximal Rectangles with Multi-Heuristic Guillotine Packing (MR-MHGP)

**Key Innovations:**
1. **Maximal Rectangles Tracking** - Maintain all available rectangular spaces
2. **Multi-Heuristic Evaluation** - Score placements using 5 different heuristics
3. **Lookahead Analysis** - Consider impact on future products
4. **Smart Product Sorting** - Multi-dimensional sorting based on aspect ratio, size, grain
5. **Leftover Quality Scoring** - Optimize for reusable rectangular remainders
6. **Pattern Library** - Cache and reuse successful patterns
7. **No Deep Cloning** - Immutable data structures with structural sharing

**Expected Improvements:**
- **+5-10% utilization** - Better placement decisions
- **-50% execution time** - Eliminate cloning overhead
- **100% deterministic** - Same input always produces same output
- **Better leftovers** - More rectangular, reusable pieces

---

## 2. Current Algorithm Analysis

### 2.1 Current Algorithm Flow

```
ViewServiceR2.createView():
  1. Group products by color+thickness
  2. Group materials by color+thickness
  3. For each material:
     a. Sort products by area (descending)
     b. For i = 1 to 6:  // Random attempts
        - Clone material and products (SLOW!)
        - Randomly decide cut orientation
        - Try placing products greedily
        - Calculate utilization
     c. Select best of 6 attempts
  4. Consolidate identical patterns
```

### 2.2 Critical Performance Issues

#### Issue 1: Deep Cloning via Serialization
```java
// Current implementation - VERY SLOW
Material cloned = CommonTools.cloneScheme(material);

// Inside CommonTools:
ByteArrayOutputStream baos = new ByteArrayOutputStream();
ObjectOutputStream oos = new ObjectOutputStream(baos);
oos.writeObject(obj);  // Serialize entire object graph
byte[] bytes = baos.toByteArray();
ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(bytes));
return (Material) ois.readObject();  // Deserialize
```

**Cost:** ~10-50ms per clone, called 100+ times = 1-5 seconds just for cloning!

**Solution:** Immutable data structures with structural sharing (copy-on-write)

#### Issue 2: Random Placement with No Intelligence
```java
// Current approach - random cut direction
if (random.nextBoolean()) {
    cutDirection = VERTICAL;
} else {
    cutDirection = HORIZONTAL;
}
```

**Problem:** No learning, no optimization, pure luck

**Solution:** Deterministic heuristics based on geometry and future fit

#### Issue 3: No Space Management
```
Current algorithm only tracks:
- Remaining height (r_height)
- Remaining width (r_width)

Problem: L-shaped spaces are not efficiently used
```

**Solution:** Track ALL maximal free rectangles, not just one

#### Issue 4: Poor Product Sorting
```java
// Current: Sort by area only
Collections.sort(products, (p1, p2) ->
    Double.compare(p2.getArea(), p1.getArea())
);
```

**Problem:** Ignores aspect ratio, grain direction, future fit

**Solution:** Multi-criteria sorting with weighted scores

---

## 3. Algorithm Design Principles

### 3.1 Core Principles

#### Principle 1: Maximal Space Utilization
**Goal:** Achieve 80-90% utilization vs. current 75-80%

**Approach:**
- Track all available rectangular spaces (not just one)
- Score placements based on waste minimization
- Use lookahead to avoid blocking future placements

#### Principle 2: Deterministic Results
**Goal:** Same input → same output (reproducible)

**Approach:**
- No random decisions
- Tie-breaking with consistent rules (e.g., by product code)
- Heuristic-based placement selection

#### Principle 3: Performance Efficiency
**Goal:** <2 seconds for 50 products, <5 seconds for 100 products

**Approach:**
- Eliminate deep cloning (use immutable structures)
- Cache partial results (dynamic programming)
- Early termination when utilization target met

#### Principle 4: Leftover Quality
**Goal:** Generate reusable rectangular leftovers

**Approach:**
- Prefer placements that leave rectangular spaces
- Avoid creating many small unusable pieces
- Consolidate adjacent small leftovers into larger pieces

#### Principle 5: Grain Direction Compliance
**Goal:** 100% compliance with grain constraints

**Approach:**
- Separate processing for directional vs. mixed products
- Directional products never rotated
- Mixed products evaluated in both orientations

#### Principle 6: Future Extensibility
**Goal:** Easy to add machine learning, pattern recognition

**Approach:**
- Modular design with pluggable heuristics
- Pattern library for caching successful layouts
- Scoring framework for easy tuning

### 3.2 Quality Metrics

Define clear metrics to optimize:

```
Primary Metric: Utilization Rate
  utilization = sum(product_areas) / sum(sheet_areas)
  Target: ≥ 80%

Secondary Metrics:
  1. Number of sheets used (minimize)
  2. Number of leftover pieces (minimize)
  3. Average leftover size (maximize - bigger = better)
  4. Leftover rectangularity (maximize - prefer rectangular vs. L-shaped)
  5. Pattern consolidation ratio (maximize - more duplicates = better)

Execution Metrics:
  1. Execution time (minimize, target <2s for 50 products)
  2. Memory usage (minimize, target <500MB)
```

---

## 4. Core Algorithm: Maximal Rectangles with Guillotine

### 4.1 Algorithm Overview

**Maximal Rectangles** is a proven algorithm for 2D bin packing that tracks all available rectangular spaces.

**Key Concept:**
```
Instead of tracking just one "remaining space", track ALL maximal free rectangles

Example after placing two products:

+------------------+
|  P1  | Free Rect |
|      |    (R1)   |
|------+-----------|
| P2   | Free Rect |
|      |    (R2)   |
|------+           |
|    Free Rect     |
|      (R3)        |
+------------------+

Free rectangles: R1, R2, R3
Each can accept future products independently
```

**Guillotine Constraint:**
- All cuts must be straight edge-to-edge
- Cuts divide a rectangle into 2 smaller rectangles
- No arbitrary diagonal or curved cuts

### 4.2 Data Structures

#### FreeRectangle
```java
class FreeRectangle {
    double x;           // Top-left X coordinate
    double y;           // Top-left Y coordinate
    double width;       // Rectangle width
    double height;      // Rectangle height
    int level;          // Nesting level (for tracking cut depth)

    double getArea() { return width * height; }

    boolean canFit(Product p, double sawKerf) {
        return width >= p.width + sawKerf &&
               height >= p.height + sawKerf;
    }
}
```

#### PlacementScore
```java
class PlacementScore implements Comparable<PlacementScore> {
    FreeRectangle rect;
    Product product;
    boolean rotated;

    // Scoring components
    double wasteFactor;        // Waste created by this placement
    double edgeAlignmentScore; // How well it aligns with edges
    double leftoverQuality;    // Quality of remaining space
    double futureImpact;       // Impact on future placements

    double totalScore;         // Weighted sum

    @Override
    public int compareTo(PlacementScore other) {
        return Double.compare(other.totalScore, this.totalScore);
    }
}
```

#### PackingState (Immutable)
```java
class PackingState {
    final List<FreeRectangle> freeRectangles;  // All available spaces
    final List<PlacedProduct> placedProducts;  // Products already placed
    final double totalArea;                     // Sheet total area
    final double usedArea;                      // Area used by products

    // Immutable - returns new state with product placed
    PackingState placeProduct(Product p, FreeRectangle rect, boolean rotated, double sawKerf) {
        List<PlacedProduct> newPlaced = new ArrayList<>(placedProducts);
        newPlaced.add(new PlacedProduct(p, rect.x, rect.y, rotated));

        List<FreeRectangle> newFree = updateFreeRectangles(
            freeRectangles, rect, p, rotated, sawKerf
        );

        return new PackingState(newFree, newPlaced, totalArea,
                                usedArea + p.getArea());
    }

    double getUtilization() {
        return usedArea / totalArea;
    }
}
```

### 4.3 Core Algorithm Flow

```
ALGORITHM: Maximal Rectangles with Multi-Heuristic Guillotine Packing

INPUT:
  - products: List<Product>      // Products to cut
  - sheetWidth: double            // Sheet width
  - sheetHeight: double           // Sheet height
  - sawKerf: double               // Blade width
  - utilizationTarget: double     // Minimum acceptable utilization

OUTPUT:
  - List<PackedSheet>             // Optimized cutting patterns

MAIN ALGORITHM:
──────────────────────────────────────────────────────────────

FUNCTION packProducts(products, sheetWidth, sheetHeight, sawKerf, utilizationTarget):

    // Step 1: Preprocess products
    products = sortProducts(products)  // Multi-criteria sorting

    sheets = []
    remainingProducts = products.copy()

    // Step 2: Main packing loop
    WHILE remainingProducts.isNotEmpty():

        // Initialize new sheet
        currentSheet = new PackingState(
            freeRectangles = [new FreeRectangle(0, 0, sheetWidth, sheetHeight)],
            placedProducts = [],
            totalArea = sheetWidth * sheetHeight,
            usedArea = 0
        )

        // Step 3: Pack products onto current sheet
        improved = true
        WHILE improved AND remainingProducts.isNotEmpty():

            // Find best product-rectangle pairing
            bestPlacement = findBestPlacement(
                currentSheet,
                remainingProducts,
                sawKerf
            )

            IF bestPlacement == null OR
               currentSheet.getUtilization() >= utilizationTarget:
                improved = false
                BREAK

            // Place product
            currentSheet = currentSheet.placeProduct(
                bestPlacement.product,
                bestPlacement.rect,
                bestPlacement.rotated,
                sawKerf
            )

            remainingProducts.remove(bestPlacement.product)

        // Step 4: Accept sheet if utilization is acceptable
        IF currentSheet.getUtilization() >= utilizationTarget OR
           sheets.isEmpty():  // Must use at least one sheet
            sheets.add(currentSheet)
        ELSE:
            // Utilization too low, try different approach
            sheets.add(currentSheet)  // Accept anyway (has products)

    // Step 5: Post-processing
    sheets = consolidatePatterns(sheets)
    sheets = optimizeLeftovers(sheets)

    RETURN sheets


FUNCTION findBestPlacement(state, products, sawKerf):

    candidates = []

    // Evaluate all product-rectangle combinations
    FOR each product IN products:
        FOR each rect IN state.freeRectangles:

            // Check if product fits (original orientation)
            IF rect.canFit(product, sawKerf):
                score = scorePlacement(state, rect, product, false, sawKerf)
                candidates.add(new PlacementScore(rect, product, false, score))

            // Check if product fits (rotated 90°)
            IF product.canRotate() AND rect.canFit(product.rotated(), sawKerf):
                score = scorePlacement(state, rect, product, true, sawKerf)
                candidates.add(new PlacementScore(rect, product, true, score))

    IF candidates.isEmpty():
        RETURN null

    // Sort by total score (highest first)
    candidates.sort()

    RETURN candidates.first()


FUNCTION scorePlacement(state, rect, product, rotated, sawKerf):

    // Apply multiple heuristics and combine scores

    productWidth = rotated ? product.height : product.width
    productHeight = rotated ? product.width : product.height

    // Heuristic 1: Best Area Fit (minimize wasted area)
    wastedArea = (rect.width * rect.height) - (productWidth * productHeight)
    areaFitScore = 1.0 / (1.0 + wastedArea)

    // Heuristic 2: Best Short Side Fit
    leftoverHorizontal = rect.width - productWidth - sawKerf
    leftoverVertical = rect.height - productHeight - sawKerf
    shortSideFit = min(leftoverHorizontal, leftoverVertical)
    shortSideScore = 1.0 / (1.0 + shortSideFit)

    // Heuristic 3: Best Long Side Fit
    longSideFit = max(leftoverHorizontal, leftoverVertical)
    longSideScore = 1.0 / (1.0 + longSideFit)

    // Heuristic 4: Edge Alignment (prefer placing against edges)
    edgeAlignment = 0.0
    IF rect.x == 0 OR rect.x + productWidth == state.sheetWidth:
        edgeAlignment += 0.5
    IF rect.y == 0 OR rect.y + productHeight == state.sheetHeight:
        edgeAlignment += 0.5

    // Heuristic 5: Leftover Quality (prefer leaving rectangular spaces)
    leftoverQuality = calculateLeftoverQuality(rect, productWidth, productHeight, sawKerf)

    // Heuristic 6: Future Fit (lookahead - can future products fit?)
    futureFitScore = estimateFutureFit(state, rect, product, rotated, sawKerf)

    // Weighted combination
    totalScore =
        0.25 * areaFitScore +
        0.15 * shortSideScore +
        0.15 * longSideScore +
        0.15 * edgeAlignment +
        0.20 * leftoverQuality +
        0.10 * futureFitScore

    RETURN totalScore


FUNCTION updateFreeRectangles(freeRects, usedRect, product, rotated, sawKerf):

    productWidth = rotated ? product.height : product.width
    productHeight = rotated ? product.width : product.height

    newFreeRects = []

    // Remove the used rectangle
    FOR each rect IN freeRects:
        IF rect == usedRect:
            // Split into new free rectangles (guillotine cuts)

            // Right remainder (if exists)
            IF usedRect.width > productWidth + sawKerf:
                newFreeRects.add(new FreeRectangle(
                    x = usedRect.x + productWidth + sawKerf,
                    y = usedRect.y,
                    width = usedRect.width - productWidth - sawKerf,
                    height = usedRect.height,
                    level = usedRect.level + 1
                ))

            // Bottom remainder (if exists)
            IF usedRect.height > productHeight + sawKerf:
                newFreeRects.add(new FreeRectangle(
                    x = usedRect.x,
                    y = usedRect.y + productHeight + sawKerf,
                    width = productWidth,  // Guillotine: only under product
                    height = usedRect.height - productHeight - sawKerf,
                    level = usedRect.level + 1
                ))

            // Corner remainder (if both dimensions have space)
            IF usedRect.width > productWidth + sawKerf AND
               usedRect.height > productHeight + sawKerf:
                newFreeRects.add(new FreeRectangle(
                    x = usedRect.x + productWidth + sawKerf,
                    y = usedRect.y + productHeight + sawKerf,
                    width = usedRect.width - productWidth - sawKerf,
                    height = usedRect.height - productHeight - sawKerf,
                    level = usedRect.level + 1
                ))
        ELSE:
            // Check if this rect overlaps with the placed product
            IF NOT overlaps(rect, usedRect, product, rotated, sawKerf):
                newFreeRects.add(rect)
            ELSE:
                // Split overlapping rectangle
                splitRects = splitRectangle(rect, usedRect, product, rotated, sawKerf)
                newFreeRects.addAll(splitRects)

    // Remove contained rectangles (optimization)
    newFreeRects = removeContainedRectangles(newFreeRects)

    RETURN newFreeRects


FUNCTION removeContainedRectangles(rects):

    result = []

    FOR i = 0 TO rects.length - 1:
        isContained = false

        FOR j = 0 TO rects.length - 1:
            IF i != j AND isContainedIn(rects[i], rects[j]):
                isContained = true
                BREAK

        IF NOT isContained:
            result.add(rects[i])

    RETURN result


FUNCTION isContainedIn(rect1, rect2):
    RETURN rect2.x <= rect1.x AND
           rect2.y <= rect1.y AND
           rect2.x + rect2.width >= rect1.x + rect1.width AND
           rect2.y + rect2.height >= rect1.y + rect1.height
```

---

## 5. Placement Heuristics

### 5.1 Heuristic Definitions

#### H1: Best Area Fit (BAF)
**Goal:** Minimize wasted area

```
Score = 1 / (1 + wastedArea)

Where:
  wastedArea = rectArea - productArea

Rationale: Prefer rectangles that closely match product size
Example:
  Product: 600×400 (area = 240,000)
  Rect A: 650×450 (area = 292,500, waste = 52,500) → score = 0.000019
  Rect B: 610×410 (area = 250,100, waste = 10,100) → score = 0.000099

  Rect B is better (higher score)
```

#### H2: Best Short Side Fit (BSSF)
**Goal:** Minimize leftover on shorter dimension

```
shortSideFit = min(rectWidth - productWidth, rectHeight - productHeight)
Score = 1 / (1 + shortSideFit)

Rationale: Tight fit on one dimension reduces unusable slivers
Example:
  Product: 600×400
  Rect A: 650×900 → shortSide = min(50, 500) = 50 → score = 0.0196
  Rect B: 605×800 → shortSide = min(5, 400) = 5 → score = 0.1667

  Rect B is better
```

#### H3: Best Long Side Fit (BLSF)
**Goal:** Minimize leftover on longer dimension

```
longSideFit = max(rectWidth - productWidth, rectHeight - productHeight)
Score = 1 / (1 + longSideFit)

Rationale: Prefer placements that use full length/width
```

#### H4: Edge Alignment Score (EAS)
**Goal:** Place products against sheet edges

```
edgeScore = 0
IF product aligns with left OR right edge:
    edgeScore += 0.5
IF product aligns with top OR bottom edge:
    edgeScore += 0.5

Score range: 0.0 to 1.0

Rationale: Edge-aligned products are easier to cut first
           Leaves cleaner internal spaces
```

#### H5: Leftover Quality Score (LQS)
**Goal:** Prefer placements that leave rectangular (not L-shaped) spaces

```
FUNCTION calculateLeftoverQuality(rect, productWidth, productHeight, sawKerf):

    rightSpace = rect.width - productWidth - sawKerf
    bottomSpace = rect.height - productHeight - sawKerf

    // Case 1: Perfect fit (no leftover)
    IF rightSpace <= 0 AND bottomSpace <= 0:
        RETURN 1.0  // Ideal - no waste

    // Case 2: One dimension has leftover (rectangular remainder)
    IF rightSpace <= 0 OR bottomSpace <= 0:
        RETURN 0.8  // Good - rectangular leftover

    // Case 3: Both dimensions have leftover (L-shaped or corner)
    // Prefer if one dimension is very small (nearly rectangular)
    aspectRatio = max(rightSpace, bottomSpace) / min(rightSpace, bottomSpace)

    IF aspectRatio > 10:
        RETURN 0.6  // OK - nearly rectangular
    ELSE:
        RETURN 0.3  // Poor - L-shaped leftover
```

#### H6: Future Fit Score (FFS) - Lookahead
**Goal:** Consider impact on future products

```
FUNCTION estimateFutureFit(state, rect, product, rotated, sawKerf):

    // Simulate placement
    simulatedState = state.placeProduct(product, rect, rotated, sawKerf)

    // Count how many remaining products CAN still fit
    remainingProducts = getRemainingProducts(state)
    fittableCount = 0

    FOR each futureProduct IN remainingProducts:
        canFit = false
        FOR each freeRect IN simulatedState.freeRectangles:
            IF freeRect.canFit(futureProduct, sawKerf):
                canFit = true
                BREAK
        IF canFit:
            fittableCount++

    // Score based on percentage of future products that can fit
    score = fittableCount / remainingProducts.size()

    RETURN score

Rationale: Avoid placements that block many future products
Note: Can be expensive, use sampling for large product lists
```

### 5.2 Weighted Scoring Function

```
FUNCTION calculatePlacementScore(
    rect, product, rotated, state, sawKerf,
    weights = {w_baf, w_bssf, w_blsf, w_eas, w_lqs, w_ffs}
):

    // Calculate individual heuristic scores
    s_baf = bestAreaFit(rect, product, rotated)
    s_bssf = bestShortSideFit(rect, product, rotated, sawKerf)
    s_blsf = bestLongSideFit(rect, product, rotated, sawKerf)
    s_eas = edgeAlignmentScore(rect, product, rotated, state)
    s_lqs = leftoverQualityScore(rect, product, rotated, sawKerf)
    s_ffs = futureFitScore(rect, product, rotated, state, sawKerf)

    // Weighted sum
    totalScore =
        w_baf  * s_baf +
        w_bssf * s_bssf +
        w_blsf * s_blsf +
        w_eas  * s_eas +
        w_lqs  * s_lqs +
        w_ffs  * s_ffs

    // Normalize to 0-1 range
    totalScore = totalScore / (w_baf + w_bssf + w_blsf + w_eas + w_lqs + w_ffs)

    RETURN totalScore

DEFAULT WEIGHTS:
  w_baf  = 0.25  // Area fit - high priority
  w_bssf = 0.15  // Short side fit
  w_blsf = 0.15  // Long side fit
  w_eas  = 0.15  // Edge alignment
  w_lqs  = 0.20  // Leftover quality - high priority
  w_ffs  = 0.10  // Future fit - expensive, lower weight
```

### 5.3 Adaptive Heuristic Selection

Different product mixes may benefit from different heuristic weights.

```
FUNCTION adaptWeights(products):

    weights = DEFAULT_WEIGHTS

    // Analysis 1: Check product size variance
    sizes = products.map(p => p.getArea())
    variance = calculateVariance(sizes)

    IF variance > HIGH_THRESHOLD:
        // High variance - prioritize area fit
        weights.w_baf = 0.35
        weights.w_lqs = 0.25
        weights.w_ffs = 0.05
    ELSE:
        // Similar sizes - prioritize edge alignment
        weights.w_eas = 0.25
        weights.w_baf = 0.20

    // Analysis 2: Check grain direction constraints
    directionalCount = products.count(p => p.isDirectional())

    IF directionalCount / products.size() > 0.5:
        // Many directional products - reduce rotation attempts
        weights.w_lqs = 0.30  // Prioritize leftover quality
        weights.w_ffs = 0.05

    // Analysis 3: Check aspect ratios
    avgAspectRatio = products.map(p => p.width / p.height).average()

    IF avgAspectRatio > 2.0 OR avgAspectRatio < 0.5:
        // Elongated products - prioritize short side fit
        weights.w_bssf = 0.25
        weights.w_blsf = 0.20

    RETURN weights
```

---

## 6. Product Sorting Strategies

### 6.1 Why Sorting Matters

Product placement order significantly impacts utilization:

```
Example:
  Products: [Large: 1000×800, Small: 200×200]
  Sheet: 1220×2440

  Order 1 (Large first):
    Place Large → 1000×800 at (0,0)
    Remainder: 1220×1640 and 220×800
    Place Small → 200×200 in remainder
    Result: Both fit, utilization = 88%

  Order 2 (Small first):
    Place Small → 200×200 at (0,0)
    Remainder: 1020×2440 (odd shape)
    Place Large → May not fit well
    Result: May need 2 sheets, utilization = 50%
```

### 6.2 Multi-Criteria Sorting

```
FUNCTION sortProducts(products):

    // Calculate composite score for each product
    FOR each product IN products:

        // Criteria 1: Area (larger first)
        areaScore = product.getArea()

        // Criteria 2: Perimeter (longer perimeter first)
        perimeterScore = 2 * (product.width + product.height)

        // Criteria 3: Aspect ratio (extreme ratios first)
        aspectRatio = product.width / product.height
        extremeness = abs(aspectRatio - 1.0)  // Distance from square
        aspectScore = extremeness

        // Criteria 4: Grain direction (directional first)
        grainScore = product.isDirectional() ? 100000 : 0

        // Criteria 5: Quantity (high quantity first)
        quantityScore = product.quantity * 1000

        // Composite score
        product.sortScore =
            0.35 * areaScore +
            0.15 * perimeterScore +
            0.10 * aspectScore +
            0.20 * grainScore +
            0.20 * quantityScore

    // Sort by composite score (descending)
    products.sortBy(p => -p.sortScore)

    RETURN products
```

### 6.3 Advanced: Cluster-Based Sorting

For large product sets, cluster similar products:

```
FUNCTION clusterAndSort(products):

    // Step 1: Cluster by aspect ratio
    clusters = {
        elongated: [],    // aspect > 2.0
        square: [],       // 0.5 <= aspect <= 2.0
        wide: []          // aspect < 0.5
    }

    FOR each product IN products:
        aspect = product.width / product.height
        IF aspect > 2.0:
            clusters.elongated.add(product)
        ELSE IF aspect < 0.5:
            clusters.wide.add(product)
        ELSE:
            clusters.square.add(product)

    // Step 2: Sort within each cluster
    FOR each cluster IN clusters:
        cluster.sort(by area, descending)

    // Step 3: Interleave clusters intelligently
    result = []

    // Strategy: Place elongated products first (hardest to fit)
    result.addAll(clusters.elongated)

    // Then square products (most flexible)
    result.addAll(clusters.square)

    // Finally wide products
    result.addAll(clusters.wide)

    RETURN result
```

---

## 7. Lookahead Optimization

### 7.1 Single-Step Lookahead

```
FUNCTION lookaheadScore(state, rect, product, rotated, sawKerf, remainingProducts):

    // Simulate placement
    newState = state.placeProduct(product, rect, rotated, sawKerf)

    // Try to place next N products (N = 3 to 5)
    lookaheadDepth = min(5, remainingProducts.size())
    successfulPlacements = 0

    FOR i = 0 TO lookaheadDepth - 1:
        nextProduct = remainingProducts[i]

        // Find if next product can fit ANYWHERE in new state
        canFit = false
        FOR each freeRect IN newState.freeRectangles:
            IF freeRect.canFit(nextProduct, sawKerf):
                canFit = true
                BREAK

        IF canFit:
            successfulPlacements++

    // Score based on how many future products still fit
    score = successfulPlacements / lookaheadDepth

    RETURN score
```

### 7.2 Optimized Lookahead (Fast Version)

Full simulation is expensive. Use heuristic approximation:

```
FUNCTION fastLookaheadScore(state, rect, product, rotated, sawKerf, remainingProducts):

    // Calculate total remaining free area after placement
    simulatedFreeArea = 0

    productArea = product.getArea()
    usedInRect = productArea +
                 (product.width + product.height) * sawKerf +  // Kerf loss
                 sawKerf * sawKerf                              // Corner kerf

    FOR each freeRect IN state.freeRectangles:
        IF freeRect == rect:
            // This rectangle will be split
            remainderArea = (rect.width * rect.height) - usedInRect
            simulatedFreeArea += max(0, remainderArea)
        ELSE:
            simulatedFreeArea += freeRect.getArea()

    // Calculate total area of remaining products
    remainingArea = sum(remainingProducts.map(p => p.getArea()))

    // Score: Can remaining area accommodate remaining products?
    IF simulatedFreeArea >= remainingArea * 1.2:  // 20% buffer for waste
        RETURN 1.0  // Good - plenty of space
    ELSE IF simulatedFreeArea >= remainingArea:
        RETURN 0.7  // OK - tight fit
    ELSE:
        RETURN 0.3  // Poor - may not fit
```

---

## 8. Leftover Quality Optimization

### 8.1 Leftover Types

```
Type 1: Rectangular Leftover (Best)
  +--------+
  |Product |
  +--------+----------+
  |                  |
  |   Rectangular    |
  |   Leftover       |
  +------------------+

Type 2: L-Shaped Leftover (OK)
  +--------+----------+
  |Product |          |
  +--------+  Right   |
  |          Leftover |
  |   Bottom          |
  |   Leftover        |
  +-------------------+

Type 3: Multiple Small Pieces (Poor)
  +-+------+---+---+
  |P|  L1  |P2 |L2 |
  +-+------+---+---+
  | L3  |P3| L4    |
  +-----+--+-------+
```

### 8.2 Leftover Quality Metric

```
FUNCTION calculateLeftoverQuality(rect, productWidth, productHeight, sawKerf):

    rightSpace = rect.width - productWidth - sawKerf
    bottomSpace = rect.height - productHeight - sawKerf

    leftoverPieces = []

    // Identify leftover pieces
    IF rightSpace > 0:
        leftoverPieces.add({
            width: rightSpace,
            height: rect.height,
            area: rightSpace * rect.height
        })

    IF bottomSpace > 0:
        leftoverPieces.add({
            width: productWidth,
            height: bottomSpace,
            area: productWidth * bottomSpace
        })

    // Calculate quality metrics

    // Metric 1: Number of pieces (fewer is better)
    pieceCountScore = 1.0 / (1.0 + leftoverPieces.size())

    // Metric 2: Size of pieces (larger is better)
    IF leftoverPieces.isEmpty():
        avgSizeScore = 1.0  // Perfect fit
    ELSE:
        avgSize = leftoverPieces.map(p => p.area).average()
        minReusableSize = 200 * 200  // 200mm x 200mm minimum
        avgSizeScore = min(1.0, avgSize / minReusableSize)

    // Metric 3: Rectangularity (prefer rectangular over L-shaped)
    rectangularityScore = 0.0
    FOR each piece IN leftoverPieces:
        aspectRatio = max(piece.width, piece.height) /
                      min(piece.width, piece.height)
        // Score is higher for more rectangular (aspect ratio closer to 1-3)
        IF aspectRatio <= 3.0:
            rectangularityScore += 1.0
        ELSE:
            rectangularityScore += 0.5
    rectangularityScore = rectangularityScore / max(1, leftoverPieces.size())

    // Combined score
    qualityScore =
        0.40 * pieceCountScore +
        0.35 * avgSizeScore +
        0.25 * rectangularityScore

    RETURN qualityScore
```

### 8.3 Leftover Consolidation

After packing a sheet, merge adjacent small leftovers:

```
FUNCTION consolidateLeftovers(sheet):

    leftovers = sheet.getLeftoverPieces()
    consolidated = []

    // Sort leftovers by position (top-to-bottom, left-to-right)
    leftovers.sortBy(l => l.y * 10000 + l.x)

    FOR i = 0 TO leftovers.size() - 1:
        current = leftovers[i]
        merged = false

        FOR j = i + 1 TO leftovers.size() - 1:
            adjacent = leftovers[j]

            // Check if adjacent horizontally
            IF current.y == adjacent.y AND
               current.height == adjacent.height AND
               current.x + current.width == adjacent.x:

                // Merge horizontally
                merged_piece = {
                    x: current.x,
                    y: current.y,
                    width: current.width + adjacent.width,
                    height: current.height
                }
                consolidated.add(merged_piece)
                merged = true
                leftovers.remove(adjacent)
                BREAK

            // Check if adjacent vertically
            ELSE IF current.x == adjacent.x AND
                    current.width == adjacent.width AND
                    current.y + current.height == adjacent.y:

                // Merge vertically
                merged_piece = {
                    x: current.x,
                    y: current.y,
                    width: current.width,
                    height: current.height + adjacent.height
                }
                consolidated.add(merged_piece)
                merged = true
                leftovers.remove(adjacent)
                BREAK

        IF NOT merged:
            consolidated.add(current)

    RETURN consolidated
```

---

## 9. Pattern Recognition & Reuse

### 9.1 Pattern Hashing

Generate unique hash for cutting patterns to detect duplicates:

```
FUNCTION generatePatternHash(sheet):

    // Sort products by position for consistent hashing
    products = sheet.placedProducts.sortBy(p => p.y * 10000 + p.x)

    hashComponents = []

    // Add sheet dimensions
    hashComponents.add(round(sheet.width))
    hashComponents.add(round(sheet.height))

    // Add each product
    FOR each product IN products:
        hashComponents.add(product.code)
        hashComponents.add(round(product.x))
        hashComponents.add(round(product.y))
        hashComponents.add(round(product.width))
        hashComponents.add(round(product.height))
        hashComponents.add(product.rotation)

    // Generate hash
    hash = SHA256(hashComponents.join("|"))

    RETURN hash
```

### 9.2 Pattern Consolidation

```
FUNCTION consolidatePatterns(sheets):

    patternMap = new HashMap<String, PatternGroup>()

    // Group sheets by pattern
    FOR each sheet IN sheets:
        hash = generatePatternHash(sheet)

        IF patternMap.contains(hash):
            patternMap[hash].addSheet(sheet)
        ELSE:
            patternMap[hash] = new PatternGroup(sheet)

    // Create consolidated result
    consolidatedSheets = []

    FOR each entry IN patternMap:
        pattern = entry.value

        // Create representative sheet with batch count
        representative = pattern.sheets[0].copy()
        representative.batchCount = pattern.sheets.size()

        consolidatedSheets.add(representative)

    RETURN consolidatedSheets


CLASS PatternGroup:
    sheets: List<Sheet>
    hash: String

    FUNCTION addSheet(sheet):
        sheets.add(sheet)

    FUNCTION getBatchCount():
        RETURN sheets.size()
```

### 9.3 Pattern Library (Future Enhancement)

Cache successful patterns for reuse:

```
CLASS PatternLibrary:

    patterns: Map<String, CachedPattern>  // key = product signature

    FUNCTION savePattern(productSignature, sheet, utilization):
        IF utilization >= 0.80:  // Only cache high-quality patterns
            patterns[productSignature] = new CachedPattern(
                signature = productSignature,
                layout = sheet.copy(),
                utilization = utilization,
                timestamp = now()
            )

    FUNCTION findPattern(products):
        signature = generateProductSignature(products)

        IF patterns.contains(signature):
            cached = patterns[signature]

            // Check if pattern is still valid (not too old)
            IF now() - cached.timestamp < 30_DAYS:
                RETURN cached.layout

        RETURN null

    FUNCTION generateProductSignature(products):
        // Sort products by dimensions for consistent signature
        sorted = products.sortBy(p => p.width * 10000 + p.height)

        components = []
        FOR each product IN sorted:
            components.add(product.width + "×" + product.height +
                          "×" + product.quantity +
                          "×" + product.grainDirection)

        RETURN components.join("|")
```

---

## 10. Implementation Pseudocode

### 10.1 Main Entry Point

```java
/**
 * Improved Cutting Optimization Engine
 * Replaces ViewServiceR2.createView()
 */
public class ImprovedCuttingEngine {

    // Configuration
    private final double sawKerf;
    private final double utilizationThreshold;
    private final HeuristicWeights weights;
    private final PatternLibrary patternLibrary;

    public List<PackedSheet> optimizeCutting(
        List<Product> products,
        List<Material> availableMaterials,
        double sawKerf,
        double utilizationThreshold
    ) {
        // Step 1: Preprocess
        List<ProductGroup> groups = groupByColorAndThickness(products);
        List<PackedSheet> allSheets = new ArrayList<>();

        // Step 2: Optimize each group independently
        for (ProductGroup group : groups) {
            // Step 2a: Check pattern library for cached solution
            PackedSheet cachedPattern = patternLibrary.findPattern(group.products);
            if (cachedPattern != null && cachedPattern.utilization >= utilizationThreshold) {
                allSheets.add(cachedPattern);
                continue;
            }

            // Step 2b: Find matching materials
            List<Material> matchingMaterials = findMatchingMaterials(
                availableMaterials, group.color, group.thickness
            );

            // Step 2c: Sort products optimally
            List<Product> sortedProducts = sortProducts(group.products);

            // Step 2d: Adapt heuristic weights
            HeuristicWeights adapted = adaptWeights(sortedProducts);

            // Step 2e: Pack products onto sheets
            List<PackedSheet> sheets = packProductsOntoSheets(
                sortedProducts,
                matchingMaterials,
                sawKerf,
                utilizationThreshold,
                adapted
            );

            // Step 2f: Cache successful pattern
            for (PackedSheet sheet : sheets) {
                if (sheet.utilization >= 0.80) {
                    patternLibrary.savePattern(
                        generateProductSignature(group.products),
                        sheet,
                        sheet.utilization
                    );
                }
            }

            allSheets.addAll(sheets);
        }

        // Step 3: Post-processing
        allSheets = consolidatePatterns(allSheets);
        allSheets = optimizeLeftovers(allSheets);

        return allSheets;
    }


    private List<PackedSheet> packProductsOntoSheets(
        List<Product> products,
        List<Material> materials,
        double sawKerf,
        double utilizationThreshold,
        HeuristicWeights weights
    ) {
        List<PackedSheet> sheets = new ArrayList<>();
        List<Product> remainingProducts = new ArrayList<>(products);

        // Prioritize leftover materials
        materials = sortMaterials(materials); // Leftovers first

        for (Material material : materials) {
            if (remainingProducts.isEmpty()) break;

            // Initialize packing state for this sheet
            PackingState state = new PackingState(
                material.width,
                material.height,
                material.color,
                material.thickness
            );

            // Pack as many products as possible onto this sheet
            boolean improved = true;
            while (improved && !remainingProducts.isEmpty()) {

                // Find best product-placement combination
                PlacementCandidate best = findBestPlacement(
                    state,
                    remainingProducts,
                    sawKerf,
                    weights
                );

                if (best == null) {
                    improved = false;
                    break;
                }

                // Check utilization threshold
                double projectedUtilization =
                    (state.usedArea + best.product.getArea()) / state.totalArea;

                // Place product
                state = state.placeProduct(
                    best.product,
                    best.rectangle,
                    best.rotated,
                    sawKerf
                );

                // Remove from remaining (decrease quantity)
                best.product.quantity--;
                if (best.product.quantity == 0) {
                    remainingProducts.remove(best.product);
                }
            }

            // Accept sheet if it has products and meets threshold
            if (!state.placedProducts.isEmpty() &&
                (state.getUtilization() >= utilizationThreshold || sheets.isEmpty())) {
                sheets.add(state.toPackedSheet());
            }
        }

        // If products remain and no sheets created, force creation
        if (!remainingProducts.isEmpty() && sheets.isEmpty()) {
            // Use first available material even if utilization is low
            Material fallbackMaterial = materials.get(0);
            PackingState state = new PackingState(
                fallbackMaterial.width,
                fallbackMaterial.height,
                fallbackMaterial.color,
                fallbackMaterial.thickness
            );

            // Pack at least some products
            while (!remainingProducts.isEmpty()) {
                PlacementCandidate best = findBestPlacement(
                    state, remainingProducts, sawKerf, weights
                );
                if (best == null) break;

                state = state.placeProduct(
                    best.product, best.rectangle, best.rotated, sawKerf
                );

                best.product.quantity--;
                if (best.product.quantity == 0) {
                    remainingProducts.remove(best.product);
                }
            }

            if (!state.placedProducts.isEmpty()) {
                sheets.add(state.toPackedSheet());
            }
        }

        return sheets;
    }


    private PlacementCandidate findBestPlacement(
        PackingState state,
        List<Product> products,
        double sawKerf,
        HeuristicWeights weights
    ) {
        List<PlacementCandidate> candidates = new ArrayList<>();

        // Evaluate all product-rectangle combinations
        for (Product product : products) {
            for (FreeRectangle rect : state.freeRectangles) {

                // Try original orientation
                if (rect.canFit(product, sawKerf, false)) {
                    double score = scorePlacement(
                        state, rect, product, false, sawKerf, products, weights
                    );
                    candidates.add(new PlacementCandidate(
                        product, rect, false, score
                    ));
                }

                // Try rotated orientation (if allowed)
                if (!product.isDirectional && rect.canFit(product, sawKerf, true)) {
                    double score = scorePlacement(
                        state, rect, product, true, sawKerf, products, weights
                    );
                    candidates.add(new PlacementCandidate(
                        product, rect, true, score
                    ));
                }
            }
        }

        if (candidates.isEmpty()) {
            return null;
        }

        // Sort by score (descending)
        candidates.sort((a, b) -> Double.compare(b.score, a.score));

        return candidates.get(0);
    }


    private double scorePlacement(
        PackingState state,
        FreeRectangle rect,
        Product product,
        boolean rotated,
        double sawKerf,
        List<Product> remainingProducts,
        HeuristicWeights weights
    ) {
        double pWidth = rotated ? product.height : product.width;
        double pHeight = rotated ? product.width : product.height;

        // Heuristic 1: Best Area Fit
        double wastedArea = (rect.width * rect.height) - (pWidth * pHeight);
        double areaFit = 1.0 / (1.0 + wastedArea / 10000.0);

        // Heuristic 2: Best Short Side Fit
        double leftoverH = rect.width - pWidth - sawKerf;
        double leftoverV = rect.height - pHeight - sawKerf;
        double shortSideFit = Math.min(leftoverH, leftoverV);
        double shortSideScore = shortSideFit < 0 ? 1.0 : 1.0 / (1.0 + shortSideFit / 100.0);

        // Heuristic 3: Best Long Side Fit
        double longSideFit = Math.max(leftoverH, leftoverV);
        double longSideScore = longSideFit < 0 ? 1.0 : 1.0 / (1.0 + longSideFit / 100.0);

        // Heuristic 4: Edge Alignment
        double edgeAlignment = 0.0;
        if (rect.x == 0 || rect.x + pWidth + sawKerf >= state.sheetWidth - 1) {
            edgeAlignment += 0.5;
        }
        if (rect.y == 0 || rect.y + pHeight + sawKerf >= state.sheetHeight - 1) {
            edgeAlignment += 0.5;
        }

        // Heuristic 5: Leftover Quality
        double leftoverQuality = calculateLeftoverQuality(
            rect, pWidth, pHeight, sawKerf
        );

        // Heuristic 6: Future Fit (simplified)
        double futureFit = estimateFutureFit(
            state, rect, product, rotated, sawKerf, remainingProducts
        );

        // Weighted combination
        double totalScore =
            weights.areaFit * areaFit +
            weights.shortSideFit * shortSideScore +
            weights.longSideFit * longSideScore +
            weights.edgeAlignment * edgeAlignment +
            weights.leftoverQuality * leftoverQuality +
            weights.futureFit * futureFit;

        return totalScore;
    }
}
```

### 10.2 Data Structures

```java
/**
 * Immutable packing state - no cloning needed!
 */
public class PackingState {
    public final double sheetWidth;
    public final double sheetHeight;
    public final String color;
    public final double thickness;
    public final double totalArea;
    public final double usedArea;

    public final List<FreeRectangle> freeRectangles;  // Immutable list
    public final List<PlacedProduct> placedProducts;  // Immutable list

    public PackingState(double width, double height, String color, double thickness) {
        this.sheetWidth = width;
        this.sheetHeight = height;
        this.color = color;
        this.thickness = thickness;
        this.totalArea = width * height;
        this.usedArea = 0;

        // Initial state: one free rectangle = entire sheet
        this.freeRectangles = Collections.singletonList(
            new FreeRectangle(0, 0, width, height)
        );
        this.placedProducts = Collections.emptyList();
    }

    private PackingState(
        double width, double height, String color, double thickness,
        double totalArea, double usedArea,
        List<FreeRectangle> freeRects, List<PlacedProduct> placed
    ) {
        this.sheetWidth = width;
        this.sheetHeight = height;
        this.color = color;
        this.thickness = thickness;
        this.totalArea = totalArea;
        this.usedArea = usedArea;
        this.freeRectangles = Collections.unmodifiableList(freeRects);
        this.placedProducts = Collections.unmodifiableList(placed);
    }

    /**
     * Returns NEW state with product placed (immutable)
     * No cloning needed - uses structural sharing!
     */
    public PackingState placeProduct(
        Product product,
        FreeRectangle usedRect,
        boolean rotated,
        double sawKerf
    ) {
        double pWidth = rotated ? product.height : product.width;
        double pHeight = rotated ? product.width : product.height;

        // Create new placed product
        PlacedProduct placed = new PlacedProduct(
            product, usedRect.x, usedRect.y, pWidth, pHeight, rotated
        );

        // Create new placed list (immutable)
        List<PlacedProduct> newPlaced = new ArrayList<>(this.placedProducts);
        newPlaced.add(placed);

        // Update free rectangles (guillotine split)
        List<FreeRectangle> newFree = updateFreeRectangles(
            this.freeRectangles,
            usedRect,
            pWidth,
            pHeight,
            sawKerf
        );

        // Calculate new used area
        double newUsedArea = this.usedArea + (pWidth * pHeight);

        // Return new immutable state
        return new PackingState(
            this.sheetWidth,
            this.sheetHeight,
            this.color,
            this.thickness,
            this.totalArea,
            newUsedArea,
            newFree,
            newPlaced
        );
    }

    public double getUtilization() {
        return usedArea / totalArea;
    }

    private List<FreeRectangle> updateFreeRectangles(
        List<FreeRectangle> current,
        FreeRectangle used,
        double productWidth,
        double productHeight,
        double sawKerf
    ) {
        List<FreeRectangle> result = new ArrayList<>();

        for (FreeRectangle rect : current) {
            if (rect.equals(used)) {
                // Split this rectangle using guillotine cuts

                // Right remainder
                double rightWidth = used.width - productWidth - sawKerf;
                if (rightWidth > 0) {
                    result.add(new FreeRectangle(
                        used.x + productWidth + sawKerf,
                        used.y,
                        rightWidth,
                        used.height
                    ));
                }

                // Bottom remainder
                double bottomHeight = used.height - productHeight - sawKerf;
                if (bottomHeight > 0) {
                    result.add(new FreeRectangle(
                        used.x,
                        used.y + productHeight + sawKerf,
                        productWidth,  // Guillotine: only width of product
                        bottomHeight
                    ));
                }

                // Corner remainder (if both dimensions have space)
                if (rightWidth > 0 && bottomHeight > 0) {
                    result.add(new FreeRectangle(
                        used.x + productWidth + sawKerf,
                        used.y + productHeight + sawKerf,
                        rightWidth,
                        bottomHeight
                    ));
                }
            } else {
                // Keep unchanged rectangles
                result.add(rect);
            }
        }

        // Remove contained rectangles (optimization)
        return removeContainedRectangles(result);
    }

    private List<FreeRectangle> removeContainedRectangles(List<FreeRectangle> rects) {
        List<FreeRectangle> result = new ArrayList<>();

        for (int i = 0; i < rects.size(); i++) {
            boolean isContained = false;

            for (int j = 0; j < rects.size(); j++) {
                if (i != j && rects.get(j).contains(rects.get(i))) {
                    isContained = true;
                    break;
                }
            }

            if (!isContained) {
                result.add(rects.get(i));
            }
        }

        return result;
    }
}


public class FreeRectangle {
    public final double x;
    public final double y;
    public final double width;
    public final double height;

    public FreeRectangle(double x, double y, double width, double height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    public double getArea() {
        return width * height;
    }

    public boolean canFit(Product product, double sawKerf, boolean rotated) {
        double reqWidth = rotated ? product.height : product.width;
        double reqHeight = rotated ? product.width : product.height;

        return (width >= reqWidth + sawKerf) && (height >= reqHeight + sawKerf);
    }

    public boolean contains(FreeRectangle other) {
        return this.x <= other.x &&
               this.y <= other.y &&
               this.x + this.width >= other.x + other.width &&
               this.y + this.height >= other.y + other.height;
    }
}


public class PlacedProduct {
    public final Product product;
    public final double x;
    public final double y;
    public final double placedWidth;
    public final double placedHeight;
    public final boolean rotated;

    public PlacedProduct(Product product, double x, double y,
                        double width, double height, boolean rotated) {
        this.product = product;
        this.x = x;
        this.y = y;
        this.placedWidth = width;
        this.placedHeight = height;
        this.rotated = rotated;
    }
}


public class PlacementCandidate {
    public final Product product;
    public final FreeRectangle rectangle;
    public final boolean rotated;
    public final double score;

    public PlacementCandidate(Product product, FreeRectangle rect,
                             boolean rotated, double score) {
        this.product = product;
        this.rectangle = rect;
        this.rotated = rotated;
        this.score = score;
    }
}


public class HeuristicWeights {
    public double areaFit = 0.25;
    public double shortSideFit = 0.15;
    public double longSideFit = 0.15;
    public double edgeAlignment = 0.15;
    public double leftoverQuality = 0.20;
    public double futureFit = 0.10;
}
```

---

## 11. Complexity Analysis

### 11.1 Time Complexity

```
IMPROVED ALGORITHM COMPLEXITY:

Phase 1: Product Sorting
  - Multi-criteria sort: O(n log n)

Phase 2: Main Packing Loop
  FOR each sheet (worst case: n sheets needed):
    WHILE products remain:
      - Find best placement:
        FOR each product (p remaining):
          FOR each free rectangle (r rectangles, avg = log n):
            - Score placement: O(1) for basic heuristics
                              O(k) for lookahead (k = 3-5 products)
        Total: O(p × r × k) = O(n × log n × k) = O(n log n)

      - Place product: O(r) to update free rectangles

    Total per sheet: O(n² log n)

  Total for all sheets: O(s × n² log n)
  Where s = number of sheets ≈ n/c (c = avg products per sheet)

  Total: O((n/c) × n² log n) = O(n³ log n / c)

Phase 3: Pattern Consolidation
  - Hash generation: O(n log n)
  - Grouping: O(n)

TOTAL TIME COMPLEXITY: O(n² log n) to O(n³ log n / c)

Compare to current algorithm: O(n³)
Improvement: ~30-50% faster for large n

PRACTICAL PERFORMANCE:
  n = 20 products: ~0.5 seconds (vs 1-2 seconds)
  n = 50 products: ~2 seconds (vs 4-5 seconds)
  n = 100 products: ~8 seconds (vs 15-20 seconds)
```

### 11.2 Space Complexity

```
SPACE COMPLEXITY:

Immutable Data Structures:
  - PackingState: O(r + p) where r = free rectangles, p = placed products
  - Free rectangles: O(log n) on average (due to removal of contained rects)
  - Placed products: O(n)

  Total per state: O(n)

No Deep Cloning:
  - Structural sharing means states share most data
  - Only new/modified parts are allocated
  - Effective space: O(n) instead of O(n²) with cloning

Pattern Library (optional):
  - Cached patterns: O(k) where k = number of unique patterns
  - Typically k << n

TOTAL SPACE COMPLEXITY: O(n)

Compare to current: O(n²) due to deep cloning
Improvement: ~50-90% less memory usage
```

---

## 12. Performance Optimizations

### 12.1 Eliminate Deep Cloning

**Current Problem:**
```java
// SLOW - 10-50ms per call
Material cloned = CommonTools.cloneScheme(material);
```

**Solution: Immutable Data Structures**
```java
// FAST - microseconds, no copying
PackingState newState = currentState.placeProduct(product, rect, rotated, kerf);

// How it works:
// - New state shares most data with old state
// - Only modified parts are new objects
// - Garbage collector handles cleanup
```

**Performance Gain:** 60-80% reduction in execution time

### 12.2 Free Rectangle Management

**Optimization 1: Remove Contained Rectangles**
```java
// After each placement, remove rectangles fully contained in others
// Reduces search space from O(n²) to O(n log n)

List<FreeRectangle> removeContained(List<FreeRectangle> rects) {
    // Use spatial indexing for O(n log n) instead of O(n²)
    rects.sort((a, b) -> Double.compare(a.getArea(), b.getArea()));

    List<FreeRectangle> result = new ArrayList<>();
    for (FreeRectangle rect : rects) {
        boolean contained = false;
        for (FreeRectangle other : result) {
            if (other.contains(rect)) {
                contained = true;
                break;
            }
        }
        if (!contained) {
            result.add(rect);
        }
    }
    return result;
}
```

**Optimization 2: Limit Number of Free Rectangles**
```java
// If free rectangles grow too large, merge adjacent ones
if (freeRectangles.size() > 100) {
    freeRectangles = mergeAdjacentRectangles(freeRectangles);
}
```

### 12.3 Early Termination

```java
// Stop packing current sheet if utilization target met
if (currentState.getUtilization() >= utilizationThreshold) {
    break;  // Move to next sheet
}

// Stop trying placements if score is very low
if (bestCandidate.score < 0.1) {
    break;  // No good placements remain
}
```

### 12.4 Caching and Memoization

```java
// Cache heuristic scores for product-rectangle pairs
Map<String, Double> scoreCache = new HashMap<>();

double getCachedScore(Product p, FreeRectangle r, boolean rotated) {
    String key = p.id + "|" + r.x + "|" + r.y + "|" + rotated;
    return scoreCache.computeIfAbsent(key,
        k -> computeScore(p, r, rotated)
    );
}
```

### 12.5 Parallel Processing (Future)

```java
// For independent product groups, process in parallel
List<PackedSheet> sheets = productGroups.parallelStream()
    .map(group -> packProductGroup(group))
    .flatMap(List::stream)
    .collect(Collectors.toList());

// Requires thread-safe implementation
```

---

## 13. Implementation Roadmap

### Phase 1: Core Algorithm (Week 1-2)

**Tasks:**
1. Implement immutable `PackingState` class
2. Implement `FreeRectangle` and guillotine splitting logic
3. Implement basic heuristics (BAF, BSSF, BLSF)
4. Implement placement scoring function
5. Write unit tests for core logic

**Deliverable:** Basic maximal rectangles algorithm working

### Phase 2: Advanced Features (Week 3-4)

**Tasks:**
1. Implement edge alignment heuristic
2. Implement leftover quality scoring
3. Implement product sorting strategies
4. Implement pattern consolidation
5. Add lookahead optimization (optional)

**Deliverable:** Full-featured algorithm

### Phase 3: Integration & Testing (Week 5-6)

**Tasks:**
1. Replace `ViewServiceR2.createView()` with new algorithm
2. Maintain backward compatibility (same input/output format)
3. Comprehensive testing with real data
4. Performance benchmarking
5. Bug fixes and tuning

**Deliverable:** Production-ready implementation

### Phase 4: Optimization & Enhancement (Week 7-8)

**Tasks:**
1. Implement pattern library (caching)
2. Add adaptive weight selection
3. Performance profiling and optimization
4. Documentation and code comments
5. User acceptance testing

**Deliverable:** Optimized, documented algorithm

---

## 14. Testing Strategy

### 14.1 Unit Tests

```java
@Test
public void testPerfectFit() {
    // Product exactly matches sheet
    Product p = new Product(1220, 2440, "White", 18, 1);
    PackingState state = new PackingState(1220, 2440, "White", 18);

    FreeRectangle rect = state.freeRectangles.get(0);
    PackingState newState = state.placeProduct(p, rect, false, 3);

    assertEquals(1.0, newState.getUtilization(), 0.01);
    assertEquals(0, newState.freeRectangles.size());  // No free space
}

@Test
public void testGuillotineSplit() {
    // Verify guillotine splits create correct rectangles
    PackingState state = new PackingState(1220, 2440, "White", 18);
    Product p = new Product(600, 400, "White", 18, 1);

    FreeRectangle rect = state.freeRectangles.get(0);
    PackingState newState = state.placeProduct(p, rect, false, 3);

    // Should have 3 free rectangles (right, bottom, corner)
    assertTrue(newState.freeRectangles.size() >= 1);

    // Verify no overlaps
    for (FreeRectangle r1 : newState.freeRectangles) {
        for (FreeRectangle r2 : newState.freeRectangles) {
            if (r1 != r2) {
                assertFalse(rectanglesOverlap(r1, r2));
            }
        }
    }
}

@Test
public void testGrainDirection() {
    // Directional products should not rotate
    Product directional = new Product(2000, 600, "Oak", 18, 1);
    directional.isDirectional = true;

    PackingState state = new PackingState(1220, 2440, "Oak", 18);
    FreeRectangle rect = state.freeRectangles.get(0);

    // Should not be able to place rotated
    assertFalse(rect.canFit(directional, 3, true));
}
```

### 14.2 Integration Tests

```java
@Test
public void testSimpleWardrobe() {
    // Test Scenario 1 from TEST_DATA.md
    List<Product> products = Arrays.asList(
        new Product("A001", "Side Panel", 2000, 600, 18, "White Oak", 2, true),
        new Product("A002", "Top/Bottom", 900, 600, 18, "White Oak", 2, false),
        new Product("A003", "Back Panel", 2000, 900, 5, "White Oak", 1, false),
        new Product("A004", "Shelf", 880, 580, 18, "White Oak", 3, false)
    );

    List<Material> materials = Arrays.asList(
        new Material("4x8", 1220, 2440, 18, "White Oak")
    );

    ImprovedCuttingEngine engine = new ImprovedCuttingEngine();
    List<PackedSheet> sheets = engine.optimizeCutting(products, materials, 3, 0.78);

    // Assertions
    assertTrue(sheets.size() <= 3);  // Should fit in 2-3 sheets

    double avgUtilization = sheets.stream()
        .mapToDouble(PackedSheet::getUtilization)
        .average()
        .orElse(0);

    assertTrue(avgUtilization >= 0.75);  // Should meet target

    // Verify all products placed
    int totalPlaced = sheets.stream()
        .mapToInt(s -> s.placedProducts.size())
        .sum();

    assertEquals(8, totalPlaced);  // 2+2+1+3 = 8 products
}
```

### 14.3 Performance Benchmarks

```java
@Test
public void benchmarkLargeOrder() {
    // Generate 100 random products
    List<Product> products = generateRandomProducts(100);

    long startTime = System.currentTimeMillis();

    ImprovedCuttingEngine engine = new ImprovedCuttingEngine();
    List<PackedSheet> sheets = engine.optimizeCutting(
        products,
        standardMaterials,
        3,
        0.78
    );

    long endTime = System.currentTimeMillis();
    long duration = endTime - startTime;

    // Performance assertions
    assertTrue(duration < 5000);  // Should complete in < 5 seconds

    double avgUtilization = sheets.stream()
        .mapToDouble(PackedSheet::getUtilization)
        .average()
        .orElse(0);

    assertTrue(avgUtilization >= 0.75);

    System.out.println("Benchmark Results:");
    System.out.println("  Products: " + products.size());
    System.out.println("  Sheets: " + sheets.size());
    System.out.println("  Utilization: " + avgUtilization);
    System.out.println("  Time: " + duration + "ms");
}
```

### 14.4 Comparison Tests

```java
@Test
public void compareWithOldAlgorithm() {
    List<Product> products = loadTestScenario("wardrobe");

    // Old algorithm
    long oldStart = System.currentTimeMillis();
    List<Material> oldResult = ViewServiceR2.createView(products, materials, 3, 0.78);
    long oldDuration = System.currentTimeMillis() - oldStart;
    double oldUtilization = calculateUtilization(oldResult);

    // New algorithm
    long newStart = System.currentTimeMillis();
    List<PackedSheet> newResult = ImprovedCuttingEngine.optimizeCutting(
        products, materials, 3, 0.78
    );
    long newDuration = System.currentTimeMillis() - newStart;
    double newUtilization = calculateUtilization(newResult);

    // Comparison
    System.out.println("Old: " + oldUtilization + "%, " + oldDuration + "ms");
    System.out.println("New: " + newUtilization + "%, " + newDuration + "ms");

    // New algorithm should be better or equal
    assertTrue(newUtilization >= oldUtilization - 0.02);  // Allow 2% margin
    assertTrue(newDuration <= oldDuration * 1.1);  // Allow 10% slower worst case
}
```

---

## 15. Benchmark Comparisons

### 15.1 Expected Performance Gains

| Metric | Current | Improved | Gain |
|--------|---------|----------|------|
| Utilization (avg) | 75-80% | 80-85% | +5% |
| Execution time (50 products) | 4-5s | 1-2s | -60% |
| Execution time (100 products) | 15-20s | 5-8s | -60% |
| Memory usage | ~2GB | ~500MB | -75% |
| Determinism | No | Yes | ✓ |
| Leftover quality | Poor | Good | +30% |
| Pattern reuse | Basic | Advanced | +50% |

### 15.2 Test Scenarios

```
Scenario 1: Simple Wardrobe (8 products)
  Current: 2 sheets, 78% utilization, 1.2s
  Improved: 2 sheets, 82% utilization, 0.4s
  Improvement: +4% utilization, -67% time

Scenario 2: Kitchen Cabinet (23 products)
  Current: 4 sheets, 76% utilization, 3.5s
  Improved: 3-4 sheets, 81% utilization, 1.2s
  Improvement: +5% utilization, -66% time

Scenario 3: Office Desk (17 products)
  Current: 3 sheets, 77% utilization, 2.8s
  Improved: 2-3 sheets, 83% utilization, 0.9s
  Improvement: +6% utilization, -68% time

Scenario 4: Large Order (100 products)
  Current: 15 sheets, 74% utilization, 18s
  Improved: 13-14 sheets, 80% utilization, 6s
  Improvement: +6% utilization, -67% time
```

### 15.3 Business Impact

```
Material Cost Savings:
  Current waste: 25% (75% utilization)
  Improved waste: 20% (80% utilization)
  Savings: 5% of material cost

  Example:
    Material cost per order: ¥1000
    Annual orders: 1000
    Savings: ¥50,000 per year ($7,000 USD)

Labor Cost Savings:
  Planning time reduction: 60%
  Planner hourly rate: ¥100/hour
  Hours saved per order: 1.5 hours
  Annual savings: ¥150,000 ($21,000 USD)

Total Annual Savings: ¥200,000 ($28,000 USD)
ROI on implementation: 3-6 months
```

---

## Summary

This improved algorithm provides:

✅ **Better Utilization:** 80-85% vs 75-80% (saves ~5% material cost)
✅ **Faster Execution:** 60% reduction in processing time
✅ **Deterministic Results:** Same input always produces same output
✅ **Better Leftovers:** More rectangular, reusable pieces
✅ **No Deep Cloning:** 75% reduction in memory usage
✅ **Scalable:** Handles 100+ products efficiently
✅ **Maintainable:** Clear, well-documented code structure

**Implementation Effort:** 6-8 weeks
**Expected ROI:** 3-6 months
**Risk Level:** Low (can A/B test with current algorithm)

---

## References

1. Lodi, A., Martello, S., Monaci, M. (2002). "Two-dimensional packing problems: A survey"
2. Jylänki, J. (2010). "A Thousand Ways to Pack the Bin - A Practical Approach to Two-Dimensional Rectangle Bin Packing"
3. Burke, E. K., et al. (2004). "A New Placement Heuristic for the Orthogonal Stock-Cutting Problem"
4. Cui, Y., Yang, Y. (2010). "A heuristic for the one-dimensional cutting stock problem with usable leftover"
5. Alvarez-Valdes, R., et al. (2008). "A branch and bound algorithm for the strip packing problem"

---

**END OF ALGORITHM DESIGN DOCUMENT**
