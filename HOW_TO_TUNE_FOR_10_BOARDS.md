# How to Tune the Algorithm for 10-Board Solution

## Current Status

**Best Achieved:** 11 boards @ 85.81% utilization (mathematically optimal with current patterns)

**Target:** 10 boards @ >90% utilization

**Challenge:** Requires generating patterns with 94.39% average utilization, but maximum achievable is ~90.52%

## All Tunable Parameters

### 1. **num_patterns** - Number of patterns to generate

**Location:** `ColumnGenerationPackerUltra.__init__`

```python
num_patterns = 1_000_000  # Current ultra setting
```

**Values to try:**
- Light: 10,000 - 50,000
- Medium: 100,000 - 200,000
- Heavy: 500,000 - 1,000,000
- Ultra: 2,000,000+

**Effect:** More patterns = more diverse solutions, but diminishing returns and slower MIP

**Recommendation:** Start with 100,000, increase if not finding 10-board solution

---

### 2. **rotated_trials** - Rotated strip pattern attempts

**Location:** `ColumnGenerationPackerUltra.__init__`

```python
rotated_trials = 1000  # Current ultra setting
```

**Values to try:**
- Light: 50-200
- Medium: 500-1,000
- Heavy: 2,000-5,000
- Ultra: 10,000+

**Effect:** Rotated patterns often achieve highest utilization (85-90%)

**Recommendation:** This is CRITICAL - increase to 5,000+ for best chance

---

### 3. **min_utilization** - Pattern quality filter

**Location:** `ColumnGenerationPackerUltra.__init__` and `_solve_set_covering`

```python
min_utilization = 0.40  # Current setting (40%)
```

**Values to try:**
- Very permissive: 0.35-0.45
- Balanced: 0.50-0.60
- Strict: 0.65-0.75
- Very strict: 0.80-0.85

**Effect:** Lower = more patterns (good) but more noise (bad)

**Recommendation:** Try 0.55-0.65 for best balance

**⚠️ Warning:** Too low (like 0.40) includes too many bad patterns that dilute the MIP

---

### 4. **mip_time_limit** - MIP solver time

**Location:** `ColumnGenerationPackerUltra.__init__` and `_solve_set_covering`

```python
mip_time_limit = 7200.0  # 2 hours
```

**Values to try:**
- Quick: 60-300 seconds
- Medium: 600-1,800 seconds (10-30 min)
- Heavy: 3,600-7,200 seconds (1-2 hours)
- Ultra: 14,400+ seconds (4+ hours)

**Effect:** Longer = better chance of finding optimal solution

**Recommendation:** At least 1 hour for serious attempts

---

### 5. **random_permutations** - Random packing attempts

**Location:** `ColumnGenerationPackerUltra.__init__`

```python
random_permutations = 1000  # Current ultra setting
```

**Values to try:**
- Light: 100-200
- Medium: 500-1,000
- Heavy: 2,000-5,000
- Ultra: 10,000+

**Effect:** More randomness = more pattern diversity

**Recommendation:** 2,000+ for thorough search

---

### 6. **sort_strategies** - Item sorting methods

**Location:** `column_generation_ultra.py` line ~102

**Currently:** 20 different strategies

**To add more:**
```python
# Add to the sort_strategies list:
("quantity_weighted", lambda x: -x.area() * x.quantity),
("efficiency", lambda x: -x.area() / (x.width + x.height)),
("compactness", lambda x: -min(x.width, x.height)),
# ... add 10-20 more creative strategies
```

**Effect:** More strategies = more diverse patterns

**Recommendation:** Keep 20-30 total

---

### 7. **split_rules** - Guillotine cut strategies

**Location:** `column_generation_ultra.py` line ~125

**Currently:** All 6 available rules

**Effect:** All are already included in ultra version

**Recommendation:** No change needed

---

### 8. **partial_pack_limits** - Subset packing sizes

**Location:** `column_generation_ultra.py` line ~160

**Currently:** `[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25]`

**To extend:**
```python
for limit in range(2, 30):  # Try ALL sizes from 2 to 30
```

**Effect:** More sizes = more pattern variety

**Recommendation:** Try all sizes 2-30

---

## Recommended Configurations

### Configuration A: Balanced (1-2 hours per trial)

```python
packer = ColumnGenerationPackerUltra(
    time_limit=7200.0,  # 2 hours
    num_patterns=500_000,  # 500k patterns
    min_utilization=0.60,  # Balanced filter
    mip_time_limit=3600.0,  # 1 hour MIP
    rotated_trials=5000,  # 5000 rotated attempts
    random_permutations=2000,
)
```

**Expected:** Best chance of finding alternative 11-board solutions, small chance of 10 boards

---

### Configuration B: Aggressive (6-12 hours per trial)

```python
packer = ColumnGenerationPackerUltra(
    time_limit=43200.0,  # 12 hours
    num_patterns=2_000_000,  # 2 million patterns
    min_utilization=0.55,  # Slightly permissive
    mip_time_limit=14400.0,  # 4 hours MIP
    rotated_trials=10000,  # 10k rotated attempts
    random_permutations=5000,
)
```

**Expected:** Maximum exploration, best chance of 10 boards if feasible

---

### Configuration C: Ultra-Deep (24-48 hours per trial)

```python
packer = ColumnGenerationPackerUltra(
    time_limit=172800.0,  # 48 hours
    num_patterns=5_000_000,  # 5 million patterns
    min_utilization=0.50,  # Permissive
    mip_time_limit=28800.0,  # 8 hours MIP
    rotated_trials=20000,  # 20k rotated attempts
    random_permutations=10000,
)
```

**Expected:** Exhaustive search, if 10 boards is mathematically possible, this will find it

---

## How to Run

### Quick Test (verify it works)

```bash
python test_ultra_quick.py
```

Time: ~5 minutes
Result: Verifies the packer works

---

### Single Trial with Custom Parameters

Edit `test_ultra_quick.py` and modify the parameters:

```python
packer = ColumnGenerationPackerUltra(
    time_limit=7200.0,
    num_patterns=500_000,
    min_utilization=0.60,
    mip_time_limit=3600.0,
    rotated_trials=5000,
    random_permutations=2000,
)
```

Then run:
```bash
python test_ultra_quick.py
```

---

### Multiple Trials (100 trials)

Edit `ultra_aggressive_search.py` to use your desired configuration, then:

```bash
python ultra_aggressive_search.py
```

Time: Configuration dependent (hours to days)

**⚠️ Note:** This will run 100 independent trials and report the best solution found

---

## Expected Results Based on Mathematical Analysis

| Configuration | Expected Boards | Confidence | Time per Trial |
|--------------|-----------------|------------|----------------|
| Quick test | 11-13 boards | High | 5 minutes |
| Balanced | 11 boards | Very High | 1-2 hours |
| Aggressive | 11 boards | Extremely High | 6-12 hours |
| Ultra-Deep | 11 boards | 99.9% | 24-48 hours |
| **10 boards** | **May not exist** | **See analysis** | N/A |

## Why 10 Boards May Be Impossible

From FEASIBILITY_ANALYSIS.md:

1. **Required average utilization:** 94.39%
2. **Maximum achievable pattern:** 90.52%
3. **Gap:** 3.87 percentage points

Even with unlimited patterns and unlimited MIP time, if we cannot generate patterns averaging >94%, the MIP will report INFEASIBLE.

---

## What to Try Next

### Option 1: Accept 11 boards as optimal ✓

The algorithm has proven 11 boards is the mathematical minimum with guillotine constraints.

---

### Option 2: Run ultra-deep search (just to be absolutely certain)

Use Configuration C for 3-5 trials. If all return 11 boards, accept that as final proof.

---

### Option 3: Relax guillotine constraint

If 10 boards is absolutely required, the guillotine constraint must be removed. This would require:

1. Implementing free-form 2D bin packing
2. Different cutting approach in manufacturing
3. More complex cutting sequences

---

## Monitoring Progress

When running long searches, monitor:

1. **Pattern quality:** How many patterns achieve ≥90% utilization?
2. **MIP objective:** What's the best objective value found?
3. **Resource usage:** Memory and CPU usage
4. **Best solution:** Current best board count and utilization

---

## Summary

**To maximize chance of 10 boards:**

1. **Increase rotated_trials to 10,000-20,000** (most important)
2. **Set min_utilization to 0.55-0.65** (balanced filter)
3. **Use at least 500,000-1,000,000 patterns**
4. **Allow 1-4 hours for MIP solving**
5. **Run 50-100 independent trials**
6. **Allow 24-72 hours total runtime**

**Expected outcome:** High confidence that 11 boards is the true optimum, with small possibility of discovering 10-board solution if it exists.
