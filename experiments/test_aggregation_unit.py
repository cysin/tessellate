#!/usr/bin/env python3
"""Direct unit test of _group_identical_bins() method."""

import sys
sys.path.insert(0, '/home/user/tessellate')

from tessellate.core.models import Solution, BinPacking, Bin, Item, PlacedItem

print("=" * 80)
print("UNIT TEST: _group_identical_bins()")
print("=" * 80)

# Create test data: 3 bins, 2 of which are identical
bin_type = Bin(
    id="Board-HS00-16mm",
    width=2440,
    height=1220,
    thickness=16,
    material="HS00",
    available=-1
)

item1 = Item(id="PART-A", width=600, height=400, thickness=16, material="HS00", quantity=1, rotatable=False)
item2 = Item(id="PART-B", width=600, height=400, thickness=16, material="HS00", quantity=1, rotatable=False)

# Board 1: PART-A at (0,0) + PART-B at (603.5, 0)
bp1 = BinPacking(
    bin_id=0,
    bin_type=bin_type,
    items=[
        PlacedItem(item=item1, x=0, y=0, width=600, height=400, rotated=False),
        PlacedItem(item=item2, x=603.5, y=0, width=600, height=400, rotated=False)
    ]
)

# Board 2: IDENTICAL to Board 1
bp2 = BinPacking(
    bin_id=1,
    bin_type=bin_type,
    items=[
        PlacedItem(item=item1, x=0, y=0, width=600, height=400, rotated=False),
        PlacedItem(item=item2, x=603.5, y=0, width=600, height=400, rotated=False)
    ]
)

# Board 3: DIFFERENT (only PART-A)
bp3 = BinPacking(
    bin_id=2,
    bin_type=bin_type,
    items=[
        PlacedItem(item=item1, x=0, y=0, width=600, height=400, rotated=False)
    ]
)

# Create solution
solution = Solution(bins=[bp1, bp2, bp3])

print("\nTest Setup:")
print("  - 3 boards total")
print("  - Board 1: PART-A at (0,0) + PART-B at (603.5,0)")
print("  - Board 2: PART-A at (0,0) + PART-B at (603.5,0)  [IDENTICAL to Board 1]")
print("  - Board 3: PART-A at (0,0)  [DIFFERENT]")
print("\nExpected Result:")
print("  - 2 groups:")
print("    * Group 1: quantity=2 (Board 1 + Board 2)")
print("    * Group 2: quantity=1 (Board 3)")

print("\n" + "=" * 80)
print("RUNNING _group_identical_bins()...")
print("=" * 80)

groups = solution._group_identical_bins()

print(f"\nResult: {len(groups)} group(s)")

for i, group in enumerate(groups, 1):
    print(f"\nGroup {i}:")
    print(f"  Quantity: {group['quantity']}")
    print(f"  Bins: {[bp.bin_id for bp in group['bins']]}")
    print(f"  Items on first board:")
    for item in group['bins'][0].items:
        print(f"    - {item.item.id} at ({item.x}, {item.y})")

print("\n" + "=" * 80)
print("VERIFICATION:")
print("=" * 80)

# Verify
if len(groups) == 2:
    print("✅ PASS: Got 2 groups (correct)")

    # Find the group with quantity=2
    qty2_group = [g for g in groups if g['quantity'] == 2]
    qty1_group = [g for g in groups if g['quantity'] == 1]

    if len(qty2_group) == 1 and len(qty1_group) == 1:
        print("✅ PASS: One group has quantity=2, one has quantity=1")

        # Verify the right boards are grouped
        grouped_ids = set([bp.bin_id for bp in qty2_group[0]['bins']])
        if grouped_ids == {0, 1}:
            print("✅ PASS: Boards 0 and 1 are grouped together (correct)")
        else:
            print(f"❌ FAIL: Wrong boards grouped: {grouped_ids}")

        single_id = qty1_group[0]['bins'][0].bin_id
        if single_id == 2:
            print("✅ PASS: Board 2 is in its own group (correct)")
        else:
            print(f"❌ FAIL: Wrong board in single group: {single_id}")

        print("\n✅✅✅ ALL UNIT TESTS PASSED ✅✅✅")
    else:
        print(f"❌ FAIL: Wrong quantity distribution: {[g['quantity'] for g in groups]}")
else:
    print(f"❌ FAIL: Got {len(groups)} groups, expected 2")

print("=" * 80)

# Now test the full to_dict() output
print("\n" + "=" * 80)
print("TESTING to_dict() OUTPUT:")
print("=" * 80)

result = solution.to_dict()

print(f"\nBins in to_dict() output: {len(result['bins'])}")

for i, bin_data in enumerate(result['bins'], 1):
    print(f"\nBin Group {i}:")
    print(f"  Quantity: {bin_data.get('quantity', '?')}")
    print(f"  Items: {len(bin_data['items'])}")

print("\n" + "=" * 80)
if len(result['bins']) == 2:
    quantities = [b.get('quantity', 1) for b in result['bins']]
    if 2 in quantities and 1 in quantities:
        print("✅ to_dict() CORRECTLY RETURNS AGGREGATED DATA")
    else:
        print(f"❌ to_dict() has wrong quantities: {quantities}")
else:
    print(f"❌ to_dict() returns {len(result['bins'])} bins, expected 2")
print("=" * 80)
