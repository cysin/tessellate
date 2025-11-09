# 🚀 Quick Start Guide

## Installation & Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run a quick test
python tests/test_realistic.py
```

## Running the Web Application

### Option 1: Using Startup Scripts (Easiest)

**Linux/Mac:**
```bash
cd webapp
./start.sh
```

**Windows:**
```batch
cd webapp
start.bat
```

The scripts automatically:
- Create virtual environment
- Install dependencies
- Start the server

### Option 2: Manual Setup

```bash
# Navigate to webapp directory
cd webapp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py

# Open your browser
# Navigate to: http://localhost:5000
```

## Using the Library in Your Code

```python
from tessellate import solve

# Define your cutting problem
problem = {
    "items": [
        {
            "id": "Door",
            "width": 600,
            "height": 2000,
            "thickness": 18,
            "material": "Oak",
            "quantity": 2,
            "rotatable": False  # Grain direction matters
        },
        {
            "id": "Shelf",
            "width": 800,
            "height": 400,
            "thickness": 18,
            "material": "Oak",
            "quantity": 4,
            "rotatable": True  # Can rotate
        }
    ],
    "bins": [
        {
            "id": "Standard Sheet",
            "width": 1220,
            "height": 2440,
            "thickness": 18,
            "material": "Oak",
            "available": -1  # Unlimited
        }
    ],
    "parameters": {
        "kerf": 3.0,  # Blade width in mm
        "utilizationThreshold": 0.75,  # Minimum 75% utilization
        "timeLimit": 5.0  # Max 5 seconds
    }
}

# Solve the problem
solution = solve(problem)

# Print results
print(f"Bins needed: {solution['metadata']['objectiveValue']}")
print(f"Utilization: {solution['metadata']['utilization']:.1%}")
print(f"Time taken: {solution['metadata']['executionTime']:.2f}s")

# Access each bin
for bin in solution['bins']:
    print(f"\nBin {bin['binId']+1}: {bin['utilization']:.1%} full")
    for item in bin['items']:
        print(f"  - {item['itemId']} at ({item['x']}, {item['y']})")
```

## Example Output

```
Bins needed: 2
Utilization: 82.3%
Time taken: 0.12s

Bin 1: 85.1% full
  - Door at (0, 0)
  - Door at (603, 0)

Bin 2: 79.5% full
  - Shelf at (0, 0)
  - Shelf at (0, 403)
  - Shelf at (0, 806)
  - Shelf at (0, 1209)
```

## Web Interface Features

1. **Load Example**: Click to load a sample problem
2. **Edit JSON**: Modify the problem specification
3. **Solve**: Click to get the optimal cutting plan
4. **Visualize**: See the cutting layout with SVG rendering
5. **Metrics**: View bins used, utilization, and execution time

## Problem Specification Tips

### Item Dimensions
- Specify in millimeters (or any consistent unit)
- Width and height from the item's perspective
- Set `rotatable: false` for items with grain direction

### Bin Availability
- Use `-1` for unlimited bins
- Use a positive number for limited stock

### Parameters
- **kerf**: Blade thickness (typically 3-6mm for saws)
- **utilizationThreshold**: Minimum acceptable utilization (0.75-0.85)
- **timeLimit**: Maximum computation time in seconds

## Common Use Cases

### Furniture Manufacturing
```json
{
  "items": [
    {"id": "Cabinet Door", "width": 600, "height": 2000, "rotatable": false},
    {"id": "Shelf", "width": 900, "height": 400, "rotatable": true}
  ]
}
```

### Sheet Metal Cutting
```json
{
  "parameters": {
    "kerf": 1.5,  // Laser cutter kerf
    "utilizationThreshold": 0.85
  }
}
```

### Glass Cutting
```json
{
  "parameters": {
    "kerf": 0.5,  // Diamond blade
    "timeLimit": 10.0  // More time for precision
  }
}
```

## Performance Tips

- Group items by material to reduce problem complexity
- Sort items from largest to smallest for better packing
- Use reasonable time limits (5s for most problems)
- Higher utilization thresholds may require more bins

## Next Steps

- Read the full [README_TESSELLATE.md](README_TESSELLATE.md) for complete documentation
- Check [RESEARCH_PROBLEM_STANDALONE.md](RESEARCH_PROBLEM_STANDALONE.md) for the research background
- Explore benchmark instances in `benchmarks/`
- Run all tests: `pytest tests/`

## Support

For questions or issues:
1. Check the documentation
2. Review example problems in `benchmarks/`
3. Run tests to verify installation
4. Review the research problem specification

---

**Happy Optimizing! 🎯**
