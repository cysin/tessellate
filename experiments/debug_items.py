"""Debug item dimensions"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from tessellate.core.models import Item
from collections import defaultdict

# Read test data
df = pd.read_excel('../test_data/bench/manual1.xlsx')

items = []
for _, row in df.iterrows():
    item = Item(
        id=row['Code'],
        width=float(row['Width']),
        height=float(row['Height']),
        thickness=float(row['Thickness']),
        material=row['Color'],
        quantity=int(row['Qty']),
        rotatable=(row['Grain'] == 'mixed')
    )
    items.append(item)

print("Item details:")
print(f"{'Code':<10} {'Width':>8} {'Height':>8} {'Qty':>5} {'Rotatable':<10}")
print("-" * 60)
for item in items:
    print(f"{item.id:<10} {item.width:>8.0f} {item.height:>8.0f} {item.quantity:>5} {str(item.rotatable):<10}")

print()
print("Width groups (grouping by height as per current algorithm):")
width_groups = defaultdict(list)
for item in items:
    for _ in range(item.quantity):
        width_groups[item.height].append(item)

for width, group_items in sorted(width_groups.items(), reverse=True):
    print(f"  Width {width}: {len(group_items)} pieces")

print()
print("Height groups (grouping by width):")
height_groups = defaultdict(list)
for item in items:
    for _ in range(item.quantity):
        height_groups[item.width].append(item)

for height, group_items in sorted(height_groups.items(), reverse=True):
    print(f"  Height {height}: {len(group_items)} pieces")
