# Experiments Directory

This directory contains all test scripts and experimental optimization attempts for the tessellate cutting stock problem.

## Optimization Scripts (10-board search)

### Quick Tests
- **test_ultra_quick.py** - 5-minute quick test of ultra-aggressive packer
- **find_valid_solutions.py** - 30 trials to measure success rate
- **test_deep_search.py** - Deep search test

### Optimization Attempts
- **optimized_search_best_params.py** - ⭐ RECOMMENDED: Best parameters (20k rotated trials)
- **ultra_aggressive_search.py** - Maximum exploration (1M patterns, 100 trials)
- **optimize_aggressive.py** - Aggressive parameters (100k patterns, 100 trials)
- **force_10_boards.py** - Two-stage MIP forcing exactly 10 boards

### Analysis & Debugging
- **analyze_feasibility.py** - Pattern utilization distribution analysis
- **diagnose_overproduction.py** - Debug tool for overproduction issues
- **debug_mip_formulation.py** - Debug MIP solver behavior
- **test_highs_integrality.py** - Verify HiGHS integer constraints
- **generate_ultra_high_util_patterns.py** - Search for 95%+ utilization patterns

## Algorithm Tests

### Column Generation Tests
- **test_column_gen.py** - Basic column generation test
- **test_improved_colgen.py** - Improved version test
- **test_manual1.py** - Test baseline on manual1.xlsx
- **test_manual1_final.py** - Final test on manual1.xlsx
- **test_rotated.py** - Test rotated pattern generation
- **test_final_push.py** - Final push test

### Aggregation Tests
- **test_aggregation.py** - Basic aggregation test
- **test_aggregation_detailed.py** - Detailed aggregation test
- **test_aggregation_force_multiple.py** - Force multiple aggregation
- **test_aggregation_unit.py** - Unit tests for aggregation

### Display & Visualization Tests
- **test_display.py** - Display functionality test
- **test_svg_display.py** - SVG display test
- **test_svg_fullwidth.py** - SVG full-width display
- **test_parts_display.py** - Parts display test
- **test_text_wrapping.py** - Text wrapping test
- **test_color_consistency.py** - Color consistency test

### General Tests
- **test_generated_data.py** - Test generated data
- **test_kerf_verification.py** - Verify kerf handling
- **test_offsets.py** - Test offset calculations
- **test_template_solve.py** - Template solving test
- **test_user_scenario.py** - User scenario test

## Usage

### To run the optimized search (recommended):
```bash
cd experiments
python optimized_search_best_params.py
```

### To run a quick test:
```bash
cd experiments
python test_ultra_quick.py
```

### To analyze feasibility:
```bash
cd experiments
python analyze_feasibility.py
```

## Results Summary

- **Best achieved:** 11 boards @ 85.81% utilization
- **Target:** 10 boards @ >90% utilization (requires 94.39% avg)
- **Maximum pattern utilization:** 90.52%
- **Conclusion:** 10 boards likely infeasible with guillotine constraints

See `../FEASIBILITY_ANALYSIS.md` for detailed analysis.
