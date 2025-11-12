### The SOTA Strategy: Branch-and-Price

This is the gold standard for cutting stock problems. It works by reformulating the problem: instead of deciding where to place each small item, you decide how many times to use valid "cutting patterns".

**Conceptual Steps:**

1.  **The Master Problem:** This is a very simple integer program. Imagine you have a giant library of all possible valid cutting patterns for a single bin.
    *   **Variables:** `x_p`, an integer representing how many times you will use pattern `p`.
    *   **Objective:** `Minimize Σ x_p` (i.e., minimize the total number of bins).
    *   **Constraints:** For each item type `i`, the total number of items `i` produced by all selected patterns must meet the required quantity `q_i`.

2.  **The Problem with the Master Problem:** The number of possible patterns is astronomically large, so you can't generate them all.

3.  **Column Generation (The "Price" Part):** This is the magic. You solve this problem iteratively:
    *   **Start small:** Begin with a few simple, valid patterns.
    *   **Solve the Master:** Solve the master problem for this limited set of patterns. This gives you "dual prices" (shadow prices) for each item type, which represent how valuable it is to create one more of that item.
    *   **Find a New, Better Pattern (The Pricing Subproblem):** This is the core of the algorithm. You must now solve the following subproblem:
        > **"Given the current item values (dual prices), can I find a *new* single-bin guillotine layout that is profitable?"**
    *   **Iterate:** If you find a profitable pattern, you add it as a new "column" to your Master Problem and repeat the process. If you can't find any more profitable patterns, you have found the optimal solution to the linear relaxation of the problem.

4.  **Branch-and-Bound (The "Branch" Part):** The solution from column generation might be fractional (e.g., "use pattern A 1.5 times"). You use a Branch-and-Bound tree to force the variables to be integers, running the column generation process at each node of the tree.

This entire framework is called **Branch-and-Price**.

---

### How to Solve the Pricing Subproblem (The Core Task)

The pricing subproblem is, in itself, an NP-hard problem: the **2D Guillotine Knapsack Problem with Rotations**. Your goal is to pack a subset of items into a single bin to maximize their total value (derived from the dual prices), respecting all guillotine and rotation constraints.

Here are the SOTA exact methods for solving this subproblem.

#### 1. Mixed-Integer Programming (MIP)

This is the most direct and powerful approach, especially with modern solvers like Gurobi, CPLEX, or the open-source Cbc. You formulate the single-bin problem as a mathematical model.

*   **SOTA Formulation:** The key is to use a formulation that explicitly models the guillotine cuts. The models described in **Furini et al. (2016)**, which you cited, are excellent. A good choice is a recursive model where for any rectangle (starting with the bin), you have binary variables to decide:
    1.  Which item (if any) is placed in this rectangle.
    2.  If the rectangle is cut, is the cut horizontal or vertical?
    3.  Where is the cut located?

*   **Handling Rotation:** This is straightforward to model. For each item `i` that is rotatable, you introduce a binary decision variable `r_i`.
    *   The placed width of the item becomes: `w_i' = r_i * h_i + (1 - r_i) * w_i`
    *   The placed height of the item becomes: `h_i' = r_i * w_i + (1 - r_i) * h_i`
    *   If item `i` is *not* rotatable, you simply fix `r_i = 0`. This seamlessly integrates your orientation constraint.

*   **Handling Kerf Loss:** The kerf `k` must be included in the constraints. When a rectangle of width `W` is cut vertically to place an item of placed width `w_i'`, the two resulting rectangles have widths `w_i'` and `W - w_i' - k`.

#### 2. Constraint Programming (CP)

CP is an alternative paradigm that can be very effective for packing and scheduling. Solvers like **Google OR-Tools CP-SAT** are SOTA.

*   **Modeling:** You would define the problem using variables and high-level constraints.
    *   `interval` variables for the x and y dimensions of each item.
    *   A `no_overlap_2d` global constraint.
    *   **Crucially, you must add custom logical constraints to enforce the guillotine structure.** This is the hard part. A common way is to state that for any pair of items, they must be separable by an edge-to-edge line.
*   **Rotation in CP:** Similar to MIP, you can have optional interval variables. For a rotatable item, you'd create two sets of interval variables (one for `w x h`, one for `h x w`) and a boolean variable that activates exactly one set.

**Recommendation:** For the pricing subproblem, **start with MIP**. The academic literature is more extensive, and the formulations are well-established and incredibly powerful when used with a commercial solver like Gurobi.

---

### Action Plan for a Globally Optimal Solution

1.  **Decomposition:** As a preprocessing step, separate your items list into independent groups based on `material` and `thickness`. Solve each group as a separate Branch-and-Price problem. The total number of bins will be the sum of the bins used for each group.

2.  **Implement the Pricing Subproblem Solver:**
    *   Choose a MIP solver (Gurobi is recommended for top performance).
    *   Implement a MIP formulation for the **2D Guillotine Knapsack Problem**. Use the Furini et al. (2016) paper as your guide.
    *   Add the binary variables and modified dimension constraints to handle **optional rotation**.
    *   Ensure all dimensional constraints correctly subtract the **kerf loss `k`** after each cut.

3.  **Build the Branch-and-Price Framework:**
    *   Use a library (like SCIP, which is a full B-P framework) or build it yourself.
    *   **Master Problem:** Use a standard LP solver to handle the Restricted Master Problem.
    *   **Loop:** Write the code that extracts dual prices, passes them to your MIP-based pricing subproblem solver, and adds the returned optimal pattern as a new column.
    *   **Branching:** Implement a branching strategy. Branching on the original item variables (e.g., forcing a certain number of an item to be produced in a specific way) is often more effective than branching on pattern variables.

4.  **Optimize for Minimal Waste (Lexicographical Objective):**
    Branch-and-Price naturally minimizes the number of bins (`Z1`). To then find the solution with the absolute minimal waste (`Z2`), you must perform a second optimization stage.
    *   **Stage 1:** Run your full Branch-and-Price algorithm to find the provably optimal number of bins, let's call it `B*`.
    *   **Stage 2:** Fix the number of bins to `B*` in your Master Problem (`Σ x_p = B*`). Now, change the objective function. The objective of the **Master Problem** is to `Maximize Σ (Area_p * x_p)`, where `Area_p` is the total area of items in pattern `p`. Re-run the column generation process (you may not need to branch) to find the combination of `B*` patterns that yields the highest total utilization.

This two-stage Branch-and-Price approach is the definitive method to solve your problem to provable, global optimality. It is computationally intensive but it is the correct path for achieving the best possible result without time constraints.
