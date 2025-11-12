# Parameter Tuning Guide for Column Generation Algorithm

## Overview

The algorithm has multiple parameters that control the depth, breadth, and duration of the search. This guide explains each parameter and how to tune it for maximum exploration.

## Key Parameters in column_generation.py

### 1. Pattern Generation Depth

**Number of Patterns (`num_patterns` parameter)**
```python
# Current: 10,000 patterns
# Location: ColumnGenerationPacker.__init__()
self.num_patterns = num_patterns
```

**Impact:**
- Higher = more diverse cutting patterns explored
- Diminishing returns after ~100,000 patterns
- Memory usage increases linearly

**Recommendations:**
- Light search: 5,000 - 10,000
- Medium search: 50,000 - 100,000
- Heavy search: 200,000 - 500,000
- Ultra search: 1,000,000+

---

### 2. Split Rules (Guillotine Cut Strategies)

**Number of Split Rules**
```python
# Current: 6 rules in _generate_patterns()
# Location: line ~200 in column_generation.py

split_rules = [
    'short_leftover_axis',
    'long_leftover_axis',
    'short_axis',
    'long_axis',
    'min_area_split',
    'max_area_split'
]
```

**Additional Rules to Try:**
- `'horizontal_split'` - always cut horizontally
- `'vertical_split'` - always cut vertically
- `'golden_ratio'` - split at golden ratio
- `'adaptive'` - choose based on items

**Impact:** More rules = more diverse patterns, but slower generation

---

### 3. Sort Strategies

**Number of Item Sorting Strategies**
```python
# Current: 9 strategies in _generate_patterns()
# Location: line ~190

sort_strategies = [
    lambda x: -x.area(),
    lambda x: -x.width,
    lambda x: -x.height,
    # ... 6 more
]
```

**Additional Strategies to Add:**
```python
# Aspect ratio based
lambda x: -abs(x.width - x.height),  # Most square first
lambda x: -max(x.width, x.height) / min(x.width, x.height),  # Highest aspect ratio

# Perimeter based
lambda x: -2*(x.width + x.height),  # Largest perimeter

# Quantity weighted
lambda x: -x.area() * x.quantity,  # Area × quantity

# Randomized
lambda x: random.random(),  # Pure random order
```

**Impact:** More variety in packing order = different final patterns

---

### 4. Rotated Strip Packing

**Number of Rotated Patterns**
```python
# Current: generates ~1,500 rotated patterns per trial
# Location: _generate_rotated_strip_patterns()

# Control via number of trials:
num_trials_per_sort = 50  # Current value
```

**Tune:**
```python
# Light: 10 trials
# Medium: 50 trials
# Heavy: 200 trials
# Ultra: 1000 trials
```

**Impact:** Rotated patterns often achieve highest utilization (85-90%)

---

### 5. MIP Solver Parameters

**Time Limit**
```python
# Current: max(300.0, remaining_time * 0.8) seconds
# Location: _solve_set_covering(), line ~520

h.setOptionValue("time_limit", mip_time)
```

**Tune:**
```python
# Quick: 60 seconds
# Medium: 300 seconds (5 min)
# Heavy: 1800 seconds (30 min)
# Ultra: 7200 seconds (2 hours)
```

**MIP Gap Tolerance**
```python
# Current: 0.0 (exact solution)
h.setOptionValue("mip_rel_gap", 0.0)
```

**Tune for faster results:**
```python
# Exact: 0.0
# Near-optimal: 0.01 (1% gap)
# Good: 0.05 (5% gap)
```

---

### 6. Pattern Quality Filters

**Minimum Utilization Filter**
```python
# Current: 50% in latest version
# Location: _generate_patterns(), line ~260

min_util = 0.50  # Keep patterns >= 50% utilization
good_patterns = [p for p in all_patterns if p.utilization >= min_util]
```

**Tune:**
```python
# Very permissive: 0.40 (40%)
# Permissive: 0.50 (50%)
# Balanced: 0.60 (60%)
# Strict: 0.70 (70%)
# Very strict: 0.80 (80%)
```

**Trade-off:** Lower = more patterns but more computation in MIP

---

### 7. Multi-Trial Search

**Number of Independent Trials**
```python
# External scripts like find_valid_solutions.py
# Each trial uses different random seed

num_trials = 30  # Current in find_valid_solutions.py
```

**Tune:**
```python
# Quick test: 5-10 trials
# Medium: 30-50 trials
# Heavy: 100-200 trials
# Ultra: 1000+ trials (parallel execution recommended)
```

---

## Ultra-Aggressive Configuration

For maximum exploration (doesn't care about time/resources):

```python
# In ColumnGenerationPacker.__init__()
num_patterns = 1_000_000  # 1 million patterns

# In _generate_patterns()
min_util = 0.40  # Very permissive filter
num_trials_per_sort = 1000  # Massive rotated pattern generation

# Additional split rules
split_rules = [
    'short_leftover_axis',
    'long_leftover_axis',
    'short_axis',
    'long_axis',
    'min_area_split',
    'max_area_split',
    'horizontal_split',
    'vertical_split',
]

# Additional sort strategies (add 5-10 more)
sort_strategies = [... 15-20 different strategies ...]

# In _solve_set_covering()
h.setOptionValue("time_limit", 7200.0)  # 2 hours MIP time
h.setOptionValue("mip_rel_gap", 0.0)  # Exact solution

# External trial script
num_trials = 1000  # 1000 independent trials
```

**Estimated Runtime:** 24-72 hours on single machine
**Recommended:** Run on multiple cores/machines in parallel

---

## Advanced Techniques Not Yet Implemented

### 1. Branch-and-Price (Full Implementation)

Current implementation generates patterns once, then solves.
True branch-and-price iteratively generates patterns based on dual values.

**Potential improvement:** 5-10% better solutions

### 2. Local Search / Metaheuristics

After MIP solution, try local improvements:
- Swap items between boards
- Repack single boards with different heuristics
- Simulated annealing for board assignments

### 3. Pattern Combination Search

Try finding sets of patterns that work well together:
- Complementary patterns (different item mixes)
- Multi-board pattern sequences

### 4. Machine Learning Pattern Ranking

Train ML model to predict which patterns will be selected:
- Generate millions of patterns
- Use ML to filter to most promising
- Only solve MIP on top candidates

---

## Recommended Tuning Strategy

### Phase 1: Quick Test (5 minutes)
- num_patterns: 10,000
- min_util: 0.60
- MIP time: 60s
- Trials: 5

**Goal:** Verify algorithm works

### Phase 2: Medium Search (1 hour)
- num_patterns: 100,000
- min_util: 0.50
- MIP time: 300s
- Trials: 30

**Goal:** Find good solutions

### Phase 3: Heavy Search (6 hours)
- num_patterns: 500,000
- min_util: 0.45
- MIP time: 1800s
- Trials: 100

**Goal:** Find best possible solutions

### Phase 4: Ultra Search (24-72 hours)
- num_patterns: 1,000,000
- min_util: 0.40
- MIP time: 7200s
- Trials: 1000

**Goal:** Exhaustive search for absolute optimum

---

## Monitoring Progress

Track these metrics during search:

1. **Pattern quality distribution**
   - How many patterns ≥85%, ≥90%, ≥95%?

2. **MIP solver behavior**
   - Is it finding integer solutions quickly?
   - What's the objective value trend?

3. **Best solution so far**
   - Number of boards
   - Average utilization
   - Worst board utilization

4. **Resource usage**
   - Memory consumption
   - CPU time per trial
   - Total time elapsed

---

## Expected Results

Based on mathematical analysis:

| Configuration | Expected Result | Confidence |
|--------------|-----------------|------------|
| Light search | 11-12 boards | High |
| Medium search | 11 boards @ 85.81% | Very High |
| Heavy search | 11 boards @ 85.81% | Very High |
| Ultra search | 11 boards @ 85.81% | Extremely High |

**Note:** 10 boards may still be infeasible even with ultra-aggressive search, due to fundamental guillotine constraint limitations.

However, ultra-aggressive search might find:
- Better utilization distribution across 11 boards
- Alternative 11-board solutions with different trade-offs
- Proof of infeasibility with higher certainty
