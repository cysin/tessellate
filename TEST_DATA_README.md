# Test Data Generation

This directory contains tools for generating realistic test data for the wardrobe cutting plan webapp.

## Components Data

`components_data.csv` contains 312 wardrobe components with the following format:

```
NAME,CODE
柜体侧板（L）,CB(L)-HS00-2434-574-16
```

### CODE Format

The CODE field follows this pattern: `PREFIX-COLOR-WIDTH-HEIGHT-THICK`

Example: `CB(L)-HS00-2434-574-16`
- PREFIX: `CB(L)` (Cabinet Board Left)
- COLOR: `HS00`
- WIDTH: `2434` mm
- HEIGHT: `574` mm
- THICK: `16` mm

## Test Data Generator

`generate_test_data.py` creates realistic wardrobe orders from the components data.

### Usage

```bash
python generate_test_data.py <number_of_files>
```

### Examples

Generate 5 test files:
```bash
python generate_test_data.py 5
```

Generate 10 test files:
```bash
python generate_test_data.py 10
```

### Output

Files are created in `test_data/` directory:
- `wardrobe_order_001.xlsx`
- `wardrobe_order_002.xlsx`
- `wardrobe_order_003.xlsx`
- etc.

### Realistic Order Simulation

The script simulates realistic wardrobe orders by:

1. **Side Panels** - Typically 2 pieces (left and right)
2. **Top/Bottom Panels** - 2-4 pieces (single or double door units)
3. **Shelves** - 3-8 pieces with varying quantities
4. **Back Panels** - 1-2 pieces
5. **Doors** - 1-4 pieces
6. **Drawers** - 0-4 sets (optional)
7. **Other Components** - 2-5 miscellaneous items

### Grain Direction

The script intelligently assigns grain orientation:
- **Fixed** - Side panels and doors (vertical grain matters)
- **Mixed or Fixed** - Shelves and back panels (can vary)

### Component Categories

The 312 components are categorized as:
- 侧板 (Side Panels): 2 items
- 顶底板 (Top/Bottom Panels): 12 items
- 层隔板 (Shelves): 20 items
- 背板 (Back Panels): 64 items
- 门板 (Doors): 64 items
- 抽屉 (Drawers): 54 items
- 其他 (Others): 96 items

## Testing the Webapp

1. Generate test files:
   ```bash
   python generate_test_data.py 5
   ```

2. Start the webapp:
   ```bash
   cd webapp
   source venv/bin/activate
   python app.py
   ```

3. Open http://localhost:5000

4. Upload one of the generated `.xlsx` files from `test_data/` directory

5. Click "Generate Cutting Plan"

## File Format

Generated files are compatible with the webapp's Excel upload format:

| Name | Code | Width | Height | Thickness | Color | Qty | Grain |
|------|------|-------|--------|-----------|-------|-----|-------|
| 柜体侧板（L） | CB(L)-HS00-2434-574-16 | 2434 | 574 | 16 | HS00 | 1 | fixed |

All dimensions are in millimeters.
