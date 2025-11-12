# 2D Packing Problem Specification (Furniture Panel Cutting)

## 1. Scope

This document specifies a practical variant of the two‑dimensional (2D) packing/cutting stock problem for furniture panel cutting. Rectangular parts must be cut from rectangular boards while observing manufacturing constraints such as kerf (saw blade width), grain orientation, and material attributes (e.g., thickness, color). The specification is implementation‑agnostic.

## 2. Entities and Parameters

- Part (demand item)
  - id: unique identifier
  - w, h: width and height (mm)
  - q: required quantity (integer ≥ 1)
  - rot: rotation permission (boolean; true allows 90° rotation)
  - attr: material attributes (e.g., thickness, color/finish)

- Board Type
  - type_id: unique identifier for a standard board size
  - W, H: width and height (mm)
  - attr: material attributes compatible with parts (e.g., thickness, color/finish)
  - cost: per‑board cost (optional, for cost‑aware objectives)

- Leftover Piece (optional input inventory)
  - lof_id: unique identifier
  - Wl, Hl: residual width and height (mm)
  - attr: material attributes
  - qty: available quantity (integer ≥ 1)

- Process Parameters
  - kerf: saw kerf width (mm, ≥ 0)
  - edge_margin: minimum clearance from board outer edge to any cut/part (mm, ≥ 0)
  - min_keep: minimum dimension threshold to retain a leftover piece (mm, ≥ 0); pieces with width < min_keep or height < min_keep are discarded
  - guillotine: whether patterns must be obtainable via recursive full‑length orthogonal cuts (boolean)

## 3. Decision Variables (conceptual)

- Board selection
  - Choose a multiset of board instances from available board types and/or leftover pieces to use.

- Placement
  - For each placed part copy, choose: board instance, position (x, y), orientation (0° or 90° if rot = true).

- Cutting plan (if guillotine = true)
  - Choose an ordered sequence/tree of orthogonal full‑length cuts that yields the placed rectangles from the board.

- Leftover retention
  - For each unused rectangular region, decide whether it is retained as a leftover (must satisfy min_keep) and record its dimensions and attributes.

## 4. Objectives

One or more of the following objectives may be used (single objective or multi‑objective):

- Minimize number of boards used.
- Minimize total cost of boards used.
- Minimize total waste area = sum(board areas) − sum(placed part areas) − (optional) kerf loss modeling.
- Minimize cut complexity (e.g., total cut length, number of cuts).
- Maximize leftover quality (e.g., retained area weighted by usefulness).

When multiple objectives apply, use a defined priority order (lexicographic) or weighting scheme.

## 5. Constraints

5.1 Demand Satisfaction
- For each part id, the total number of placed copies across all boards must be ≥ its required quantity q (typically exactly q unless overproduction is allowed).

5.2 Attribute Compatibility
- A part can be assigned only to boards (or leftovers) whose attr exactly match the part’s attr (e.g., same thickness and finish/color). Mixing incompatible attributes is prohibited.

5.3 Containment
- Each placed part rectangle must lie entirely within the usable area of its board instance, respecting edge_margin on all sides.

5.4 Non‑Overlap
- Placed part rectangles must be pairwise disjoint with a clearance that ensures feasible cutting under the kerf model (see 5.5).

5.5 Kerf and Clearances
- Adjacent parts must be separated by at least kerf in the cutting plan. Two modeling options are common:
  - Clearance model: enforce a minimum spacing ≥ kerf between adjacent rectangles and from parts to cut lines/edge.
  - Cut‑aware model: explicitly model cut lines and ensure every cut removes kerf width; placed rectangles are separated by cut lines rather than raw clearance.

5.6 Orientation (Grain Direction)
- If rot = false, the part must be placed with its specified (w, h) (no rotation). If rot = true, (w, h) or (h, w) may be used.

5.7 Guillotine Feasibility (optional; applies if guillotine = true)
- For each board instance, the set of placed rectangles must be obtainable via a sequence of recursive orthogonal full‑length cuts. Equivalently, there exists a binary slicing (guillotine) tree whose leaves correspond to the placed rectangles and whose internal nodes represent horizontal or vertical full‑length cuts separating two sub‑rectangles.

5.8 Board Usage Integrality
- The number of boards used for each board type is an integer ≥ 0. If pattern duplication is allowed, the same layout may be replicated across multiple identical boards.

5.9 Leftover Retention Rules
- Any rectangular region not occupied by parts after cutting may be recorded as a retained leftover only if both its width and height are ≥ min_keep. Otherwise it is treated as waste.

5.10 Edge Margin
- No part or cut line may encroach within edge_margin of the board outer boundary (safety and handling tolerance).

5.11 Machine/Process Constraints (optional)
- Orientation of first cut (e.g., must start along long edge).
- Maximum number of cuts per board or maximum cut depth.
- Minimum dimension on any cut segment (to ensure stability and safety during cutting).

## 6. Derived Quantities and Metrics

- Area utilization per board = (sum of placed part areas on the board) / (board area).
- Global utilization = (sum of placed part areas) / (sum of board areas used).
- Total waste area = sum(board areas) − sum(placed part areas) − (optional) retained leftover areas (if counted as non‑waste).
- Cut length = sum of lengths of all cut segments executed.
- Leftover inventory = multiset of retained leftover pieces with dimensions and attributes for future runs.

## 7. Variants (choose as applicable)

- Non‑guillotine vs. guillotine‑constrained packing.
- Single board size vs. multiple board types with selection/costs.
- With vs. without initial leftover inventory.
- Strict vs. flexible demand (allow overproduction or penalties for underfill).
- Deterministic vs. stochastic objectives (e.g., expected leftover value under future demand distribution).

## 8. Assumptions

- Geometry is orthogonal; parts and boards are rectangles with edges aligned to axes.
- Measurements are in consistent units (e.g., millimeters).
- Kerf is uniform and applied consistently across cuts.
- Material attributes fully capture compatibility (no implicit mixing allowed).

## 9. Acceptance Criteria (example)

An instance is considered feasibly solved if:
- All demand constraints (5.1) are satisfied.
- All geometric and process constraints (5.2–5.10) are satisfied.
- Objective value is reported with accompanying metrics (utilization, boards used, waste, cut length).
- The solution provides, per board, either: (a) coordinates and orientations of placed parts with declared kerf/clearances; or (b) a guillotine cut tree and leaf rectangles if guillotine is required.

## 10. Data Exchange (optional guidance)

While not mandated, solutions typically exchange data using:
- Parts: list of objects with id, w, h, q, rot, attr.
- Board types: list with type_id, W, H, attr, cost (optional).
- Leftovers: list with lof_id, Wl, Hl, attr, qty.
- Parameters: kerf, edge_margin, min_keep, guillotine, objective selection/weights.
- Output: selected boards, per‑board placements (x, y, orientation), optional cut plan, retained leftovers, metrics.

