# GV Application - Test Data

## Test Scenario 1: Simple Wardrobe (衣柜)

### Product Components (家具构件开料明细)

| 编号 (Code) | 名称 (Name) | 长 (Length) | 宽 (Width) | 厚 (Thickness) | 花色 (Color) | 数量 (Qty) | 纹理 (Grain) |
|------------|------------|------------|-----------|---------------|-------------|-----------|-------------|
| A001 | 侧板 (Side Panel) | 2000 | 600 | 18 | 白橡木 (White Oak) | 2 | 单向 (Directional) |
| A002 | 顶底板 (Top/Bottom) | 900 | 600 | 18 | 白橡木 (White Oak) | 2 | 混合 (Mixed) |
| A003 | 背板 (Back Panel) | 2000 | 900 | 5 | 白橡木 (White Oak) | 1 | 混合 (Mixed) |
| A004 | 层板 (Shelf) | 880 | 580 | 18 | 白橡木 (White Oak) | 3 | 混合 (Mixed) |
| A005 | 抽屉面板 (Drawer Front) | 400 | 200 | 18 | 白橡木 (White Oak) | 3 | 单向 (Directional) |

### Board Configuration (板材配置)
- **Board Size (板材规格)**: 4 x 8 呎 (1220 x 2440 mm)
- **Thickness (厚度)**: 18mm (for main components)
- **Saw Kerf (锯口尺寸)**: 3 mm
- **Utilization Rate (板材利用率)**: 0.78 (78%)

---

## Test Scenario 2: Kitchen Cabinet (橱柜)

### Product Components

| 编号 | 名称 | 长 | 宽 | 厚 | 花色 | 数量 | 纹理 |
|-----|------|----|----|----|----|------|------|
| B001 | 柜门 (Cabinet Door) | 700 | 400 | 18 | 樱桃木 (Cherry) | 4 | 单向 |
| B002 | 侧板 (Side Panel) | 800 | 600 | 18 | 樱桃木 (Cherry) | 4 | 单向 |
| B003 | 台面板 (Countertop) | 2400 | 600 | 25 | 樱桃木 (Cherry) | 1 | 混合 |
| B004 | 隔板 (Divider) | 780 | 580 | 18 | 樱桃木 (Cherry) | 6 | 混合 |
| B005 | 抽屉侧板 (Drawer Side) | 500 | 120 | 12 | 樱桃木 (Cherry) | 8 | 混合 |

### Board Configuration
- **Board Size**: 5 x 8 呎 (1530 x 2440 mm)
- **Saw Kerf**: 3 mm
- **Utilization Rate**: 0.75

---

## Test Scenario 3: Bookshelf (书架) - With Leftover Material

### Product Components

| 编号 | 名称 | 长 | 宽 | 厚 | 花色 | 数量 | 纹理 |
|-----|------|----|----|----|----|------|------|
| C001 | 竖板 (Vertical Panel) | 1800 | 250 | 18 | 胡桃木 (Walnut) | 4 | 单向 |
| C002 | 层板 (Shelf) | 900 | 250 | 18 | 胡桃木 (Walnut) | 5 | 混合 |
| C003 | 顶板 (Top Panel) | 920 | 300 | 18 | 胡桃木 (Walnut) | 1 | 混合 |
| C004 | 底板 (Bottom Panel) | 920 | 300 | 18 | 胡桃木 (Walnut) | 1 | 混合 |
| C005 | 背板槽 (Back Groove) | 1780 | 50 | 12 | 胡桃木 (Walnut) | 2 | 混合 |

### Leftover Material (库存余料) - Optional
Check the "库存余料优先" checkbox and add:

| 长 | 宽 | 厚 | 花色 | 数量 |
|----|----|----|----|------|
| 800 | 600 | 18 | 胡桃木 | 1 |
| 500 | 400 | 18 | 胡桃木 | 2 |

### Board Configuration
- **Board Size**: 4 x 8 呎 (1220 x 2440 mm)
- **Saw Kerf**: 3 mm
- **Utilization Rate**: 0.78

---

## Test Scenario 4: Office Desk (办公桌)

### Product Components

| 编号 | 名称 | 长 | 宽 | 厚 | 花色 | 数量 | 纹理 |
|-----|------|----|----|----|----|------|------|
| D001 | 桌面 (Desktop) | 1600 | 800 | 25 | 黑胡桃 (Black Walnut) | 1 | 单向 |
| D002 | 桌腿侧板 (Leg Side) | 720 | 600 | 18 | 黑胡桃 (Black Walnut) | 4 | 单向 |
| D003 | 抽屉面板 (Drawer Front) | 500 | 120 | 18 | 黑胡桃 (Black Walnut) | 3 | 单向 |
| D004 | 抽屉侧板 (Drawer Side) | 450 | 120 | 12 | 黑胡桃 (Black Walnut) | 6 | 混合 |
| D005 | 抽屉底板 (Drawer Bottom) | 480 | 430 | 5 | 黑胡桃 (Black Walnut) | 3 | 混合 |

### Board Configuration
- **Board Size**: 5 x 9 呎 (1530 x 2750 mm)
- **Saw Kerf**: 3 mm
- **Utilization Rate**: 0.80

---

## Test Scenario 5: Small Test (快速测试)

For quick testing, use this minimal dataset:

| 编号 | 名称 | 长 | 宽 | 厚 | 花色 | 数量 | 纹理 |
|-----|------|----|----|----|----|------|------|
| T001 | 板材A | 800 | 400 | 18 | 白色 | 4 | 混合 |
| T002 | 板材B | 600 | 300 | 18 | 白色 | 6 | 混合 |
| T003 | 板材C | 400 | 200 | 18 | 白色 | 8 | 混合 |

### Board Configuration
- **Board Size**: 4 x 8 呎 (1220 x 2440 mm)
- **Saw Kerf**: 3 mm
- **Utilization Rate**: 0.75

---

## How to Use This Test Data

### Step 1: Access the Application
Open: http://localhost:8089/GV/input.jsp

### Step 2: Enter Product Data
For each product row, click "添加" (Add) button to add new rows, then fill in:
- **编号** (Code): Product code (e.g., A001)
- **名称** (Name): Product name (e.g., 侧板)
- **长** (Length): Length in mm (e.g., 2000)
- **宽** (Width): Width in mm (e.g., 600)
- **厚** (Thickness): Thickness in mm (e.g., 18)
- **花色** (Color): Wood color/pattern (e.g., 白橡木)
- **数量** (Quantity): Number of pieces (e.g., 2)
- **纹理方向** (Grain): Select 单向 (directional) or 混合 (mixed)

### Step 3: Configure Board Settings
- **板材规格** (Board Size): Select from dropdown (4×8, 5×8, etc.)
- **裁切锯口尺寸** (Saw Kerf): Enter 3 (mm)
- **板材利用率** (Utilization): Enter 0.78 (or 0.75, 0.80)

### Step 4: Optional - Add Leftover Material
1. Check the "库存余料优先" checkbox
2. Add leftover pieces with their dimensions

### Step 5: Generate Cutting Plan
1. Click "确认完成" (Confirm Complete) button
2. Then click "确认开板" (Generate Cutting Plan) button

### Step 6: View Results
The system will show:
- Visual cutting diagrams showing how products are placed on boards
- List of products with quantities
- Leftover material summary
- Material utilization statistics
- Print option for cutting instructions

---

## Expected Results

### Scenario 1 (Simple Wardrobe)
- **Expected boards needed**: 2-3 boards
- **Estimated utilization**: 75-85%
- **Leftover pieces**: Several small pieces suitable for future use

### Scenario 2 (Kitchen Cabinet)
- **Expected boards needed**: 3-4 boards (due to 25mm countertop)
- **Estimated utilization**: 70-80%
- **Note**: Different thicknesses may require separate boards

### Scenario 3 (Bookshelf with Leftover)
- **Expected boards needed**: 2-3 boards
- **Estimated utilization**: 80-90% (higher due to leftover usage)
- **Leftover reuse**: System prioritizes using existing leftover material first

### Scenario 4 (Office Desk)
- **Expected boards needed**: 2-3 boards (larger board size helps)
- **Estimated utilization**: 75-85%
- **Note**: Large desktop piece may affect overall efficiency

### Scenario 5 (Small Test)
- **Expected boards needed**: 1-2 boards
- **Estimated utilization**: 80-90%
- **Processing time**: < 5 seconds (fast for testing)

---

## Tips for Testing

1. **Start with Scenario 5** (Small Test) to understand the interface
2. **Try different board sizes** to see optimization differences
3. **Adjust saw kerf** (2-5mm) to see impact on material usage
4. **Change utilization threshold** to balance efficiency vs. complexity
5. **Test grain direction** - 单向 prevents rotation, 混合 allows rotation
6. **Use leftover material** to see how system prioritizes existing stock

---

## Common Board Sizes in China

| Size | Metric (mm) | Common Use |
|------|------------|-----------|
| 4 x 8 呎 | 1220 x 2440 | Most common, general furniture |
| 5 x 8 呎 | 1530 x 2440 | Wider pieces, less waste |
| 4 x 9 呎 | 1220 x 2750 | Longer pieces |
| 5 x 9 呎 | 1530 x 2750 | Large furniture |
| 4 x 10 呎 | 1220 x 3060 | Special orders |
| 5 x 10 呎 | 1530 x 3060 | Minimal waste for large projects |

---

## Troubleshooting Test Data

**Issue**: No results or error message
- Check that all dimensions are numeric (no letters)
- Ensure product codes are unique
- Verify quantities are greater than 0

**Issue**: Low utilization rate
- Try different board sizes
- Adjust utilization threshold lower (e.g., 0.70)
- Mix directional and non-directional pieces

**Issue**: Too many boards used
- Increase utilization threshold
- Use larger board sizes
- Consider allowing more grain rotation (混合)

---

## Save Your Results

After generating the cutting plan:
1. Click the **打印** (Print) button to save/print cutting instructions
2. Take screenshots of the visual diagrams
3. Note the material utilization percentage
4. Save leftover piece information for future use

---

**Ready to test!** Start with Scenario 5 for a quick test, then try the more complex scenarios.
