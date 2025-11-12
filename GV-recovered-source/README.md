# GV Application - Recovered Source Code

## Overview

**GV (开板系统)** is a Board/Panel Cutting Optimization System for furniture manufacturing. It calculates optimal cutting patterns to minimize material waste when cutting furniture components from standard board sizes.

**Recovery Date**: 2025-11-08
**Original Deployment**: Apache Tomcat 8.5.57
**Decompiler Used**: CFR 0.152

---

## Application Purpose

This application solves the **2D Cutting Stock Problem** (also known as 2D Bin Packing):
- **Input**: Furniture component specifications (dimensions, quantities, colors, grain direction)
- **Process**: Optimizes placement on standard board sizes (4×8, 5×8, 4×9, 5×9, 4×10, 5×10 feet)
- **Output**: Visual cutting diagrams with product placement, leftover material tracking, and utilization statistics

---

## Directory Structure

```
GV-recovered-source/
├── src/                          # Decompiled Java source code
│   ├── com/gv/
│   │   ├── action/              # Struts 2 Controllers
│   │   │   └── ViewAction.java      (Entry point)
│   │   ├── service/             # Business Logic / Algorithms
│   │   │   ├── ViewServiceR2.java   (Main optimization algorithm - ACTIVE)
│   │   │   ├── ViewService.java
│   │   │   ├── ViewServiceR.java
│   │   │   ├── ViewServiceN.java
│   │   │   └── 9 other variants    (Experimental implementations)
│   │   ├── model/               # Data Models
│   │   │   ├── Product.java        (Furniture component)
│   │   │   ├── Material.java       (Board/panel)
│   │   │   └── Scheme.java         (Cutting scheme)
│   │   ├── tool/                # Utilities
│   │   │   ├── CommonTools.java
│   │   │   └── DecimalMath.java
│   │   └── constant/
│   │       └── Constant.java       (Board size constants)
│   └── [Test classes]
│       ├── T.java
│       ├── CreatTest.java
│       ├── CreatViewA.java
│       └── ProAndMat.java
│
└── webapp/                       # Web resources
    ├── WEB-INF/
    │   ├── web.xml                  (Servlet configuration)
    │   └── classes/
    │       ├── struts.xml           (Struts action mapping)
    │       └── applicationContext.xml (Spring config)
    ├── input.jsp                    (Main UI - 1400+ lines)
    ├── css/                         (Stylesheets)
    └── js/                          (JavaScript)
```

---

## Technology Stack

### Backend
- **Java** (JRE 7+)
- **Struts 2.3.x** - MVC framework
- **Spring 3.0.6** - Dependency injection (minimal usage, mostly commented out)
- **MyBatis 3.0.6** - ORM (database config commented out - runs in-memory)

### Frontend
- **JSP** - Server-side rendering
- **JavaScript / jQuery 1.7.2** - Client-side interactivity
- **HTML/CSS** - UI layout

### Libraries
- FreeMarker 2.3.18 (templating)
- Log4j 1.2.14 (logging)
- Commons IO, Lang, FileUpload
- OGNL 3.0.4 (expression language)
- MySQL Connector 5.0.8 (unused in this version)

---

## Core Components

### 1. Data Models

#### **Product.java** (`src/com/gv/model/Product.java`)
Represents a furniture component to be cut:
- `p_no` - Product code (unique identifier)
- `p_name` - Product name
- `p_height`, `p_width`, `p_weight` - Dimensions (length, width, thickness in mm)
- `p_color` - Surface color/pattern
- `p_count` - Quantity needed
- `p_is_dir` - Grain direction constraint (1=directional, 0=bidirectional)
- `m_left`, `m_top` - Placement coordinates on board (calculated)

#### **Material.java** (`src/com/gv/model/Material.java`)
Represents a board/panel:
- `m_name` - Board size designation
- `m_height`, `m_width`, `m_weight` - Dimensions (mm) and thickness
- `m_color` - Surface color/pattern
- `m_products` - List of products placed on this board
- `m_y_materials` - List of leftover material regions
- `m_u_count` - Number of boards used
- `m_area_used` - Total area utilized
- `r_height`, `r_width` - Remaining usable dimensions
- `m_is_yl` - Flag indicating leftover material (1=yes)

### 2. Controller Layer

#### **ViewAction.java** (`src/com/gv/action/ViewAction.java`)
Main Struts 2 action handling optimization requests:

**Key Method**: `createView()` (line 177)
1. Parses comma-separated product specifications from form
2. Creates Product objects with bidirectional grain support
3. Parses optional leftover material inventory
4. Groups products by thickness and color
5. Calls `ViewServiceR2.createView()` for optimization
6. Returns JSON result with cutting plans

### 3. Service Layer (Optimization Algorithms)

#### **ViewServiceR2.java** (`src/com/gv/service/ViewServiceR2.java`) ⭐ ACTIVE
The main optimization algorithm (Recursive variant 2):

**Algorithm Overview**:
- Uses a **First-Fit Decreasing (FFD)** heuristic
- Sorts products by area (largest first)
- Tries multiple random placement attempts
- Recursively fills boards using guillotine cutting patterns
- Tracks leftover regions for reuse
- Filters results by utilization threshold

**Key Methods**:
- `createView(products, materials, saw_bite, scale)` - Main entry point
- `scoreAreaProduct()` - Sorts products by area
- `scoreMaterial()` - Scores and ranks available boards
- `processProduct()` - Groups products by specs
- `processMaterial()` - Groups materials by specs

#### Other Service Implementations
- `ViewService.java` - Original algorithm
- `ViewServiceR.java` - Recursive variant 1
- `ViewServiceN.java` - Alternative heuristic
- `ViewServiceR1.java`, `ViewServiceN1.java` - Further iterations
- Various "CopyOf" versions - Development snapshots

### 4. Utility Classes

#### **CommonTools.java** (`src/com/gv/tool/CommonTools.java`)
- `clonePro()` - Deep copy Product objects
- `cloneMatList()` - Deep copy Material lists
- Helper methods for object manipulation

#### **DecimalMath.java** (`src/com/gv/tool/DecimalMath.java`)
High-precision decimal arithmetic for area calculations

#### **Constant.java** (`src/com/gv/constant/Constant.java`)
Defines standard board sizes:
- 4×8 呎: 1220 × 2440 mm
- 5×8 呎: 1530 × 2440 mm
- 4×9 呎: 1220 × 2750 mm
- 5×9 呎: 1530 × 2750 mm
- 4×10 呎: 1220 × 3060 mm
- 5×10 呎: 1530 × 3060 mm

---

## Configuration

### Struts Configuration (`webapp/WEB-INF/classes/struts.xml`)
```xml
<package name="json" extends="json-default">
    <action name="createView"
            class="com.gv.action.ViewAction"
            method="createView">
        <result type="json">
            <param name="root">materials</param>
        </result>
    </action>
</package>
```

### Web Configuration (`webapp/WEB-INF/web.xml`)
- Entry point: `input.jsp`
- Struts 2 filter mapped to `/*`
- Spring ContextLoaderListener enabled

### Spring Configuration (`webapp/WEB-INF/classes/applicationContext.xml`)
**Note**: Database configuration is **commented out**. This version runs without database persistence.

---

## User Interface

### Main Page (`webapp/input.jsp`)

**Sections**:

1. **Product Input Table** (家具构件开料明细)
   - Dynamic rows for adding multiple products
   - Fields: Code, Name, Length, Width, Thickness, Color, Quantity, Grain Direction
   - Validation: All dimensions must be numeric, codes must be unique

2. **Leftover Material Input** (库存余料优先)
   - Optional checkbox to enable leftover material
   - Fields: Length, Width, Thickness, Color, Quantity

3. **Board Configuration**
   - Board size dropdown (4×8, 5×8, etc.)
   - Saw kerf size (cutting blade width, default: 3mm)
   - Utilization threshold (default: 0.78 = 78%)

4. **Output Display**
   - Visual cutting diagrams (SVG-like DIV layout)
   - Product placement with coordinates
   - Leftover material regions (patterned background)
   - Material summary table
   - Print functionality

**Technologies**:
- jQuery 1.7.2 for dynamic row management
- AJAX POST to `createView.action`
- JSON response processing
- Dynamic HTML generation for cutting diagrams

---

## Algorithm Details

### Problem Classification
**2D Cutting Stock Problem** - NP-Hard complexity

### Heuristic Used
**First-Fit Decreasing with Guillotine Cuts**:
1. Sort products by area (descending)
2. For each board type:
   - Try to place largest product
   - Make guillotine cut (straight line through board)
   - Recursively pack remaining regions
   - Track leftover pieces
3. Attempt multiple random orderings
4. Select best result above utilization threshold

### Key Optimizations
- **Pre-sorting**: Products sorted by area
- **Material scoring**: Boards ranked by suitability
- **Leftover reuse**: Small boards from previous cuts reused
- **Grain direction**: Bidirectional products duplicated with rotated dimensions
- **Saw kerf compensation**: Blade width added to all dimensions
- **Multi-attempt**: 6 randomized placements per iteration

### Constraints
- Minimum leftover size: 60mm × 60mm (smaller pieces discarded)
- Saw kerf: User-configurable (typically 3mm)
- Utilization threshold: 0-1 (filters inefficient layouts)
- Maximum products per diagram: 12

---

## Building and Running

### Prerequisites
```bash
Java JDK 7 or higher
Apache Tomcat 8.5.x
Maven or Ant (for compilation)
```

### Compilation
```bash
# From src/ directory
javac -cp "path/to/tomcat/lib/*:path/to/struts-libs/*:path/to/spring-libs/*" \
      -d ../build \
      com/gv/**/*.java

# Or use an IDE like IntelliJ IDEA / Eclipse
```

### Dependencies Required
```
struts2-core-2.3.x.jar
spring-context-3.0.6.jar
spring-beans-3.0.6.jar
commons-lang-2.5.jar
commons-io-2.0.1.jar
log4j-1.2.14.jar
ognl-3.0.4.jar
javassist-3.11.0.jar
freemarker-2.3.18.jar
```

### Deployment
1. Compile all Java sources
2. Create WAR structure:
   ```
   GV.war
   ├── WEB-INF/
   │   ├── classes/
   │   │   └── com/gv/**/*.class
   │   ├── lib/ (all dependencies)
   │   └── web.xml
   ├── input.jsp
   ├── css/
   └── js/
   ```
3. Deploy to Tomcat `webapps/` directory
4. Access: `http://localhost:8080/GV/input.jsp`

---

## Known Issues

### Decompilation Artifacts
1. **Variable names**: May not match originals (e.g., `m_m_no`, `t_flag`)
2. **Comments**: Original comments lost during compilation
3. **Formatting**: Code style may differ from original

### Code Quality
1. **Magic numbers**: Many hard-coded values (60, 6, 1000000)
2. **Chinese strings**: Debug messages in Chinese (escaped Unicode)
3. **Multiple algorithm copies**: Suggests iterative development without cleanup
4. **No unit tests**: Test classes present but incomplete

### Security Concerns
1. **Old frameworks**: Struts 2.3.x has known vulnerabilities
2. **No input sanitization**: SQL injection risk (if DB enabled)
3. **Hardcoded credentials**: Check if any exist in commented code

---

## Usage Example

### Input
```
Products:
- Code: A001, Name: Door Panel, Size: 2000×600×18mm, Color: White Oak, Qty: 4
- Code: A002, Name: Shelf, Size: 800×400×18mm, Color: White Oak, Qty: 8

Board: 4×8呎 (1220×2440mm), Thickness: 18mm
Saw Kerf: 3mm
Utilization: 78%
```

### Process
1. System creates bidirectional variants (doors can't rotate, shelves can)
2. Sorts by area: Doors (1.2m²) → Shelves (0.32m²)
3. Attempts to fit 4 doors + 8 shelves on minimum boards
4. Calculates saw kerf loss
5. Generates cutting diagram

### Output
```
Board 1 (1220×2440mm):
- 2× Door Panels (2000×600)
- 6× Shelves (400×800, rotated)
- Leftover: 1× 1220×434mm

Board 2 (1220×2440mm):
- 2× Door Panels (2000×600)
- 2× Shelves (800×400)
- Leftover: 1× 1220×434mm

Total: 2 boards, 85% utilization
```

---

## Further Development

### Recommended Improvements
1. **Upgrade frameworks**: Migrate to Struts 2.5+ or Spring MVC
2. **Add database**: Persist cutting plans and material inventory
3. **Optimize algorithm**: Implement genetic algorithm or simulated annealing
4. **Unit tests**: Add comprehensive test coverage
5. **API documentation**: Generate Javadoc
6. **Internationalization**: Extract Chinese strings to properties files
7. **Modern UI**: Replace JSP with React/Vue.js frontend

### Research References
- "Cutting and Packing Problems" - Wäscher et al. (2007)
- "Two-Dimensional Bin Packing Problems" - Lodi et al. (2002)
- "Guillotine Cutting Stock Problem" - Gilmore & Gomory (1965)

---

## License

**Note**: Original license information not found in decompiled code. Verify with original developers before redistribution.

---

## Credits

**Recovered by**: Source code recovery using CFR decompiler
**Original Developers**: Unknown (check version control if available)
**Related Systems**: Part of manufacturing ERP ecosystem (DataCenter, DesignOLN2)

---

## Contact

For questions about the recovered source code or the decompilation process, refer to the original Apache Tomcat deployment at:
`/home/star/work/apache-tomcat-8.5.57/webapps/GV/`
