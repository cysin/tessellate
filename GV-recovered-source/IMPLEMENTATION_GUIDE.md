# Quick Implementation Guide
## Improved Cutting Optimization Algorithm

**Target:** Replace ViewServiceR2 with better algorithm
**Timeline:** 6-8 weeks
**Expected Results:** 80-85% utilization (vs current 75-80%), 60% faster execution

---

## Phase 1: Core Implementation (Week 1-2)

### Step 1.1: Create Immutable Data Structures

Create new file: `src/com/gv/algorithm/PackingState.java`

```java
package com.gv.algorithm;

import com.gv.model.Product;
import java.util.*;

/**
 * Immutable packing state - eliminates need for deep cloning
 * Uses structural sharing for performance
 */
public class PackingState {
    public final double sheetWidth;
    public final double sheetHeight;
    public final String color;
    public final double thickness;
    public final double totalArea;
    public final double usedArea;

    public final List<FreeRectangle> freeRectangles;
    public final List<PlacedProduct> placedProducts;

    // Constructor for initial state
    public PackingState(double width, double height, String color, double thickness) {
        this.sheetWidth = width;
        this.sheetHeight = height;
        this.color = color;
        this.thickness = thickness;
        this.totalArea = width * height;
        this.usedArea = 0;

        this.freeRectangles = Collections.singletonList(
            new FreeRectangle(0, 0, width, height, 0)
        );
        this.placedProducts = Collections.emptyList();
    }

    // Private constructor for creating new states
    private PackingState(double width, double height, String color, double thickness,
                        double usedArea, List<FreeRectangle> freeRects,
                        List<PlacedProduct> placed) {
        this.sheetWidth = width;
        this.sheetHeight = height;
        this.color = color;
        this.thickness = thickness;
        this.totalArea = width * height;
        this.usedArea = usedArea;
        this.freeRectangles = Collections.unmodifiableList(freeRects);
        this.placedProducts = Collections.unmodifiableList(placed);
    }

    /**
     * Returns NEW state with product placed (no mutation!)
     * This is the key optimization - no deep cloning needed
     */
    public PackingState placeProduct(Product product, FreeRectangle usedRect,
                                    boolean rotated, double sawKerf) {
        double pWidth = rotated ? product.getP_height() : product.getP_width();
        double pHeight = rotated ? product.getP_width() : product.getP_height();

        // Create new placed product
        PlacedProduct placed = new PlacedProduct(
            product, usedRect.x, usedRect.y, pWidth, pHeight, rotated
        );

        // New placed list (copy existing + add new)
        List<PlacedProduct> newPlaced = new ArrayList<>(this.placedProducts);
        newPlaced.add(placed);

        // Update free rectangles with guillotine splits
        List<FreeRectangle> newFree = updateFreeRectangles(
            this.freeRectangles, usedRect, pWidth, pHeight, sawKerf
        );

        // Calculate new used area
        double newUsedArea = this.usedArea + (pWidth * pHeight);

        // Return new immutable state (structural sharing!)
        return new PackingState(
            this.sheetWidth, this.sheetHeight, this.color, this.thickness,
            newUsedArea, newFree, newPlaced
        );
    }

    public double getUtilization() {
        return usedArea / totalArea;
    }

    /**
     * Guillotine split: divide used rectangle into new free rectangles
     */
    private List<FreeRectangle> updateFreeRectangles(
        List<FreeRectangle> current, FreeRectangle used,
        double productWidth, double productHeight, double sawKerf
    ) {
        List<FreeRectangle> result = new ArrayList<>();

        for (FreeRectangle rect : current) {
            if (rect.equals(used)) {
                // This rectangle is being used - split it

                // Right remainder
                double rightWidth = used.width - productWidth - sawKerf;
                if (rightWidth > 10) {  // Minimum useful size
                    result.add(new FreeRectangle(
                        used.x + productWidth + sawKerf,
                        used.y,
                        rightWidth,
                        used.height,
                        used.level + 1
                    ));
                }

                // Bottom remainder
                double bottomHeight = used.height - productHeight - sawKerf;
                if (bottomHeight > 10) {
                    result.add(new FreeRectangle(
                        used.x,
                        used.y + productHeight + sawKerf,
                        productWidth,  // Guillotine constraint
                        bottomHeight,
                        used.level + 1
                    ));
                }

                // Corner remainder (if both have space)
                if (rightWidth > 10 && bottomHeight > 10) {
                    result.add(new FreeRectangle(
                        used.x + productWidth + sawKerf,
                        used.y + productHeight + sawKerf,
                        rightWidth,
                        bottomHeight,
                        used.level + 1
                    ));
                }
            } else {
                // Keep unchanged rectangles
                result.add(rect);
            }
        }

        // Remove rectangles fully contained in others (optimization)
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
```

### Step 1.2: Create Supporting Classes

Create `src/com/gv/algorithm/FreeRectangle.java`:

```java
package com.gv.algorithm;

import com.gv.model.Product;

public class FreeRectangle {
    public final double x;
    public final double y;
    public final double width;
    public final double height;
    public final int level;  // Nesting depth

    public FreeRectangle(double x, double y, double width, double height, int level) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.level = level;
    }

    public double getArea() {
        return width * height;
    }

    public boolean canFit(Product product, double sawKerf, boolean rotated) {
        double reqWidth = rotated ? product.getP_height() : product.getP_width();
        double reqHeight = rotated ? product.getP_width() : product.getP_height();

        return (width >= reqWidth + sawKerf) && (height >= reqHeight + sawKerf);
    }

    public boolean contains(FreeRectangle other) {
        return this.x <= other.x &&
               this.y <= other.y &&
               this.x + this.width >= other.x + other.width &&
               this.y + this.height >= other.y + other.height;
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof FreeRectangle)) return false;
        FreeRectangle other = (FreeRectangle) obj;
        return Math.abs(this.x - other.x) < 0.01 &&
               Math.abs(this.y - other.y) < 0.01 &&
               Math.abs(this.width - other.width) < 0.01 &&
               Math.abs(this.height - other.height) < 0.01;
    }
}
```

Create `src/com/gv/algorithm/PlacedProduct.java`:

```java
package com.gv.algorithm;

import com.gv.model.Product;

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
```

---

## Phase 2: Heuristics Implementation (Week 3-4)

### Step 2.1: Placement Scoring

Create `src/com/gv/algorithm/PlacementScorer.java`:

```java
package com.gv.algorithm;

import com.gv.model.Product;
import java.util.List;

public class PlacementScorer {

    // Heuristic weights (tunable)
    private double weightAreaFit = 0.25;
    private double weightShortSide = 0.15;
    private double weightLongSide = 0.15;
    private double weightEdgeAlign = 0.15;
    private double weightLeftoverQuality = 0.20;
    private double weightFutureFit = 0.10;

    public double scorePlacement(PackingState state, FreeRectangle rect,
                                Product product, boolean rotated, double sawKerf,
                                List<Product> remainingProducts) {

        double pWidth = rotated ? product.getP_height() : product.getP_width();
        double pHeight = rotated ? product.getP_width() : product.getP_height();

        // Heuristic 1: Best Area Fit
        double wastedArea = (rect.width * rect.height) - (pWidth * pHeight);
        double areaFitScore = 1.0 / (1.0 + wastedArea / 10000.0);

        // Heuristic 2: Best Short Side Fit
        double leftoverH = rect.width - pWidth - sawKerf;
        double leftoverV = rect.height - pHeight - sawKerf;
        double shortSideFit = Math.min(leftoverH, leftoverV);
        double shortSideScore = shortSideFit < 0 ? 1.0 :
                               1.0 / (1.0 + shortSideFit / 100.0);

        // Heuristic 3: Best Long Side Fit
        double longSideFit = Math.max(leftoverH, leftoverV);
        double longSideScore = longSideFit < 0 ? 1.0 :
                              1.0 / (1.0 + longSideFit / 100.0);

        // Heuristic 4: Edge Alignment
        double edgeScore = 0.0;
        if (Math.abs(rect.x) < 1 ||
            Math.abs(rect.x + pWidth - state.sheetWidth) < 1) {
            edgeScore += 0.5;
        }
        if (Math.abs(rect.y) < 1 ||
            Math.abs(rect.y + pHeight - state.sheetHeight) < 1) {
            edgeScore += 0.5;
        }

        // Heuristic 5: Leftover Quality
        double leftoverQuality = calculateLeftoverQuality(
            rect, pWidth, pHeight, sawKerf
        );

        // Heuristic 6: Future Fit (simplified)
        double futureFit = estimateFutureFit(
            state, rect, pWidth, pHeight, sawKerf, remainingProducts
        );

        // Weighted sum
        double totalScore =
            weightAreaFit * areaFitScore +
            weightShortSide * shortSideScore +
            weightLongSide * longSideScore +
            weightEdgeAlign * edgeScore +
            weightLeftoverQuality * leftoverQuality +
            weightFutureFit * futureFit;

        return totalScore;
    }

    private double calculateLeftoverQuality(FreeRectangle rect,
                                           double productWidth,
                                           double productHeight,
                                           double sawKerf) {
        double rightSpace = rect.width - productWidth - sawKerf;
        double bottomSpace = rect.height - productHeight - sawKerf;

        // Perfect fit (no leftover) = best
        if (rightSpace <= 0 && bottomSpace <= 0) {
            return 1.0;
        }

        // One dimension leftover (rectangular) = good
        if (rightSpace <= 0 || bottomSpace <= 0) {
            return 0.8;
        }

        // Both dimensions have leftover - check aspect ratio
        double aspectRatio = Math.max(rightSpace, bottomSpace) /
                            Math.min(rightSpace, bottomSpace);

        if (aspectRatio > 10) {
            return 0.6;  // Nearly rectangular
        } else {
            return 0.3;  // L-shaped (poor)
        }
    }

    private double estimateFutureFit(PackingState state, FreeRectangle rect,
                                    double productWidth, double productHeight,
                                    double sawKerf,
                                    List<Product> remainingProducts) {
        // Fast heuristic: check if enough area remains

        double usedInRect = productWidth * productHeight;
        double rectArea = rect.width * rect.height;
        double remainderArea = rectArea - usedInRect;

        double totalFreeArea = state.freeRectangles.stream()
            .mapToDouble(FreeRectangle::getArea)
            .sum();

        totalFreeArea = totalFreeArea - rectArea + remainderArea;

        double remainingProductArea = remainingProducts.stream()
            .mapToDouble(p -> p.getP_width() * p.getP_height() * p.getP_r_count())
            .sum();

        // Score based on ratio
        if (totalFreeArea >= remainingProductArea * 1.2) {
            return 1.0;  // Plenty of space
        } else if (totalFreeArea >= remainingProductArea) {
            return 0.7;  // Tight fit
        } else {
            return 0.3;  // May not fit
        }
    }
}
```

---

## Phase 3: Main Algorithm (Week 5-6)

### Step 3.1: Create Main Engine

Create `src/com/gv/algorithm/ImprovedCuttingEngine.java`:

```java
package com.gv.algorithm;

import com.gv.model.Product;
import com.gv.model.Material;
import java.util.*;
import java.util.stream.Collectors;

public class ImprovedCuttingEngine {

    private final PlacementScorer scorer;

    public ImprovedCuttingEngine() {
        this.scorer = new PlacementScorer();
    }

    /**
     * Main optimization entry point
     * Replaces ViewServiceR2.createView()
     */
    public List<Material> optimizeCutting(
        List<Product> products,
        List<Material> availableMaterials,
        double sawKerf,
        double utilizationThreshold
    ) {
        // Group products by color and thickness
        Map<String, List<Product>> groups = groupProducts(products);

        List<Material> resultMaterials = new ArrayList<>();

        // Process each group independently
        for (Map.Entry<String, List<Product>> entry : groups.entrySet()) {
            List<Product> groupProducts = entry.getValue();

            // Find matching materials
            String[] parts = entry.getKey().split("\\*");
            double thickness = Double.parseDouble(parts[0]);
            String color = parts[1];

            List<Material> matchingMaterials = availableMaterials.stream()
                .filter(m -> Math.abs(m.getM_weight() - thickness) < 0.01 &&
                            m.getM_color().equals(color))
                .collect(Collectors.toList());

            if (matchingMaterials.isEmpty()) continue;

            // Sort products for optimal packing
            List<Product> sortedProducts = sortProducts(groupProducts);

            // Pack onto sheets
            List<Material> packedSheets = packProducts(
                sortedProducts,
                matchingMaterials.get(0),  // Use first matching material
                sawKerf,
                utilizationThreshold
            );

            resultMaterials.addAll(packedSheets);
        }

        return resultMaterials;
    }

    private Map<String, List<Product>> groupProducts(List<Product> products) {
        Map<String, List<Product>> groups = new HashMap<>();

        for (Product p : products) {
            String key = p.getP_weight() + "*" + p.getP_color();
            groups.computeIfAbsent(key, k -> new ArrayList<>()).add(p);
        }

        return groups;
    }

    private List<Product> sortProducts(List<Product> products) {
        // Multi-criteria sorting
        List<Product> sorted = new ArrayList<>(products);

        sorted.sort((p1, p2) -> {
            // Priority 1: Grain direction (directional first)
            if (p1.getP_is_dir() != p2.getP_is_dir()) {
                return p2.getP_is_dir() - p1.getP_is_dir();
            }

            // Priority 2: Area (larger first)
            double area1 = p1.getP_width() * p1.getP_height();
            double area2 = p2.getP_width() * p2.getP_height();
            int areaCompare = Double.compare(area2, area1);
            if (areaCompare != 0) return areaCompare;

            // Priority 3: Aspect ratio (extreme first)
            double aspect1 = Math.abs(p1.getP_width() / p1.getP_height() - 1.0);
            double aspect2 = Math.abs(p2.getP_width() / p2.getP_height() - 1.0);
            return Double.compare(aspect2, aspect1);
        });

        return sorted;
    }

    private List<Material> packProducts(
        List<Product> products,
        Material templateMaterial,
        double sawKerf,
        double utilizationThreshold
    ) {
        List<Material> sheets = new ArrayList<>();
        List<Product> remaining = new ArrayList<>();

        // Expand products by quantity
        for (Product p : products) {
            for (int i = 0; i < p.getP_count(); i++) {
                Product copy = new Product();
                // Copy all properties from p
                copy.setP_no(p.getP_no());
                copy.setP_name(p.getP_name());
                copy.setP_width(p.getP_width());
                copy.setP_height(p.getP_height());
                copy.setP_weight(p.getP_weight());
                copy.setP_color(p.getP_color());
                copy.setP_is_dir(p.getP_is_dir());
                copy.setP_count(1);
                copy.setP_r_count(1);
                remaining.add(copy);
            }
        }

        // Pack onto sheets
        while (!remaining.isEmpty()) {
            PackingState state = new PackingState(
                templateMaterial.getM_width(),
                templateMaterial.getM_height(),
                templateMaterial.getM_color(),
                templateMaterial.getM_weight()
            );

            boolean improved = true;
            while (improved && !remaining.isEmpty()) {
                PlacementCandidate best = findBestPlacement(
                    state, remaining, sawKerf
                );

                if (best == null ||
                    (state.getUtilization() >= utilizationThreshold &&
                     !sheets.isEmpty())) {
                    improved = false;
                    break;
                }

                // Place product
                state = state.placeProduct(
                    best.product, best.rect, best.rotated, sawKerf
                );

                remaining.remove(best.product);
            }

            // Convert to Material and add to results
            if (!state.placedProducts.isEmpty()) {
                Material sheet = convertToMaterial(state, templateMaterial);
                sheets.add(sheet);
            } else {
                break;  // Can't place anything
            }
        }

        return sheets;
    }

    private PlacementCandidate findBestPlacement(
        PackingState state,
        List<Product> products,
        double sawKerf
    ) {
        List<PlacementCandidate> candidates = new ArrayList<>();

        for (Product p : products) {
            for (FreeRectangle rect : state.freeRectangles) {
                // Try original orientation
                if (rect.canFit(p, sawKerf, false)) {
                    double score = scorer.scorePlacement(
                        state, rect, p, false, sawKerf, products
                    );
                    candidates.add(new PlacementCandidate(p, rect, false, score));
                }

                // Try rotated (if allowed)
                if (p.getP_is_dir() == 0 && rect.canFit(p, sawKerf, true)) {
                    double score = scorer.scorePlacement(
                        state, rect, p, true, sawKerf, products
                    );
                    candidates.add(new PlacementCandidate(p, rect, true, score));
                }
            }
        }

        if (candidates.isEmpty()) return null;

        // Sort by score (highest first)
        candidates.sort((a, b) -> Double.compare(b.score, a.score));

        return candidates.get(0);
    }

    private Material convertToMaterial(PackingState state, Material template) {
        Material m = new Material();
        m.setM_name(template.getM_name());
        m.setM_width(state.sheetWidth);
        m.setM_height(state.sheetHeight);
        m.setM_color(state.color);
        m.setM_weight(state.thickness);
        m.setM_area_used(state.getUtilization());

        // Set placed products
        List<Product> placed = new ArrayList<>();
        for (PlacedProduct pp : state.placedProducts) {
            Product p = pp.product;
            p.setM_left(pp.x);
            p.setM_top(pp.y);
            p.setP_is_show(1);
            placed.add(p);
        }
        m.setM_products(placed);

        return m;
    }

    // Inner class for placement candidates
    private static class PlacementCandidate {
        Product product;
        FreeRectangle rect;
        boolean rotated;
        double score;

        PlacementCandidate(Product product, FreeRectangle rect,
                          boolean rotated, double score) {
            this.product = product;
            this.rect = rect;
            this.rotated = rotated;
            this.score = score;
        }
    }
}
```

---

## Phase 4: Integration (Week 7-8)

### Step 4.1: Update ViewAction

Modify `src/com/gv/action/ViewAction.java`:

```java
// Add import
import com.gv.algorithm.ImprovedCuttingEngine;

public class ViewAction extends ActionSupport {

    // Add flag to switch between algorithms
    private boolean useImprovedAlgorithm = true;

    public String createView() {
        // ... existing product parsing code ...

        if (useImprovedAlgorithm) {
            // Use new algorithm
            ImprovedCuttingEngine engine = new ImprovedCuttingEngine();
            this.materials = engine.optimizeCutting(
                m_products,
                createMaterials(),
                saw_bite,
                scale
            );
        } else {
            // Use old algorithm (for comparison)
            ViewServiceR2 service = new ViewServiceR2();
            this.materials = service.createView(
                m_products,
                createMaterials(),
                saw_bite,
                scale
            );
        }

        this.result = "success";
        return this.result;
    }
}
```

### Step 4.2: A/B Testing

Add configuration parameter to switch algorithms:

```xml
<!-- struts.xml -->
<action name="createView" class="viewAction" method="createView">
    <param name="useImprovedAlgorithm">true</param>
    <result name="success" type="json">
        <param name="root">materials</param>
    </result>
</action>
```

---

## Testing Checklist

- [ ] Unit tests for PackingState
- [ ] Unit tests for guillotine splitting
- [ ] Unit tests for heuristics
- [ ] Integration test with TEST_DATA.md scenarios
- [ ] Performance benchmark vs old algorithm
- [ ] Verify grain direction compliance
- [ ] Verify utilization improvement
- [ ] Test with 100+ products
- [ ] Memory usage profiling
- [ ] User acceptance testing

---

## Rollout Strategy

1. **Week 1-4:** Implement core algorithm
2. **Week 5:** Side-by-side testing (old vs new)
3. **Week 6:** A/B testing with real users (50/50 split)
4. **Week 7:** Analyze results, tune weights
5. **Week 8:** Full rollout if metrics improved

---

## Success Metrics

Track these metrics during rollout:

```
Utilization Rate:
  Target: ≥ 80% (current: 75-80%)
  Measure: Average across all jobs

Execution Time:
  Target: < 2s for 50 products (current: 4-5s)
  Measure: 95th percentile response time

User Satisfaction:
  Target: ≥ 4.5/5.0
  Measure: Post-job survey

Material Cost Savings:
  Target: 5% reduction
  Measure: Monthly material costs
```

---

## Fallback Plan

If new algorithm has issues:

1. Flip `useImprovedAlgorithm` flag to `false`
2. Investigate logs and error reports
3. Fix bugs in development environment
4. Re-test before re-enabling

---

## Files to Create

```
src/com/gv/algorithm/
  ├── ImprovedCuttingEngine.java       (Main engine)
  ├── PackingState.java                (Immutable state)
  ├── FreeRectangle.java               (Free space)
  ├── PlacedProduct.java               (Placed product)
  └── PlacementScorer.java             (Heuristics)

test/com/gv/algorithm/
  ├── PackingStateTest.java
  ├── PlacementScorerTest.java
  └── ImprovedCuttingEngineTest.java
```

---

## Quick Start Commands

```bash
# 1. Create algorithm package
mkdir -p src/com/gv/algorithm

# 2. Copy implementation files (create from templates above)

# 3. Compile
./build.sh

# 4. Deploy
./deploy.sh

# 5. Test
curl -X POST -d "product_no=A001&product_name=Test&..." \
  http://localhost:8089/GV/createView.action
```

---

**Questions? See IMPROVED_ALGORITHM_DESIGN.md for full details.**
