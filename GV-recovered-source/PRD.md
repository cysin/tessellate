# Product Requirements Document (PRD)
## GV Board Cutting Optimization System

**Document Version:** 1.0
**Last Updated:** 2025-11-08
**Product:** GV (板材优化开料系统 - Board Cutting Optimization System)
**Status:** Reverse-Engineered from Production Code

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [Problem Statement](#3-problem-statement)
4. [Goals & Objectives](#4-goals--objectives)
5. [Target Users & Personas](#5-target-users--personas)
6. [User Stories](#6-user-stories)
7. [Functional Requirements](#7-functional-requirements)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [User Interface Specifications](#9-user-interface-specifications)
10. [Technical Architecture](#10-technical-architecture)
11. [Data Models](#11-data-models)
12. [Algorithm Specifications](#12-algorithm-specifications)
13. [Integration Requirements](#13-integration-requirements)
14. [Success Metrics](#14-success-metrics)
15. [Constraints & Limitations](#15-constraints--limitations)
16. [Future Enhancements](#16-future-enhancements)
17. [Dependencies](#17-dependencies)
18. [Risks & Mitigation](#18-risks--mitigation)
19. [Appendix](#19-appendix)

---

## 1. Executive Summary

### 1.1 Product Vision

GV is a web-based cutting optimization system designed to minimize material waste and maximize efficiency in furniture manufacturing. The system solves the 2D Cutting Stock Problem by automatically generating optimal cutting patterns for wood panels, plywood sheets, and other board materials.

### 1.2 Business Value

- **Reduce Material Waste:** Optimize sheet utilization by 75-85%, reducing raw material costs
- **Increase Production Efficiency:** Automate cutting pattern generation, reducing planning time from hours to seconds
- **Improve Manufacturing Quality:** Provide visual cutting diagrams and batch consolidation for consistent production
- **Minimize Human Error:** Eliminate manual calculation errors in material estimation

### 1.3 Target Market

- Custom furniture manufacturers (wardrobes, cabinets, shelves)
- Kitchen cabinet manufacturers
- Woodworking shops
- Interior design companies
- Building material suppliers

### 1.4 Key Features

1. Multi-product cutting optimization with grain direction support
2. Leftover material inventory management and reuse prioritization
3. Visual cutting diagram generation with precise measurements
4. Batch pattern consolidation for manufacturing efficiency
5. Support for 7 standard board sizes (4×8 to 5×10 feet)
6. Configurable saw kerf (blade width) and utilization thresholds

---

## 2. Product Overview

### 2.1 Product Type

Web application (JSP-based) with server-side optimization engine

### 2.2 Core Functionality

The GV system accepts a list of products (furniture components) to be cut from standard board sheets and generates optimized cutting patterns that:
- Minimize the number of sheets required
- Maximize material utilization rate
- Respect grain direction constraints
- Prioritize leftover material reuse
- Consolidate identical cutting patterns for batch production

### 2.3 Product Scope

**In Scope:**
- 2D rectangular cutting optimization
- Single material type per optimization run (grouped by color/thickness)
- Guillotine cuts only (no arbitrary shapes)
- Grain direction constraints (directional vs. mixed)
- Leftover material tracking and reuse
- Visual cutting diagram generation
- Print-ready cutting instructions

**Out of Scope:**
- 3D optimization or nested volumes
- Curved/irregular shape cutting
- Multi-factory distributed optimization
- Real-time inventory management integration
- CNC machine direct control
- Cost estimation and pricing

---

## 3. Problem Statement

### 3.1 Current Challenges

**For Furniture Manufacturers:**
1. **Manual Calculation Inefficiency:** Production planners spend 2-4 hours manually calculating cutting patterns for each order
2. **High Material Waste:** Manual layouts achieve only 60-70% material utilization, resulting in 30-40% waste
3. **Inconsistent Quality:** Different planners produce different results, causing variable material costs
4. **Leftover Management Difficulty:** Tracking and reusing leftover pieces is done manually, often resulting in usable material being discarded
5. **Scaling Challenges:** Large orders with 50+ unique components become extremely complex to optimize manually

**Business Impact:**
- Material costs represent 40-60% of furniture manufacturing expenses
- 20-30% waste directly reduces profit margins
- Manual planning delays production by 1-2 days per order
- Inconsistent cutting patterns complicate inventory management

### 3.2 Root Causes

1. **Computational Complexity:** The 2D Cutting Stock Problem is NP-Hard, making manual optimization infeasible
2. **Lack of Tooling:** Affordable, Chinese-language optimization software is limited
3. **Domain Expertise Required:** Effective manual optimization requires years of experience
4. **Data Management:** Tracking leftover materials across multiple jobs requires systematic processes

---

## 4. Goals & Objectives

### 4.1 Primary Goals

| Goal | Success Metric | Target |
|------|----------------|--------|
| Reduce Material Waste | Average utilization rate | ≥ 75% |
| Decrease Planning Time | Time to generate cutting plan | < 30 seconds |
| Improve Consistency | Standard deviation in utilization | < 5% |
| Enable Leftover Reuse | Leftover material reuse rate | ≥ 20% |
| Increase Throughput | Orders processed per day | +50% |

### 4.2 User Experience Goals

1. **Simplicity:** Non-technical production staff can use the system with < 10 minutes training
2. **Speed:** Generate optimization results in real-time (< 5 seconds for typical orders)
3. **Clarity:** Provide visual cutting diagrams that shop floor workers can follow without confusion
4. **Flexibility:** Support common board sizes and configurable cutting parameters
5. **Localization:** Full Chinese language support for UI and documentation

### 4.3 Business Objectives

1. **Cost Reduction:** Reduce material costs by 10-15% through waste minimization
2. **Operational Efficiency:** Reduce production planning labor by 60-80%
3. **Quality Improvement:** Eliminate calculation errors that cause material shortages
4. **Competitive Advantage:** Offer faster quotes and lower prices to customers

---

## 5. Target Users & Personas

### 5.1 Primary Persona: Production Planner (生产计划员)

**Demographics:**
- Age: 28-45
- Role: Production Planning Manager
- Experience: 3-8 years in furniture manufacturing
- Education: Vocational/technical school

**Goals:**
- Minimize material waste to meet company cost targets
- Generate cutting plans quickly to maintain production schedules
- Ensure cutting patterns are clear and error-free for shop workers
- Track leftover materials for future jobs

**Pain Points:**
- Manual calculation is time-consuming and error-prone
- Pressure to optimize costs while maintaining fast turnaround
- Difficulty tracking and reusing leftover materials
- Communication gaps between planning and shop floor

**Technical Proficiency:**
- Comfortable with basic computer operations (web browsers, spreadsheets)
- Not familiar with complex software or programming
- Prefers simple, intuitive interfaces

### 5.2 Secondary Persona: Shop Floor Supervisor (车间主管)

**Demographics:**
- Age: 35-55
- Role: Workshop Supervisor/Cutting Machine Operator
- Experience: 10+ years in woodworking
- Education: Technical school or apprenticeship

**Goals:**
- Receive clear, unambiguous cutting instructions
- Minimize material waste during actual cutting operations
- Identify and report leftover materials for reuse
- Maintain cutting accuracy and quality

**Pain Points:**
- Handwritten or unclear cutting diagrams cause errors
- Confusion about grain direction requirements
- Difficulty tracking which pieces belong to which orders
- Leftover materials not systematically documented

**Technical Proficiency:**
- Basic computer literacy (can view and print web pages)
- Prefers printed instructions over digital screens
- Values simplicity and clarity over features

### 5.3 Tertiary Persona: Factory Owner (工厂老板)

**Demographics:**
- Age: 35-60
- Role: Factory Owner/General Manager
- Experience: 5-20 years in furniture business

**Goals:**
- Reduce overall material costs
- Improve production efficiency and throughput
- Maintain quality and consistency
- Data-driven decision making

**Pain Points:**
- Lack of visibility into material utilization rates
- Difficulty comparing efficiency across different planners
- No historical data for cost analysis
- Uncertainty about ROI of optimization software

---

## 6. User Stories

### 6.1 Core User Stories

#### US-001: Generate Basic Cutting Plan
**As a** production planner
**I want to** input a list of furniture components and generate an optimized cutting plan
**So that** I can minimize material waste and reduce costs

**Acceptance Criteria:**
- Can enter product dimensions (length, width, thickness) via web form
- Can specify quantity for each product
- Can select board size from standard options (4×8, 5×8, etc.)
- System generates cutting plan in < 5 seconds
- Displays material utilization percentage
- Shows visual cutting diagrams with measurements

#### US-002: Specify Grain Direction
**As a** production planner
**I want to** mark certain products as "directional" (grain direction matters)
**So that** the system respects wood grain requirements for visible surfaces

**Acceptance Criteria:**
- Can mark each product as "directional" (单向) or "mixed" (混合)
- Directional products are not rotated in cutting patterns
- Mixed products can be rotated 90° for better optimization
- Visual diagrams show product orientation clearly

#### US-003: Prioritize Leftover Material
**As a** production planner
**I want to** add leftover materials from previous jobs to the optimization
**So that** existing inventory is used before cutting new sheets

**Acceptance Criteria:**
- Can enable "leftover material priority" checkbox (库存余料优先)
- Can input leftover piece dimensions (length, width, thickness, color)
- System attempts to place products on leftover pieces first
- Displays which products were cut from leftover vs. new sheets
- Shows remaining leftover pieces after optimization

#### US-004: Batch Pattern Consolidation
**As a** production planner
**I want** identical cutting patterns to be consolidated
**So that** shop floor workers can cut multiple sheets with the same setup

**Acceptance Criteria:**
- System identifies identical cutting patterns across multiple sheets
- Groups patterns and shows batch quantity (e.g., "3× this pattern")
- Reduces visual diagram count by consolidating duplicates
- Shows total quantity of each product across all patterns

#### US-005: Print Cutting Instructions
**As a** shop floor supervisor
**I want to** print clear cutting diagrams with measurements
**So that** machine operators can execute cuts accurately

**Acceptance Criteria:**
- Print button generates printer-friendly format
- Each diagram shows sheet dimensions and all product placements
- Product codes, dimensions, and positions are clearly labeled
- Grain direction is indicated visually
- Leftover areas are marked for salvage

#### US-006: Configure Cutting Parameters
**As a** production planner
**I want to** adjust saw kerf (blade width) and utilization threshold
**So that** optimization matches our equipment and quality standards

**Acceptance Criteria:**
- Can set saw kerf from 2-6mm (default: 3mm)
- Can set minimum utilization threshold 0.50-0.90 (default: 0.78)
- System accounts for kerf loss in all calculations
- Only accepts cutting patterns above utilization threshold

### 6.2 Advanced User Stories

#### US-007: Multi-Color/Material Grouping
**As a** production planner
**I want** products to be automatically grouped by color and thickness
**So that** each cutting plan uses only one material type

**Acceptance Criteria:**
- System groups products by color name (花色)
- System groups by thickness (厚度)
- Generates separate cutting plans for each color+thickness combination
- Displays grouping clearly in results

#### US-008: Handle Mixed Thicknesses
**As a** production planner
**I want** an order with multiple thicknesses to be optimized separately
**So that** each thickness gets its own optimized cutting plan

**Acceptance Criteria:**
- Products with different thicknesses are processed in separate batches
- Each thickness shows its own material utilization statistics
- Leftover materials are tracked per thickness

#### US-009: View Leftover Material Summary
**As a** production planner
**I want to** see a detailed list of leftover pieces after optimization
**So that** I can add them to inventory for future jobs

**Acceptance Criteria:**
- System calculates all leftover pieces > minimum size (e.g., 200×200mm)
- Shows leftover dimensions, location on sheet, and quantity
- Categorizes leftover by type (edge pieces, corner pieces, center pieces)
- Provides option to export leftover list

---

## 7. Functional Requirements

### 7.1 Product Input & Configuration

#### FR-001: Product Data Entry
**Priority:** P0 (Critical)
**Description:** Users can enter product specifications via web form

**Details:**
- **Required Fields:**
  - Product Code (编号): Alphanumeric identifier (e.g., "A001")
  - Product Name (名称): Descriptive name (e.g., "侧板 - Side Panel")
  - Length (长): Integer, millimeters (e.g., 2000)
  - Width (宽): Integer, millimeters (e.g., 600)
  - Thickness (厚): Integer, millimeters (e.g., 18)
  - Color/Material (花色): Text (e.g., "白橡木 - White Oak")
  - Quantity (数量): Integer, number of pieces (e.g., 2)
  - Grain Direction (纹理方向): Radio button (单向/混合)

- **Input Methods:**
  - Web form with "Add Row" button for multiple products
  - Comma-separated values (CSV) for each row
  - Maximum 100 products per optimization run

- **Validation:**
  - All dimensions must be > 0 and < 10,000mm
  - Quantity must be ≥ 1 and ≤ 999
  - Product codes must be unique within an order
  - Thickness must match available board thicknesses

#### FR-002: Board Configuration
**Priority:** P0 (Critical)
**Description:** Users can select board size and configure cutting parameters

**Details:**
- **Board Size Selection (板材规格):** Dropdown menu with options:
  - 4×8 呎 (1220 × 2440 mm)
  - 5×8 呎 (1530 × 2440 mm)
  - 4×9 呎 (1220 × 2750 mm)
  - 5×9 呎 (1530 × 2750 mm)
  - 4×10 呎 (1220 × 3060 mm)
  - 5×10 呎 (1530 × 3060 mm)
  - Custom (user-defined dimensions)

- **Saw Kerf (裁切锯口尺寸):** Numeric input, 2-6mm, default 3mm
- **Utilization Threshold (板材利用率):** Numeric input, 0.50-0.90, default 0.78
- **Optimization Attempts:** Hidden parameter, default 6 random placement attempts

#### FR-003: Leftover Material Management
**Priority:** P1 (High)
**Description:** Users can add leftover materials from inventory

**Details:**
- **Enable/Disable:** Checkbox "库存余料优先" (Prioritize Leftover Material)
- **Leftover Input Fields:**
  - Length (长): Integer, millimeters
  - Width (宽): Integer, millimeters
  - Thickness (厚): Integer, millimeters
  - Color/Material (花色): Text (must match product colors)
  - Quantity (数量): Integer, number of leftover pieces

- **Behavior:**
  - When enabled, system attempts to place products on leftover pieces first
  - Leftover pieces are treated as priority materials
  - Unused leftover pieces remain in leftover inventory
  - New leftover pieces generated from optimization are added to list

### 7.2 Optimization Engine

#### FR-004: Cutting Pattern Generation
**Priority:** P0 (Critical)
**Description:** System generates optimized cutting patterns using 2D bin packing algorithm

**Algorithm Requirements:**
- **Grouping Phase:**
  - Group products by color + thickness
  - Group materials by color + thickness
  - Process each group independently

- **Placement Strategy:**
  - Sort products by area (largest first)
  - For each material sheet:
    - Try 6 random placement orientations
    - Use guillotine cuts only (no arbitrary angles)
    - Recursively fill remaining space with smaller products
    - Select placement with highest utilization

- **Utilization Calculation:**
  - utilization = sum(product_areas) / sheet_area
  - Accept pattern if utilization ≥ threshold
  - Account for saw kerf in all dimension calculations

- **Remainder Handling:**
  - Track leftover pieces from each cut
  - Attempt to fill leftover areas with additional products
  - Mark leftover pieces < 200×200mm as non-reusable waste

#### FR-005: Grain Direction Constraints
**Priority:** P0 (Critical)
**Description:** System respects grain direction settings

**Details:**
- **Directional Products (单向):**
  - Cannot be rotated 90°
  - Length orientation is fixed
  - Typically used for visible surfaces (doors, drawer fronts)

- **Mixed Products (混合):**
  - Can be rotated 90° if it improves utilization
  - System tries both orientations and selects best fit
  - Typically used for internal components (shelves, dividers)

- **Visual Indication:**
  - Cutting diagrams show arrow or marker for grain direction
  - Directional products use different color/pattern in diagrams

#### FR-006: Pattern Consolidation
**Priority:** P1 (High)
**Description:** System consolidates identical cutting patterns for batch production

**Details:**
- **Pattern Matching:**
  - Compare cutting patterns by dimensions, positions, and product list
  - Patterns with identical layouts are merged
  - Display batch quantity (m_u_count) for consolidated patterns

- **Benefits:**
  - Reduces diagram count for large orders
  - Allows shop floor to set up cutting machine once for multiple sheets
  - Improves manufacturing efficiency

- **Display:**
  - Show "3× this pattern" or similar notation
  - List all sheets using this pattern
  - Total products across all identical patterns

### 7.3 Output & Visualization

#### FR-007: Visual Cutting Diagrams
**Priority:** P0 (Critical)
**Description:** System generates visual diagrams showing product placement on sheets

**Diagram Elements:**
- **Sheet Boundary:** Rectangle representing full sheet dimensions
- **Product Rectangles:** Each product shown as rectangle with:
  - Product code (e.g., "A001")
  - Dimensions (e.g., "2000×600")
  - Position coordinates (top-left corner)
  - Grain direction indicator (if directional)

- **Measurements:**
  - All dimensions in millimeters
  - Position coordinates (X, Y) from top-left origin
  - Leftover area dimensions

- **Color Coding:**
  - Different products use different colors (if display supports)
  - Leftover areas shown in gray or white
  - Waste areas (too small to reuse) shown with hatching

- **Legend:**
  - Product list with codes and quantities
  - Sheet size and utilization percentage
  - Total sheets required

#### FR-008: Material Utilization Statistics
**Priority:** P1 (High)
**Description:** System calculates and displays material efficiency metrics

**Metrics:**
- **Per-Sheet Utilization:** Percentage of each sheet used by products
- **Overall Utilization:** Average across all sheets
- **Total Sheets Required:** Count of sheets needed
- **Total Product Area:** Sum of all product areas
- **Total Waste Area:** Sum of all leftover areas
- **Leftover Piece Count:** Number of reusable leftover pieces
- **Non-Reusable Waste:** Area of waste too small to salvage

**Display Format:**
```
Material Summary:
- Total sheets required: 3
- Sheet size: 4×8 呎 (1220×2440mm)
- Overall utilization: 82.3%
- Total product area: 7,350,000 mm²
- Total waste area: 1,580,000 mm²
- Reusable leftover: 12 pieces
```

#### FR-009: Leftover Material Report
**Priority:** P1 (High)
**Description:** System generates list of leftover pieces for inventory

**Report Contents:**
- **Leftover Piece Details:**
  - Dimensions (length × width)
  - Thickness and color
  - Source sheet number
  - Position on sheet (for cutting reference)
  - Quantity (if multiple identical pieces)

- **Categorization:**
  - Type: Left edge, Top edge, Corner piece, Center piece
  - Size category: Large (>600mm), Medium (300-600mm), Small (200-300mm)
  - Reusability: Reusable vs. Too Small to Save

- **Export Options:**
  - Print to PDF
  - Copy to clipboard for manual entry into inventory system

#### FR-010: Print-Ready Output
**Priority:** P0 (Critical)
**Description:** Users can print cutting diagrams for shop floor use

**Print Features:**
- **Format:** Standard A4 or Letter size pages
- **Layout:** One cutting pattern per page (or multiple if patterns are small)
- **Content:**
  - Sheet number and pattern identifier
  - Full-size diagram with all measurements
  - Product list table with codes, names, dimensions, quantities
  - Cutting sequence suggestions (if applicable)
  - Batch information (if pattern is repeated)

- **Quality:**
  - High-contrast black and white (for clarity)
  - Large, readable fonts (minimum 10pt)
  - Clear line drawings (no anti-aliasing artifacts)

### 7.4 Data Persistence (Optional)

#### FR-011: Save Optimization Results
**Priority:** P2 (Medium)
**Description:** Users can save optimization results for future reference

**Details:**
- **Save Format:** JSON or XML
- **Saved Data:**
  - Product specifications
  - Board configuration
  - Generated cutting patterns
  - Material statistics
  - Timestamp and user identifier

- **Retrieval:**
  - Load saved results to view/modify
  - Export to external systems

**Note:** Current implementation returns results as JSON but does not persist to database

---

## 8. Non-Functional Requirements

### 8.1 Performance

#### NFR-001: Response Time
- **Requirement:** Generate optimization results in < 5 seconds for typical orders
- **Typical Order:** 20-50 products, 1-3 material groups
- **Maximum Order:** 100 products, < 30 seconds
- **Measurement:** 95th percentile response time under normal load

#### NFR-002: Scalability
- **Concurrent Users:** Support 10 concurrent optimization requests
- **Peak Load:** Handle 50 requests per hour during business hours
- **Resource Limits:** Maximum 2GB memory per optimization request

#### NFR-003: Optimization Quality
- **Minimum Utilization:** Achieve ≥ 75% average material utilization
- **Consistency:** Standard deviation < 5% across multiple runs (note: current implementation uses randomization)
- **Waste Reduction:** Reduce material waste by ≥ 10% vs. manual planning

### 8.2 Usability

#### NFR-004: Learning Curve
- **Training Time:** Users should be productive within 10 minutes of training
- **Interface Complexity:** Maximum 3 clicks to generate cutting plan
- **Error Recovery:** Clear error messages with corrective guidance

#### NFR-005: Accessibility
- **Language:** Full Chinese language support (Simplified Chinese)
- **Browser Compatibility:** Support IE 11+, Chrome, Firefox, Edge
- **Screen Resolution:** Support 1024×768 minimum resolution
- **Input Methods:** Support keyboard-only navigation

#### NFR-006: Visual Clarity
- **Diagram Legibility:** All measurements readable at 100% zoom
- **Color Scheme:** High contrast for visibility in bright workshop environments
- **Print Quality:** Diagrams remain clear when printed in black and white

### 8.3 Reliability

#### NFR-007: Availability
- **Uptime Target:** 99% during business hours (8am-8pm, 7 days/week)
- **Planned Maintenance:** Maximum 4 hours/month during off-hours
- **Recovery Time:** < 1 hour in case of failure

#### NFR-008: Data Integrity
- **Calculation Accuracy:** All dimension calculations accurate to 0.1mm
- **No Data Loss:** Optimization results displayed must be accurate and reproducible
- **Error Handling:** Invalid input rejected with clear error messages

#### NFR-009: Fault Tolerance
- **Input Validation:** Prevent processing of invalid data
- **Graceful Degradation:** Display partial results if optimization cannot complete
- **Error Logging:** Log all errors for debugging

### 8.4 Security

#### NFR-010: Authentication (Future)
- **User Access:** No authentication required in current version
- **Future:** Support user login and role-based access control

#### NFR-011: Data Privacy
- **Customer Data:** Product specifications should not be logged or shared
- **Isolation:** Each optimization session isolated (no cross-contamination)

### 8.5 Maintainability

#### NFR-012: Code Quality
- **Modularity:** Separate presentation, business logic, and data layers
- **Documentation:** Code comments for complex algorithms
- **Testing:** Unit tests for core optimization logic (currently lacking)

#### NFR-013: Configuration
- **Board Sizes:** Board size list configurable without code changes (currently hardcoded)
- **Algorithm Parameters:** Tunable parameters (saw kerf, utilization threshold, placement attempts)

### 8.6 Compatibility

#### NFR-014: Platform Support
- **Server:** Java 7+ runtime environment
- **Application Server:** Apache Tomcat 8.5.x or compatible
- **Operating System:** Linux, Windows Server
- **Database:** None required (stateless operation)

#### NFR-015: Integration
- **Input Format:** Accept CSV or web form input
- **Output Format:** JSON for programmatic access, HTML for display, print for shop floor
- **API:** RESTful endpoint for external system integration (via Struts action)

---

## 9. User Interface Specifications

### 9.1 Page Layout

#### Page: Product Input (input.jsp)

**Layout Structure:**
```
+----------------------------------------------------------+
|  [Logo]  GV板材优化开料系统                                |
+----------------------------------------------------------+
|  产品构件开料明细 (Product Cutting Details)                  |
|                                                          |
|  [Add Row Button] 添加                                     |
|                                                          |
|  +------------------------------------------------------+ |
|  | 编号 | 名称 | 长 | 宽 | 厚 | 花色 | 数量 | 纹理方向       | |
|  |------|------|----|----|----|----|------|-------------| |
|  | A001 | 侧板 |2000| 600| 18 |白橡木|  2  | ○单向 ○混合  | |
|  | [Input fields continue for multiple rows...]          | |
|  +------------------------------------------------------+ |
|                                                          |
|  板材配置 (Board Configuration)                            |
|  +------------------------------------------------------+ |
|  | 板材规格: [Dropdown: 4×8 呎 ▼]                          | |
|  | 锯口尺寸: [Input: 3] mm                                 | |
|  | 利用率:   [Input: 0.78]                                | |
|  +------------------------------------------------------+ |
|                                                          |
|  ☐ 库存余料优先 (Prioritize Leftover Material)             |
|                                                          |
|  [Leftover material input section - hidden by default]  |
|                                                          |
|  [确认完成 Button]  [确认开板 Button]                      |
+----------------------------------------------------------+
```

**Input Form Specifications:**
- **Table Layout:** Dynamic table with "Add Row" button
- **Field Widths:**
  - 编号 (Code): 80px
  - 名称 (Name): 120px
  - 长/宽/厚 (L/W/T): 60px each
  - 花色 (Color): 100px
  - 数量 (Qty): 50px
  - 纹理 (Grain): 150px (radio buttons)

- **Input Validation:**
  - Numeric fields only accept integers
  - Dimensions: 1-10,000 range
  - Quantity: 1-999 range
  - Required field indicators (red asterisk)

- **Actions:**
  - "添加" (Add): Add new product row
  - "确认完成" (Confirm Complete): Validate input
  - "确认开板" (Generate Plan): Submit for optimization

#### Page: Cutting Plan Results (result.jsp)

**Layout Structure:**
```
+----------------------------------------------------------+
|  [Logo]  GV板材优化开料系统 - 开料方案                       |
+----------------------------------------------------------+
|  材料统计 (Material Statistics)                            |
|  +------------------------------------------------------+ |
|  | 总用板数: 3 张                                          | |
|  | 板材规格: 4×8 呎 (1220×2440mm)                          | |
|  | 平均利用率: 82.3%                                       | |
|  | 总产品面积: 7,350,000 mm²                               | |
|  | 余料数量: 12 件                                         | |
|  +------------------------------------------------------+ |
|                                                          |
|  开料图 (Cutting Diagrams)                                 |
|                                                          |
|  板材 #1 - 利用率: 85.2% (重复 2 次)                       |
|  +------------------------------------------------------+ |
|  |                                                      | |
|  |  +-----------+  +--------+                          | |
|  |  |  A001     |  | A002   |                          | |
|  |  | 2000×600  |  | 900×600|                          | |
|  |  |           |  |        |                          | |
|  |  +-----------+  +--------+                          | |
|  |                                                      | |
|  |  [Leftover: 1220×840]                               | |
|  |                                                      | |
|  +------------------------------------------------------+ |
|                                                          |
|  产品清单 (Product List)                                   |
|  +------------------------------------------------------+ |
|  | 产品编号 | 名称 | 尺寸 | 数量 | 已排 | 未排 |            | |
|  |---------|------|------|------|------|------|           | |
|  | A001    | 侧板 | 2000×600×18 | 2 | 2 | 0 |           | |
|  | A002    | 顶板 | 900×600×18  | 2 | 2 | 0 |           | |
|  +------------------------------------------------------+ |
|                                                          |
|  余料清单 (Leftover Material List)                         |
|  +------------------------------------------------------+ |
|  | 尺寸 | 厚度 | 花色 | 数量 | 位置 |                      | |
|  |------|------|------|------|------|                     | |
|  | 1220×840 | 18 | 白橡木 | 1 | 板材#1 右侧 |           | |
|  | 600×400  | 18 | 白橡木 | 2 | 板材#2 顶部 |           | |
|  +------------------------------------------------------+ |
|                                                          |
|  [打印 Button]  [返回修改 Button]  [保存方案 Button]        |
+----------------------------------------------------------+
```

**Diagram Specifications:**
- **Canvas:** SVG or Canvas element for visual rendering
- **Coordinate System:** Top-left origin (0,0)
- **Scale:** Auto-scale to fit display area while maintaining aspect ratio
- **Colors:**
  - Product rectangles: Light blue (#E3F2FD)
  - Product borders: Dark blue (#1976D2)
  - Leftover areas: Light gray (#F5F5F5)
  - Waste areas: Hatched pattern
  - Sheet boundary: Black 2px border

- **Labels:**
  - Product code: Bold, 14px
  - Dimensions: Regular, 12px
  - Position coordinates: Small, 10px, gray color

- **Interactive Features (Future):**
  - Hover to highlight product and show details
  - Click product to view in product list
  - Zoom in/out controls

### 9.2 Visual Design Guidelines

#### Color Palette
- **Primary:** Blue (#1976D2) - Actions, headers
- **Secondary:** Gray (#757575) - Labels, borders
- **Accent:** Green (#4CAF50) - Success states, utilization > 80%
- **Warning:** Orange (#FF9800) - Utilization 60-80%
- **Error:** Red (#F44336) - Validation errors, utilization < 60%
- **Background:** White (#FFFFFF)
- **Surface:** Light gray (#FAFAFA)

#### Typography
- **Headings:** SimHei (黑体), 18-24px, Bold
- **Body Text:** SimSun (宋体), 14px, Regular
- **Input Fields:** Arial, 14px (for better number readability)
- **Diagrams:** Arial, 10-14px

#### Spacing
- **Padding:** 16px standard, 8px compact
- **Margin:** 24px between sections, 12px between elements
- **Grid:** 12-column responsive grid (though current version is desktop-only)

---

## 10. Technical Architecture

### 10.1 Architecture Overview

**Architecture Pattern:** Model-View-Controller (MVC) with Struts 2 Framework

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  input.jsp   │  │ result.jsp   │  │ print.jsp    │      │
│  │  (Product    │  │ (Cutting     │  │ (Print View) │      │
│  │   Input)     │  │  Results)    │  │              │      │
│  └──────┬───────┘  └──────▲───────┘  └──────▲───────┘      │
│         │                 │                  │              │
└─────────┼─────────────────┼──────────────────┼──────────────┘
          │                 │                  │
┌─────────▼─────────────────┴──────────────────┴──────────────┐
│                    Controller Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          ViewAction (Struts 2 Action)                │   │
│  │  - createView()                                      │   │
│  │  - processProducts()                                 │   │
│  │  Properties: product_no[], product_name[], ...      │   │
│  └─────────────────────┬────────────────────────────────┘   │
│                        │                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                  Business Logic Layer                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           ViewServiceR2 (Optimization Engine)        │   │
│  │  - createView(products, materials, saw_bite, scale)  │   │
│  │  - processProduct() - Group products                 │   │
│  │  - processMaterial() - Group materials               │   │
│  │  - scoreMaterial() - Sort materials                  │   │
│  │  - scoreAreaProduct() - Sort products by area        │   │
│  │  - queryUsedProducts() - Consolidate patterns        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Utility Classes                         │   │
│  │  - CommonTools: Deep cloning via serialization       │   │
│  │  - DecimalMath: Precision arithmetic (BigDecimal)    │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 Domain Models                        │   │
│  │  - Product: Furniture components                     │   │
│  │  - Material: Board sheets                            │   │
│  │  - Scheme: Product-Material mapping                  │   │
│  │  - Constant: Board size definitions                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  [No Database Layer - Stateless Operation]                  │
└──────────────────────────────────────────────────────────────┘
```

### 10.2 Technology Stack

#### Server-Side
- **Language:** Java 7
- **Framework:** Struts 2.3.1.2
- **Dependency Injection:** Spring 3.0.6
- **Application Server:** Apache Tomcat 8.5.x
- **Build Tool:** Shell script + javac (no Maven/Gradle)

#### Client-Side
- **HTML:** JSP (JavaServer Pages)
- **CSS:** Inline + external stylesheets
- **JavaScript:** jQuery (likely, for dynamic form manipulation)
- **Graphics:** SVG or Canvas for cutting diagrams

#### Libraries & Dependencies
- **Spring Framework 3.0.6:**
  - spring-core, spring-beans, spring-context
  - spring-web, spring-aop
  - spring-jdbc, spring-transaction (not used)

- **Struts 2:**
  - struts2-core-2.3.1.2.jar
  - struts2-spring-plugin-2.2.3.1.jar
  - struts2-json-plugin-2.2.3.1.jar (for JSON output)
  - xwork-core-2.3.1.2.jar
  - ognl-3.0.4.jar

- **Commons Libraries:**
  - commons-io-2.0.1.jar
  - commons-lang-2.5.jar
  - commons-fileupload-1.2.2.jar
  - commons-logging.jar

- **Other:**
  - freemarker-2.3.18.jar (templating)
  - javassist-3.11.0.GA.jar (bytecode manipulation)
  - log4j-1.2.14.jar (logging)

### 10.3 Deployment Architecture

**Single-Server Deployment:**
```
┌─────────────────────────────────────────┐
│         Linux Server (Production)       │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │    Apache Tomcat 8.5.57           │ │
│  │                                   │ │
│  │  Service: Catalina2 (Port 8089)  │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  GV.war                     │ │ │
│  │  │  - WEB-INF/classes/         │ │ │
│  │  │  - WEB-INF/lib/             │ │ │
│  │  │  - *.jsp, *.html, *.jpg     │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [No Database Required]                 │
└─────────────────────────────────────────┘
          │
          ▼
   Browser (Client)
   http://server:8089/GV/input.jsp
```

**Scalability Notes:**
- Current architecture is single-threaded per request
- No session state (stateless optimization)
- Can scale horizontally with load balancer (future)
- No shared database means no data consistency issues

### 10.4 Data Flow

**Request Processing Flow:**
```
1. User fills form in input.jsp
   - Enters product data
   - Selects board configuration
   - Clicks "确认开板"

2. Browser submits POST to /GV/createView.action
   - Parameters: product_no[], product_name[], product_height[], ...
   - Content-Type: application/x-www-form-urlencoded

3. Struts 2 interceptor chain processes request
   - Parameter binding to ViewAction properties
   - Validation (if configured)
   - Action invocation

4. ViewAction.createView() executes
   - Parse CSV arrays into Product objects
   - Create rotation variants for rotatable products
   - Load Material definitions from Constant.class
   - Call ViewServiceR2.createView()

5. ViewServiceR2.createView() performs optimization
   - Group products by color+thickness
   - Group materials by color+thickness
   - For each group:
     - Sort materials and products
     - Try 6 random placement attempts
     - Select best pattern (highest utilization)
     - Recursively fill remainder areas
   - Consolidate identical patterns
   - Calculate leftover materials

6. ViewServiceR2 returns List<Material>
   - Each Material contains placed products
   - Nested m_materials for remainders
   - Statistics calculated (utilization, waste, etc.)

7. ViewAction sets result properties
   - materials = optimized material list
   - result = "success"

8. Struts returns to result.jsp
   - Iterate materials to render diagrams
   - Display statistics
   - Show product and leftover lists

9. Browser renders HTML response
   - User views cutting diagrams
   - Option to print or modify
```

---

## 11. Data Models

### 11.1 Product Model

**Class:** `com.gv.model.Product`
**Purpose:** Represents a furniture component to be cut from board material

**Attributes:**

| Field | Type | Description | Example | Constraints |
|-------|------|-------------|---------|-------------|
| p_no | String | Product code/identifier | "A001" | Unique, 1-20 chars |
| p_name | String | Product name | "侧板" | 1-50 chars |
| p_height | double | Length dimension (mm) | 2000.0 | > 0, < 10000 |
| p_width | double | Width dimension (mm) | 600.0 | > 0, < 10000 |
| p_weight | double | Thickness (mm) | 18.0 | > 0, < 100 |
| p_color | String | Material color/type | "白橡木" | 1-30 chars |
| p_count | int | Total quantity needed | 2 | ≥ 1, ≤ 999 |
| p_r_count | int | Remaining quantity to place | 0-2 | ≥ 0 |
| p_is_dir | int | Grain direction: 0=rotatable, 1=fixed | 1 | 0 or 1 |
| p_is_copy | int | Rotation variant flag | 0 | 0 or 1 |
| p_is_show | int | Placement status: 0=unplaced, 1=placed | 1 | 0 or 1 |
| m_left | double | X position on material (mm) | 0.0 | ≥ 0 |
| m_top | double | Y position on material (mm) | 0.0 | ≥ 0 |
| p_n_left | double | Normalized X position | 0.0 | ≥ 0 |
| p_n_top | double | Normalized Y position | 0.0 | ≥ 0 |
| p_is_score | int | Pattern scoring flag | 0 | 0 or 1 |
| p_i_score | int | Instance scoring flag | 0 | 0 or 1 |
| p_p_count | int | Pattern occurrence count | 1 | ≥ 0 |
| p_products | List<Product> | Nested products (rotation variants) | null | Optional |

**Serialization:** Implements `Serializable` for deep cloning

**Business Rules:**
- If `p_is_dir = 0`, system creates rotation variant with swapped height/width
- `p_r_count` decrements as products are placed on materials
- `m_left` and `m_top` are set when product is placed on a material
- `p_is_show = 1` marks product as placed, references parent material's node_id

### 11.2 Material Model

**Class:** `com.gv.model.Material`
**Purpose:** Represents a board sheet with placed products and leftover areas

**Attributes:**

| Field | Type | Description | Example | Constraints |
|-------|------|-------------|---------|-------------|
| m_name | String | Board size name | "4 x 8 呎" | 1-20 chars |
| m_height | double | Sheet height (mm) | 2440.0 | > 0 |
| m_width | double | Sheet width (mm) | 1220.0 | > 0 |
| m_count | int | Quantity of this sheet type | 1 | ≥ 1 |
| m_weight | double | Thickness (mm) | 18.0 | > 0 |
| m_color | String | Material color/type | "白橡木" | 1-30 chars |
| r_height | double | Remaining height available | 2440.0 | ≥ 0 |
| r_width | double | Remaining width available | 1220.0 | ≥ 0 |
| m_m_left | double | X position (for sub-materials) | 0.0 | ≥ 0 |
| m_m_top | double | Y position (for sub-materials) | 0.0 | ≥ 0 |
| m_is_show | int | Processing status: 0=active, 1=processed | 0 | 0 or 1 |
| m_is_yl | int | Leftover flag: 0=primary, 1=leftover | 0 | 0 or 1 |
| m_is_dk | int | Dark key flag | 0 | 0 or 1 |
| m_is_p_info | int | Product info flag | 0 | 0 or 1 |
| m_area_used | double | Utilization ratio (0.0-1.0) | 0.823 | 0.0-1.0 |
| m_u_count | int | Batch count (identical patterns) | 3 | ≥ 1 |
| m_c_type | int | Cut type: 0=vertical, 1=horizontal | 0 | 0 or 1 |
| m_hs_type | int | Horizontal/vertical split type | 0 | 0-2 |
| m_y_is_ud | int | Leftover position: 0=left, 1=top, 2=corner | 0 | 0-2 |
| m_f_id | int | Parent material node ID | 0 | ≥ 0 |
| m_node_id | int | Current material node ID | 1 | > 0 |
| m_products | List<Product> | Products placed on this sheet | [...] | Optional |
| m_materials | List<Material> | Sub-materials (remainder areas) | [...] | Optional |
| m_y_materials | List<Material> | Leftover pieces for reuse | [...] | Optional |
| m_i_products | List<Product> | Consolidated product list | [...] | Optional |
| m_material_map | Map<String, List<Material>> | Material variants by dimensions | {...} | Optional |

**Serialization:** Implements `Serializable` for deep cloning

**Business Rules:**
- `r_height` and `r_width` represent available space after products are placed
- `m_products` contains all products placed directly on this sheet
- `m_materials` contains remainder areas that can be filled recursively
- `m_y_materials` contains leftover pieces large enough for reuse (>= 200×200mm)
- `m_area_used` = sum(product_areas) / (m_height × m_width)
- `m_u_count` > 1 indicates this pattern is repeated multiple times (batch production)
- Tree structure: `m_f_id` points to parent, `m_node_id` is unique identifier

### 11.3 Scheme Model

**Class:** `com.gv.model.Scheme`
**Purpose:** Maps products to materials (simple association)

**Attributes:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| p_no | String | Product code | "A001" |
| m_no | String | Material identifier | "Sheet_1" |
| c_type | int | Cut type/configuration | 0 |

**Usage:** Minimal usage in current implementation; appears to be legacy or future feature

### 11.4 Constant Configuration

**Class:** `com.gv.constant.Constant`
**Purpose:** Define standard board sizes available for cutting

**Static Initialization:**
```java
public class Constant {
    public static List<Material> MATERIAL_LIST = new ArrayList<Material>();

    static {
        // 5x10 呎 - 1530 x 3060 mm
        Material m1 = new Material();
        m1.setM_name("5 x 10");
        m1.setM_height(3060);
        m1.setM_width(1530);
        MATERIAL_LIST.add(m1);

        // 5x8 呎 - 1530 x 2440 mm
        Material m2 = new Material();
        m2.setM_name("5 x 8");
        m2.setM_height(2440);
        m2.setM_width(1530);
        MATERIAL_LIST.add(m2);

        // 4x8 呎 - 1220 x 2440 mm (most common)
        Material m3 = new Material();
        m3.setM_name("4 x 8");
        m3.setM_height(2440);
        m3.setM_width(1220);
        MATERIAL_LIST.add(m3);

        // Additional sizes: 5x8, 4x9, 4x10, 5x9
        // ...
    }
}
```

**Supported Board Sizes:**
1. 5×10 呎: 1530 × 3060 mm
2. 5×8 呎: 1530 × 2440 mm
3. 4×8 呎: 1220 × 2440 mm (most common)
4. 5×8 呎: 1530 × 2440 mm (duplicate entry)
5. 4×9 呎: 1220 × 2750 mm
6. 4×10 呎: 1220 × 3060 mm
7. 5×9 呎: 1530 × 2750 mm

---

## 12. Algorithm Specifications

### 12.1 Algorithm Classification

**Problem Type:** 2D Cutting Stock Problem (2D-CSP)
**Complexity:** NP-Hard
**Approach:** Greedy Heuristic with Randomized Multi-Start
**Variant:** Guillotine Cutting with Grain Direction Constraints

### 12.2 Algorithm Pseudocode

```
FUNCTION createView(products[], materials[], saw_bite, scale_threshold):
    // Phase 1: Grouping
    product_groups = processProduct(products)  // Group by color+thickness
    material_groups = processMaterial(materials)  // Group by color+thickness

    result_materials = []
    node_id = 0

    // Phase 2: Optimization per group
    FOR EACH product_group IN product_groups:
        group_key = product_group.key  // e.g., "18*白橡木"
        group_products = product_group.products
        group_materials = material_groups[group_key]

        scoreMaterial(group_materials)  // Sort: non-leftover first

        // Phase 3: Material iteration
        FOR EACH material IN group_materials:
            WHILE (group_products has unplaced items):
                scoreAreaProduct(group_products)  // Sort by area descending

                best_pattern = null
                best_utilization = 0

                // Phase 4: Multi-attempt optimization
                FOR attempt = 1 TO 6:
                    temp_material = clone(material)
                    temp_products = clone(group_products)

                    // Randomized placement
                    FOR EACH product IN temp_products:
                        IF (product.p_r_count > 0):
                            // Check fit
                            IF (material.r_height >= product.p_height + saw_bite AND
                                material.r_width >= product.p_width + saw_bite):

                                // Place product
                                place_product(temp_material, product, saw_bite)
                                product.p_r_count--

                                // Calculate remainder
                                r_height = material.r_height - product.p_height - saw_bite
                                r_width = material.r_width - product.p_width - saw_bite

                                // Try placing more products in remainder
                                IF (r_height > 60 OR r_width > 60):
                                    recursiveFill(remainder_area, temp_products, saw_bite)

                    // Evaluate utilization
                    utilization = calculate_utilization(temp_material)

                    IF (utilization > best_utilization):
                        best_pattern = temp_material
                        best_utilization = utilization

                // Phase 5: Accept pattern if above threshold
                IF (best_utilization >= scale_threshold):
                    result_materials.add(best_pattern)
                    update_product_counts(group_products, best_pattern)
                ELSE:
                    BREAK  // Cannot achieve threshold, try next material

    // Phase 6: Post-processing
    consolidatePatterns(result_materials)  // Merge identical patterns
    calculateLeftovers(result_materials)    // Identify reusable pieces

    RETURN result_materials


FUNCTION place_product(material, product, saw_bite):
    // Set product position
    product.m_left = material.m_m_left
    product.m_top = material.m_m_top

    // Add to material's product list
    material.m_products.add(product)

    // Update remaining space
    material.r_height -= (product.p_height + saw_bite)
    material.r_width -= (product.p_width + saw_bite)

    // Calculate utilization
    used_area = sum(p.p_height * p.p_width for p in material.m_products)
    total_area = material.m_height * material.m_width
    material.m_area_used = used_area / total_area


FUNCTION consolidatePatterns(materials[]):
    pattern_map = {}

    FOR EACH material IN materials:
        pattern_key = generate_pattern_key(material)

        IF (pattern_key EXISTS IN pattern_map):
            // Merge identical patterns
            pattern_map[pattern_key].m_u_count++
        ELSE:
            pattern_map[pattern_key] = material
            material.m_u_count = 1

    // Return consolidated list
    RETURN values(pattern_map)
```

### 12.3 Algorithm Parameters

| Parameter | Type | Range | Default | Impact |
|-----------|------|-------|---------|--------|
| saw_bite | double | 2-6 mm | 3 mm | Kerf loss per cut; higher = more waste |
| scale_threshold | double | 0.50-0.90 | 0.78 | Minimum utilization to accept pattern; higher = fewer boards with more waste |
| placement_attempts | int | 1-10 | 6 | Random placement tries; higher = better optimization but slower |
| min_leftover_size | double | 100-500 mm | 200 mm | Minimum dimension for reusable leftover pieces |

### 12.4 Optimization Strategies

#### 12.4.1 Product Sorting (scoreAreaProduct)
```
Sort products by area (height × width) in DESCENDING order
Rationale: Place large products first to reduce fragmentation
```

#### 12.4.2 Material Sorting (scoreMaterial)
```
Sort materials by:
1. Leftover flag (m_is_yl): 0 before 1 (primary sheets before leftovers)
2. Area: larger sheets first

Rationale: Use primary sheets first for main production,
           reserve leftovers for small/odd pieces
```

#### 12.4.3 Randomized Search
```
FOR each placement attempt:
    - Randomly choose cut direction (vertical or horizontal)
    - Use Random.nextBoolean() to decide orientation

Rationale: Explore multiple solutions to avoid local optima
Trade-off: Non-deterministic results (different runs = different outputs)
```

#### 12.4.4 Recursive Remainder Filling
```
After placing a product:
1. Calculate leftover area (L-shaped or rectangular)
2. Try placing additional products in leftover space
3. Recursively subdivide if products don't fit perfectly
4. Track leftover tree structure via m_f_id/m_node_id

Rationale: Maximize utilization by filling every usable space
```

### 12.5 Algorithm Complexity Analysis

**Time Complexity:**
- Worst case: O(P × M × A × N²)
  - P = product groups (by color+thickness)
  - M = materials available
  - A = placement attempts (default 6)
  - N = average products per group

- Typical case: O(N² × M) for single material type

**Space Complexity:**
- O(N + M) for grouping maps
- O(A × N) for deep cloning during attempts
- O(N²) for recursive remainder tree

**Performance Bottleneck:**
- Serialization-based deep cloning (60%+ of execution time)
- Nested loops (5 levels deep in worst case)
- No caching or memoization of partial solutions

### 12.6 Algorithm Limitations

1. **No Global Optimum Guarantee:**
   - Greedy approach finds local optima only
   - Randomization helps but doesn't guarantee best solution
   - Different runs may produce different results

2. **Guillotine Cuts Only:**
   - Cannot handle arbitrary polygonal shapes
   - All cuts must be straight edge-to-edge
   - Reduces flexibility for complex geometries

3. **Single Material Type:**
   - Cannot mix colors or thicknesses on same sheet
   - Separate optimization runs required for each type
   - May miss cross-material optimization opportunities

4. **Fixed Board Sizes:**
   - Only predefined sizes supported
   - No dynamic board size optimization
   - Custom sizes require code modification

5. **Computational Scalability:**
   - O(N²) complexity limits input size
   - Recommended max: 100 products per run
   - Large orders may require batch processing

---

## 13. Integration Requirements

### 13.1 Input Integration

#### 13.1.1 Web Form Input (Current)
**Endpoint:** `/GV/createView.action`
**Method:** POST
**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
```
product_no[]=A001&product_no[]=A002&...
product_name[]=侧板&product_name[]=顶板&...
product_height[]=2000&product_height[]=900&...
product_width[]=600&product_width[]=600&...
product_weight[]=18&product_weight[]=18&...
product_color[]=白橡木&product_color[]=白橡木&...
product_count[]=2&product_count[]=2&...
product_is_dir[]=1&product_is_dir[]=0&...
material_name=4 x 8
saw_bite=3
scale=0.78
```

#### 13.1.2 JSON API Input (Future Enhancement)
**Endpoint:** `/GV/api/optimize` (future)
**Method:** POST
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "products": [
    {
      "code": "A001",
      "name": "侧板",
      "length": 2000,
      "width": 600,
      "thickness": 18,
      "color": "白橡木",
      "quantity": 2,
      "grainDirection": "directional"
    }
  ],
  "boardConfig": {
    "size": "4x8",
    "sawKerf": 3,
    "utilizationThreshold": 0.78
  },
  "leftoverMaterials": [
    {
      "length": 800,
      "width": 600,
      "thickness": 18,
      "color": "白橡木",
      "quantity": 1
    }
  ]
}
```

### 13.2 Output Integration

#### 13.2.1 JSON Response (Current)
**Content-Type:** `application/json` (via struts2-json-plugin)

**Response Structure:**
```json
{
  "materials": [
    {
      "m_name": "4 x 8 呎",
      "m_height": 2440,
      "m_width": 1220,
      "m_area_used": 0.823,
      "m_u_count": 2,
      "m_products": [
        {
          "p_no": "A001",
          "p_name": "侧板",
          "p_height": 2000,
          "p_width": 600,
          "p_weight": 18,
          "p_color": "白橡木",
          "p_count": 2,
          "m_left": 0,
          "m_top": 0
        }
      ],
      "m_y_materials": [
        {
          "m_height": 840,
          "m_width": 1220,
          "m_y_is_ud": 1
        }
      ]
    }
  ],
  "statistics": {
    "totalSheets": 3,
    "averageUtilization": 0.812,
    "totalProductArea": 7350000,
    "totalWasteArea": 1650000
  }
}
```

#### 13.2.2 HTML Rendering (Current)
- JSP iterates over materials list
- Generates SVG/Canvas cutting diagrams
- Displays product and leftover tables
- Provides print button for shop floor

### 13.3 External System Integration (Future)

#### 13.3.1 ERP Integration
**Use Case:** Import orders from ERP, export cutting plans back

**Requirements:**
- Import order line items as products
- Map ERP material codes to GV color/thickness
- Export cutting plans as manufacturing orders
- Update inventory with leftover materials

**Integration Method:**
- RESTful API (JSON)
- Batch file import/export (CSV/XML)
- Database integration (MyBatis support exists but unused)

#### 13.3.2 CAD/CAM Integration
**Use Case:** Export cutting diagrams for CNC machines

**Requirements:**
- Export cutting patterns in DXF or G-code format
- Include precise coordinates and tool paths
- Support for automatic nesting in CAM software

**Integration Method:**
- File export (DXF, SVG with metadata)
- Direct machine control (future, requires hardware integration)

#### 13.3.3 Inventory Management
**Use Case:** Track leftover materials and material consumption

**Requirements:**
- Add leftover pieces to inventory after each job
- Deduct materials used from inventory
- Alert when material stock is low

**Integration Method:**
- Database integration (SQL insert/update)
- API calls to external inventory system

---

## 14. Success Metrics

### 14.1 Business Metrics

| Metric | Baseline (Manual) | Target (With GV) | Measurement Method |
|--------|-------------------|------------------|-------------------|
| Material Utilization Rate | 60-70% | ≥ 75% | Average across all jobs |
| Material Cost per Order | ¥1000 | ≤ ¥850 | Cost reduction = 15% |
| Planning Time per Order | 2-4 hours | < 5 minutes | Time from input to approved plan |
| Calculation Errors | 5-10% of orders | < 1% | Orders requiring rework due to errors |
| Leftover Reuse Rate | < 5% | ≥ 20% | Leftover material used in subsequent jobs |
| Orders Processed per Day | 5-8 | 15-20 | Production throughput |

### 14.2 Technical Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Response Time (95th percentile) | < 5 seconds | Server-side timing logs |
| Response Time (typical) | < 2 seconds | Average for 20-50 product orders |
| System Uptime | 99% | Monitoring tool (e.g., Nagios) |
| Error Rate | < 0.1% | Failed requests / total requests |
| Concurrent Users | 10 | Load testing with JMeter |
| Memory Usage per Request | < 2GB | JVM monitoring |

### 14.3 User Experience Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| User Training Time | < 10 minutes | Time to complete first optimization |
| Task Completion Rate | > 95% | Users who successfully generate cutting plan |
| User Satisfaction | ≥ 4.0/5.0 | Post-use survey |
| Print Quality Rating | ≥ 4.0/5.0 | Shop floor supervisor feedback |
| Repeat Usage Rate | > 80% | Users who use system for 2+ orders |

### 14.4 Quality Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Calculation Accuracy | 100% | Dimension validation (sum of products ≤ sheet size) |
| Utilization Consistency | < 5% std dev | Variance across similar orders |
| Leftover Accuracy | 100% | Manual verification of leftover calculations |
| Grain Direction Compliance | 100% | Directional products never rotated |

---

## 15. Constraints & Limitations

### 15.1 Technical Constraints

1. **Java 7 Compatibility:**
   - Code must compile with `-source 1.7 -target 1.7`
   - Required for Spring 3.0.6 bytecode compatibility
   - Limits use of modern Java features (lambdas, streams, etc.)

2. **Tomcat 8.5.x Dependency:**
   - Application designed for Tomcat servlet container
   - Not tested on other containers (Jetty, WildFly)
   - Requires servlet-api.jar for compilation

3. **Single-Threaded Optimization:**
   - Each request processed sequentially
   - No parallel processing of product groups
   - Limits scalability for very large orders

4. **No Database Integration:**
   - Stateless operation (no data persistence)
   - Cannot save optimization history
   - Leftover inventory not tracked between sessions

5. **Hardcoded Configuration:**
   - Board sizes defined in Constant.java (requires recompilation to change)
   - No admin interface for configuration
   - Algorithm parameters buried in code

### 15.2 Algorithm Constraints

1. **Guillotine Cuts Only:**
   - Cannot handle non-rectangular shapes
   - Cannot optimize arbitrary polygon nesting
   - Reduces flexibility for curved or irregular products

2. **2D Optimization:**
   - Does not consider 3D stacking or volumetric optimization
   - Single sheet depth only

3. **No Cross-Material Optimization:**
   - Products grouped by color+thickness must use separate sheets
   - Cannot mix materials even if it would reduce waste
   - May result in multiple sheets with low utilization

4. **Randomized Results:**
   - Different runs produce different cutting patterns
   - Not reproducible without fixing random seed
   - Difficult to compare or validate results

5. **No Optimality Guarantee:**
   - Greedy heuristic finds local optima only
   - May miss globally optimal solution
   - No approximation ratio specified

### 15.3 Business Constraints

1. **Chinese Language Only:**
   - UI and documentation in Simplified Chinese
   - Not suitable for international markets without localization

2. **Furniture Industry Focus:**
   - Designed for wood panel cutting
   - May not suit other industries (metal, glass, fabric)

3. **Manual Input Required:**
   - No automated order import
   - Requires manual data entry for each order
   - Error-prone for large orders

4. **No Cost Estimation:**
   - Does not calculate material costs
   - No pricing or quotation features
   - Requires separate tools for cost analysis

### 15.4 Operational Constraints

1. **Network Access Required:**
   - Web-based application requires server access
   - No offline mode
   - Vulnerable to network outages

2. **Print Dependency:**
   - Shop floor relies on printed cutting diagrams
   - No digital display on cutting machines
   - Paper-based workflow

3. **No User Management:**
   - No authentication or authorization
   - Anyone with access can use system
   - No audit trail of who created which plans

4. **Limited Error Recovery:**
   - If optimization fails, must restart from scratch
   - No save/resume capability
   - No undo/redo functionality

---

## 16. Future Enhancements

### 16.1 Short-Term Enhancements (3-6 months)

#### FE-001: Database Integration
**Priority:** High
**Description:** Add database to persist optimization results and leftover inventory

**Benefits:**
- Track optimization history for cost analysis
- Maintain leftover inventory across sessions
- Enable user management and audit trails

**Technical Requirements:**
- Add MySQL or PostgreSQL database
- Use MyBatis (already in dependencies) for ORM
- Create schema for: users, orders, products, materials, optimization_results

#### FE-002: CSV/Excel Import
**Priority:** High
**Description:** Allow users to upload product lists via CSV or Excel files

**Benefits:**
- Reduce manual data entry errors
- Speed up input for large orders (50+ products)
- Enable ERP integration via file export

**Technical Requirements:**
- Add Apache POI for Excel parsing
- Support CSV format (comma-separated)
- Validate and preview before optimization

#### FE-003: Saved Templates
**Priority:** Medium
**Description:** Allow users to save commonly used product configurations

**Benefits:**
- Speed up repeat orders
- Standardize common furniture designs
- Reduce training time for new users

**Technical Requirements:**
- Add template CRUD operations
- Store in database
- UI for template selection and customization

#### FE-004: Custom Board Sizes
**Priority:** Medium
**Description:** Allow users to define custom board dimensions

**Benefits:**
- Support non-standard materials
- Enable optimization for special orders
- Reduce dependency on hardcoded sizes

**Technical Requirements:**
- Add board size CRUD interface
- Store in database or configuration file
- Validate dimensions (must be > all products)

### 16.2 Medium-Term Enhancements (6-12 months)

#### FE-005: Multi-User Support
**Priority:** High
**Description:** Add user authentication, roles, and permissions

**User Roles:**
- **Planner:** Create and manage cutting plans
- **Supervisor:** View and print cutting plans
- **Admin:** Configure system, manage users, view analytics
- **Guest:** View-only access

**Technical Requirements:**
- Spring Security integration
- User management interface
- Session management
- Audit logging

#### FE-006: Analytics Dashboard
**Priority:** High
**Description:** Provide reports and analytics on material utilization

**Metrics:**
- Material utilization trends over time
- Cost savings vs. manual planning
- Most efficient product configurations
- Leftover inventory value

**Visualizations:**
- Line charts: Utilization rate by month
- Bar charts: Material consumption by product type
- Pie charts: Waste breakdown by category
- Tables: Top 10 most efficient orders

**Technical Requirements:**
- Data aggregation queries
- Chart library (D3.js, Chart.js)
- Export to PDF/Excel

#### FE-007: Improved Algorithm
**Priority:** Medium
**Description:** Replace greedy heuristic with more advanced optimization

**Approaches:**
- **Genetic Algorithm:** Evolve cutting patterns over generations
- **Simulated Annealing:** Accept worse solutions to escape local optima
- **Column Generation:** Linear programming for optimal solution
- **Machine Learning:** Learn from historical patterns

**Benefits:**
- Higher utilization rates (potentially 80-90%)
- More consistent results
- Faster optimization for large orders

**Trade-offs:**
- Increased complexity
- Longer optimization time (may need async processing)
- Requires research and testing

#### FE-008: 3D Visualization
**Priority:** Low
**Description:** Provide interactive 3D visualization of cutting plans

**Features:**
- Rotate, zoom, pan cutting diagrams
- Click products to highlight in list
- Animate cutting sequence
- Export to 3D formats (OBJ, STL)

**Technical Requirements:**
- WebGL library (Three.js)
- 3D rendering engine
- Performance optimization for large diagrams

### 16.3 Long-Term Enhancements (12+ months)

#### FE-009: CNC Machine Integration
**Priority:** Medium
**Description:** Direct integration with CNC cutting machines

**Features:**
- Export cutting patterns to G-code
- Support for multiple machine types
- Automatic tool path optimization
- Real-time machine status monitoring

**Benefits:**
- Eliminate manual programming
- Reduce cutting errors
- Increase automation
- Faster production

**Technical Requirements:**
- Hardware integration (serial/USB/network)
- G-code generation library
- Machine-specific protocols
- Safety interlocks and error handling

#### FE-010: Mobile App
**Priority:** Low
**Description:** Mobile app for shop floor supervisors

**Features:**
- View cutting plans on tablet/phone
- Scan QR codes to track products
- Report completed cuts
- Update leftover inventory

**Platforms:**
- iOS (iPhone, iPad)
- Android (phone, tablet)

**Technical Requirements:**
- Native or hybrid app (React Native, Flutter)
- RESTful API backend
- QR code scanner integration
- Offline mode for shop floor (no network)

#### FE-011: Multi-Factory Support
**Priority:** Low
**Description:** Cloud-based platform for multiple factory locations

**Features:**
- Centralized order management
- Distribute orders across factories
- Consolidated inventory management
- Cross-factory material sharing

**Technical Requirements:**
- Cloud deployment (AWS, Azure, Alibaba Cloud)
- Multi-tenant architecture
- Load balancing
- Data synchronization

#### FE-012: AI-Powered Optimization
**Priority:** Low
**Description:** Use machine learning to improve optimization over time

**Features:**
- Learn from historical cutting patterns
- Predict optimal board sizes for order types
- Suggest product design changes to reduce waste
- Automatic parameter tuning

**Technical Requirements:**
- ML framework (TensorFlow, PyTorch)
- Training data collection (historical orders)
- Model training and validation
- Integration with optimization engine

---

## 17. Dependencies

### 17.1 External Dependencies

#### 17.1.1 Runtime Dependencies (JARs)

| Library | Version | Purpose | License |
|---------|---------|---------|---------|
| Struts 2 Core | 2.3.1.2 | MVC framework | Apache 2.0 |
| Struts 2 Spring Plugin | 2.2.3.1 | Spring integration | Apache 2.0 |
| Struts 2 JSON Plugin | 2.2.3.1 | JSON output | Apache 2.0 |
| XWork Core | 2.3.1.2 | Web framework | Apache 2.0 |
| Spring Core | 3.0.6 | IoC container | Apache 2.0 |
| Spring Beans | 3.0.6 | Bean management | Apache 2.0 |
| Spring Context | 3.0.6 | Application context | Apache 2.0 |
| Spring Web | 3.0.6 | Web utilities | Apache 2.0 |
| Spring AOP | 3.0.6 | Aspect-oriented programming | Apache 2.0 |
| Spring ASM | 3.0.6 | Bytecode manipulation | Apache 2.0 |
| Spring JDBC | 3.0.6 | Database access (unused) | Apache 2.0 |
| MyBatis | 3.0.6 | ORM framework (unused) | Apache 2.0 |
| MyBatis-Spring | 1.0.2 | MyBatis integration (unused) | Apache 2.0 |
| Commons IO | 2.0.1 | File utilities | Apache 2.0 |
| Commons Lang | 2.5 | Language utilities | Apache 2.0 |
| Commons FileUpload | 1.2.2 | File upload handling | Apache 2.0 |
| Commons Logging | 1.1.x | Logging facade | Apache 2.0 |
| FreeMarker | 2.3.18 | Template engine | BSD |
| OGNL | 3.0.4 | Expression language | Apache 2.0 |
| Javassist | 3.11.0.GA | Bytecode manipulation | Apache 2.0 |
| ASM | 3.3 | Bytecode manipulation | BSD |
| Log4j | 1.2.14 | Logging | Apache 2.0 |
| MySQL Connector | 5.0.8 | MySQL JDBC driver (unused) | GPL |

#### 17.1.2 Compilation Dependencies

| Dependency | Source | Required For |
|------------|--------|--------------|
| servlet-api.jar | Tomcat 8.5.x lib/ | Servlet/JSP compilation |
| JDK 7+ | Oracle/OpenJDK | Java compilation |

#### 17.1.3 Development Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| Java Compiler (javac) | 1.7+ | Compile source code |
| JAR Tool | JDK bundled | Package WAR file |
| Bash | 4.x | Build script execution |
| CFR Decompiler | 0.152 | Source code recovery (development only) |

### 17.2 Infrastructure Dependencies

#### 17.2.1 Server Requirements

| Component | Requirement | Notes |
|-----------|-------------|-------|
| Operating System | Linux (recommended), Windows Server | Tested on Linux |
| Java Runtime | JRE 7+ (Java 8 recommended) | Must support bytecode version 51 |
| Application Server | Apache Tomcat 8.5.x | Other versions may work but untested |
| Memory | Minimum 2GB RAM | 4GB recommended for production |
| Disk Space | Minimum 100MB | For application + logs |
| CPU | 2+ cores | Single-core will work but slower |

#### 17.2.2 Client Requirements

| Component | Requirement | Notes |
|-----------|-------------|-------|
| Web Browser | Chrome 60+, Firefox 55+, IE 11+, Edge | Modern browser with JavaScript |
| Screen Resolution | Minimum 1024×768 | 1920×1080 recommended |
| Network | LAN or WAN access to server | No offline mode |
| Printer | Standard inkjet or laser | For printing cutting diagrams |

### 17.3 Integration Dependencies

#### 17.3.1 Future Database (Optional)

| Database | Version | Purpose |
|----------|---------|---------|
| MySQL | 5.6+ | Data persistence |
| PostgreSQL | 9.4+ | Alternative to MySQL |
| H2 | 1.4+ | Embedded database for testing |

**Schema Requirements:**
- Tables: users, orders, products, materials, optimization_results, leftover_inventory
- Support for UTF-8 (Chinese characters)
- Indexes for performance

#### 17.3.2 Future ERP Integration (Optional)

| System | Integration Method | Purpose |
|--------|-------------------|---------|
| SAP | RFC, Web Services | Import orders, export results |
| Oracle EBS | PL/SQL, REST API | Same as above |
| Kingdee (金蝶) | API, file import | Common in China |
| UFIDA (用友) | API, file import | Common in China |
| Custom ERP | REST API, CSV | Flexible integration |

---

## 18. Risks & Mitigation

### 18.1 Technical Risks

#### RISK-001: Algorithm Performance Degradation
**Risk Level:** High
**Description:** O(N²) algorithm may become too slow for large orders (100+ products)

**Impact:**
- User frustration with long wait times
- Timeout errors
- Server resource exhaustion

**Mitigation:**
1. **Immediate:** Set maximum product limit (100) in UI
2. **Short-term:** Optimize cloning (replace serialization with Cloneable)
3. **Medium-term:** Add async processing with progress bar
4. **Long-term:** Implement more efficient algorithm (genetic algorithm, etc.)

#### RISK-002: Bytecode Compatibility Issues
**Risk Level:** Medium
**Description:** Java version mismatch causing Spring ASM errors

**Impact:**
- Application crashes on startup or during optimization
- Unpredictable behavior

**Mitigation:**
1. **Immediate:** Document Java 7 compilation requirement
2. **Short-term:** Add automated build tests to verify bytecode version
3. **Medium-term:** Upgrade Spring to 4.x or 5.x (supports Java 8+)
4. **Long-term:** Migrate to Spring Boot with modern dependencies

#### RISK-003: Memory Leaks
**Risk Level:** Medium
**Description:** Deep cloning creates many temporary objects, potentially exhausting memory

**Impact:**
- OutOfMemoryError crashes
- Degraded performance over time
- Server instability

**Mitigation:**
1. **Immediate:** Set JVM memory limits (`-Xmx2g`)
2. **Short-term:** Add memory monitoring and alerts
3. **Medium-term:** Implement object pooling for Products/Materials
4. **Long-term:** Refactor to immutable data structures (reduce cloning)

#### RISK-004: Floating-Point Precision Errors
**Risk Level:** Low
**Description:** Accumulation of rounding errors in dimension calculations

**Impact:**
- Products may not fit on sheet despite calculations suggesting they do
- Waste calculations inaccurate by 1-2%

**Mitigation:**
1. **Immediate:** Use BigDecimal for critical calculations (already partially implemented)
2. **Short-term:** Add epsilon tolerance for comparisons
3. **Medium-term:** Switch to integer arithmetic (use millimeters as base unit)

### 18.2 Business Risks

#### RISK-005: User Resistance to Change
**Risk Level:** Medium
**Description:** Experienced planners may resist using automated system

**Impact:**
- Low adoption rate
- Continued manual planning
- ROI not realized

**Mitigation:**
1. **Immediate:** Provide hands-on training and support
2. **Short-term:** Demonstrate cost savings with pilot projects
3. **Medium-term:** Gamification (leaderboard for highest utilization)
4. **Long-term:** Make system mandatory, sunset manual process

#### RISK-006: Inaccurate Input Data
**Risk Level:** High
**Description:** Users enter incorrect product dimensions or quantities

**Impact:**
- Optimized plans don't match actual requirements
- Material shortages or excess waste
- Production delays

**Mitigation:**
1. **Immediate:** Add input validation (min/max ranges)
2. **Short-term:** Preview step before optimization (user confirms inputs)
3. **Medium-term:** Import from CAD files (reduce manual entry)
4. **Long-term:** Automated dimension verification (image recognition)

#### RISK-007: Network Outages
**Risk Level:** Medium
**Description:** Server or network downtime prevents access to optimization tool

**Impact:**
- Production planning delays
- Revert to manual process
- Missed deadlines

**Mitigation:**
1. **Immediate:** Set up server monitoring with alerts
2. **Short-term:** Document manual fallback procedure
3. **Medium-term:** High availability setup (load balancer, redundant servers)
4. **Long-term:** Offline mode (desktop application)

### 18.3 Operational Risks

#### RISK-008: Lack of Maintenance
**Risk Level:** High
**Description:** No one available to fix bugs or add features after deployment

**Impact:**
- System becomes stale and unusable
- Security vulnerabilities
- User frustration

**Mitigation:**
1. **Immediate:** Comprehensive documentation (README, PRD, code comments)
2. **Short-term:** Train internal IT staff on system architecture
3. **Medium-term:** Establish support contract with development team
4. **Long-term:** Open-source project or vendor partnership

#### RISK-009: Data Loss (No Backups)
**Risk Level:** Low (currently stateless), High (with future database)
**Description:** Server failure results in lost optimization history

**Impact:**
- Cannot retrieve previous cutting plans
- Lost leftover inventory data
- Manual re-entry required

**Mitigation:**
1. **Immediate:** N/A (stateless system, no data to lose)
2. **Short-term:** When database added, implement daily backups
3. **Medium-term:** Real-time replication to backup server
4. **Long-term:** Cloud-based storage with automatic backups

#### RISK-010: Security Vulnerabilities
**Risk Level:** Medium
**Description:** No authentication allows unauthorized access

**Impact:**
- Competitors may access proprietary designs
- Data tampering or deletion
- System abuse (DoS attacks)

**Mitigation:**
1. **Immediate:** Deploy behind firewall, restrict network access
2. **Short-term:** Add basic authentication (username/password)
3. **Medium-term:** Role-based access control
4. **Long-term:** Full security audit, penetration testing, HTTPS

---

## 19. Appendix

### 19.1 Glossary

| Term | Chinese | Definition |
|------|---------|------------|
| Board / Sheet | 板材 | Raw material panel (wood, plywood, etc.) |
| Product / Component | 产品 / 构件 | Furniture piece to be cut from board |
| Cutting Stock Problem | 下料问题 | Optimization problem of cutting items from stock material |
| Guillotine Cut | guillotine切割 | Straight edge-to-edge cut across entire sheet |
| Grain Direction | 纹理方向 | Wood grain orientation (affects appearance) |
| Directional | 单向 | Product that cannot be rotated (grain-sensitive) |
| Mixed | 混合 | Product that can be rotated 90° (grain-insensitive) |
| Utilization Rate | 利用率 | Percentage of sheet area used by products |
| Saw Kerf | 锯口 / 锯缝 | Width of material removed by saw blade |
| Leftover / Remnant | 余料 | Usable material remaining after cutting |
| Waste | 废料 | Material too small to reuse |
| Batch Consolidation | 批量合并 | Merging identical cutting patterns |
| Cutting Diagram | 开料图 | Visual layout showing product placement |
| Cutting Plan | 开料方案 | Complete optimization result |

### 19.2 Standard Board Sizes (China)

| Imperial (呎) | Metric (mm) | Common Uses |
|--------------|-------------|-------------|
| 4 × 8 呎 | 1220 × 2440 | Most common, general furniture |
| 5 × 8 呎 | 1530 × 2440 | Wider pieces, reduces waste |
| 4 × 9 呎 | 1220 × 2750 | Taller cabinets, wardrobes |
| 5 × 9 呎 | 1530 × 2750 | Large furniture |
| 4 × 10 呎 | 1220 × 3060 | Special orders, long pieces |
| 5 × 10 呎 | 1530 × 3060 | Minimize waste for large projects |

**Note:** 1 呎 (foot) = 304.8mm in metric system

### 19.3 Common Product Types

| Product Type | Chinese | Typical Dimensions | Grain Direction |
|--------------|---------|-------------------|-----------------|
| Side Panel | 侧板 | 2000×600×18 | Directional |
| Top/Bottom Panel | 顶底板 | 900×600×18 | Mixed |
| Back Panel | 背板 | 2000×900×5 | Mixed |
| Shelf | 层板 | 880×580×18 | Mixed |
| Drawer Front | 抽屉面板 | 400×200×18 | Directional |
| Cabinet Door | 柜门 | 700×400×18 | Directional |
| Divider | 隔板 | 780×580×18 | Mixed |
| Desktop | 桌面 | 1600×800×25 | Directional |

### 19.4 References

#### Industry Standards
- **GB/T 15036.1-2009:** Plywood dimensional tolerances (China)
- **GB/T 9846-2015:** Particleboard (China)
- **ISO 2848:1984:** Building construction - Modular coordination - Principles

#### Academic Papers
- Gilmore, P.C.; Gomory, R.E. (1961). "A Linear Programming Approach to the Cutting Stock Problem"
- Lodi, A.; Martello, S.; Monaci, M. (2002). "Two-dimensional packing problems: A survey"
- Wäscher, G.; Haußner, H.; Schumann, H. (2007). "An improved typology of cutting and packing problems"

#### Similar Software
- **CutList Plus** - Popular in North America
- **OptiCut** - European market
- **MaxCut** - Chinese market
- **1D/2D/3D Cutting Optimizer** - Online tools

### 19.5 Code Repository Structure

```
GV-recovered-source/
├── src/                           # Java source code
│   └── com/gv/
│       ├── action/                # Struts 2 actions (controllers)
│       │   └── ViewAction.java
│       ├── constant/              # Configuration constants
│       │   └── Constant.java
│       ├── model/                 # Domain models
│       │   ├── Material.java
│       │   ├── Product.java
│       │   └── Scheme.java
│       ├── service/               # Business logic (algorithms)
│       │   ├── ViewServiceR2.java         # Production version
│       │   ├── ViewServiceR1.java         # Legacy
│       │   ├── ViewServiceR.java          # Legacy
│       │   ├── ViewService.java           # Legacy
│       │   ├── ViewServiceN.java          # Legacy
│       │   └── ViewServiceN1.java         # Legacy
│       └── tool/                  # Utility classes
│           ├── CommonTools.java   # Deep cloning
│           └── DecimalMath.java   # Precision arithmetic
│
├── webapp/                        # Web resources
│   ├── WEB-INF/
│   │   ├── classes/
│   │   │   ├── applicationContext.xml  # Spring config
│   │   │   └── struts.xml              # Struts config
│   │   └── web.xml                     # Servlet config
│   ├── input.jsp                       # Product input page
│   ├── result.jsp                      # Cutting plan results (assumed)
│   ├── css/                            # Stylesheets
│   ├── js/                             # JavaScript
│   └── *.jpg, *.png                    # Images
│
├── lib/                           # JAR dependencies (29 files)
│
├── build.sh                       # Build script
├── deploy.sh                      # Deployment script
├── deploy-precompiled.sh          # Alternative deployment
│
├── README.md                      # Technical documentation
├── QUICKSTART.md                  # Setup guide
├── HOWTO_RUN.md                   # Running guide
├── BUILD_FIXED.txt                # Compilation fixes log
├── RECOVERY_SUMMARY.txt           # Decompilation summary
├── START_HERE.txt                 # Quick start
├── TEST_DATA.md                   # Test scenarios
└── PRD.md                         # This document
```

### 19.6 Contact Information

**Product Owner:** [To Be Determined]
**Development Team:** [To Be Determined]
**Support Contact:** [To Be Determined]

**Documentation Maintained By:** AI-Generated (Based on Source Code Analysis)
**Last Updated:** 2025-11-08

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-08 | AI Analysis | Initial PRD created from source code reverse-engineering |

---

**END OF DOCUMENT**
