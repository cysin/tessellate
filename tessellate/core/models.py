"""
Core data models for the 2D Guillotine Cutting Stock Problem.

This module defines the fundamental data structures used throughout the library.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import time


class CutType(Enum):
    """Type of guillotine cut."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class Item:
    """
    Represents an item (piece) to be cut from stock.

    Attributes:
        id: Unique identifier
        width: Original width
        height: Original height
        thickness: Material thickness
        material: Material type/color
        quantity: Number of instances needed
        rotatable: Whether the item can be rotated 90°
    """
    id: str
    width: float
    height: float
    thickness: float
    material: str
    quantity: int = 1
    rotatable: bool = True

    def area(self) -> float:
        """Calculate item area."""
        return self.width * self.height

    def aspect_ratio(self) -> float:
        """Calculate aspect ratio (width/height)."""
        return self.width / self.height if self.height > 0 else float('inf')

    def __hash__(self):
        return hash(self.id)


@dataclass
class Bin:
    """
    Represents a stock bin (sheet) from which items are cut.

    Attributes:
        id: Unique identifier
        width: Bin width
        height: Bin height
        thickness: Material thickness
        material: Material type/color
        available: Number available (-1 for unlimited)
    """
    id: str
    width: float
    height: float
    thickness: float
    material: str
    available: int = -1  # -1 means unlimited

    def area(self) -> float:
        """Calculate bin area."""
        return self.width * self.height

    def __hash__(self):
        return hash(self.id)


@dataclass
class PlacedItem:
    """
    Represents an item placed in a bin.

    Attributes:
        item: Reference to the original item
        x: X-coordinate (bottom-left corner)
        y: Y-coordinate (bottom-left corner)
        width: Placed width (after rotation if applicable)
        height: Placed height (after rotation if applicable)
        rotated: Whether the item was rotated
    """
    item: Item
    x: float
    y: float
    width: float
    height: float
    rotated: bool = False

    def right(self) -> float:
        """Right edge x-coordinate."""
        return self.x + self.width

    def top(self) -> float:
        """Top edge y-coordinate."""
        return self.y + self.height

    def overlaps(self, other: 'PlacedItem', kerf: float = 0) -> bool:
        """
        Check if this item overlaps with another, accounting for kerf.

        Args:
            other: Another placed item
            kerf: Minimum spacing (blade width)

        Returns:
            True if items overlap
        """
        return not (
            self.right() + kerf <= other.x or
            other.right() + kerf <= self.x or
            self.top() + kerf <= other.y or
            other.top() + kerf <= self.y
        )


@dataclass
class Cut:
    """
    Represents a guillotine cut.

    Attributes:
        cut_type: Horizontal or vertical
        position: Position along the axis
        start: Starting point (x, y)
        end: Ending point (x, y)
    """
    cut_type: CutType
    position: float
    start: Tuple[float, float]
    end: Tuple[float, float]


@dataclass
class BinPacking:
    """
    Represents a single bin with its placed items.

    Attributes:
        bin_id: Instance identifier
        bin_type: Reference to the bin type
        items: List of placed items
        cuts: List of guillotine cuts (optional)
    """
    bin_id: int
    bin_type: Bin
    items: List[PlacedItem] = field(default_factory=list)
    cuts: List[Cut] = field(default_factory=list)

    def utilization(self) -> float:
        """Calculate bin utilization percentage."""
        if not self.items:
            return 0.0
        used_area = sum(item.width * item.height for item in self.items)
        total_area = self.bin_type.area()
        return used_area / total_area if total_area > 0 else 0.0

    def is_valid(self, kerf: float = 0) -> bool:
        """
        Check if placement is valid (no overlaps, within boundaries).

        Args:
            kerf: Minimum spacing between items

        Returns:
            True if valid
        """
        # Check boundaries
        for item in self.items:
            if item.x < 0 or item.y < 0:
                return False
            if item.right() > self.bin_type.width:
                return False
            if item.top() > self.bin_type.height:
                return False

        # Check overlaps
        for i, item1 in enumerate(self.items):
            for item2 in self.items[i + 1:]:
                if item1.overlaps(item2, kerf):
                    return False

        return True


@dataclass
class Solution:
    """
    Complete solution to a cutting stock problem.

    Attributes:
        bins: List of bin packings
        unplaced: List of items that couldn't be placed
        metadata: Solution metrics and information
    """
    bins: List[BinPacking] = field(default_factory=list)
    unplaced: List[Tuple[Item, int]] = field(default_factory=list)  # (item, quantity)
    metadata: Dict = field(default_factory=dict)

    def num_bins(self) -> int:
        """Number of bins used."""
        return len(self.bins)

    def total_utilization(self) -> float:
        """Overall utilization across all bins."""
        if not self.bins:
            return 0.0
        return sum(bp.utilization() for bp in self.bins) / len(self.bins)

    def is_complete(self) -> bool:
        """Check if all items were placed."""
        return len(self.unplaced) == 0

    def objective_value(self) -> int:
        """Primary objective: number of bins used."""
        return self.num_bins()

    def _group_identical_bins(self) -> List[Dict]:
        """
        Group identical bins together for aggregated output.

        Bins are considered identical if they have:
        - Same board specifications (material, thickness, dimensions)
        - Same cutting layout: items with same dimensions, material, and positions

        Note: Item ID/name is NOT considered - parts with identical dimensions
        and material are treated as the same for cutting purposes.

        Returns:
            List of groups, each with {"bins": [...], "quantity": N}
        """
        from collections import defaultdict

        groups_map = defaultdict(list)

        for bp in self.bins:
            # Create signature for this bin
            # Include board spec
            board_sig = f"{bp.bin_type.material}-{bp.bin_type.thickness}-{bp.bin_type.width}-{bp.bin_type.height}"

            # Include items layout (sorted for consistency)
            # NOTE: For cutting purposes, only dimensions, material, and position matter
            # Do NOT use item.id - parts with same dimensions/material are identical for cutting
            items_sig = tuple(sorted([
                (pi.x, pi.y, pi.width, pi.height, pi.item.thickness, pi.item.material, pi.rotated)
                for pi in bp.items
            ]))

            signature = (board_sig, items_sig)
            groups_map[signature].append(bp)

        # Convert to list format
        return [
            {"bins": bins, "quantity": len(bins)}
            for bins in groups_map.values()
        ]

    def _format_bin_group(self, group: Dict) -> dict:
        """
        Format a bin group for JSON output.

        Collects all item IDs across all boards in the group to show
        complete parts list even when different parts have same dimensions.

        Args:
            group: Dictionary with "bins" and "quantity" keys

        Returns:
            Formatted bin group dictionary
        """
        from collections import defaultdict

        representative_bin = group["bins"][0]

        # Collect all items across all boards in this group
        # Key: (x, y, width, height, rotated, material, thickness)
        # Value: list of item IDs at this position across all boards
        items_by_position = defaultdict(list)

        for bp in group["bins"]:
            for pi in bp.items:
                key = (pi.x, pi.y, pi.width, pi.height, pi.rotated, pi.item.material, pi.item.thickness)
                items_by_position[key].append(pi.item.id)

        # Format items: one entry per unique position with all item IDs
        items_list = []
        for (x, y, width, height, rotated, material, thickness), item_ids in items_by_position.items():
            # Get all unique item IDs at this position
            unique_ids = list(set(item_ids))

            # Create one entry for each unique ID at this position
            for item_id in unique_ids:
                count = item_ids.count(item_id)
                items_list.append({
                    "itemId": item_id,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "rotated": rotated,
                    "material": material,
                    "thickness": thickness,
                    "count": count  # How many boards have this item at this position
                })

        return {
            "binId": representative_bin.bin_id,
            "binType": representative_bin.bin_type.id,
            "width": representative_bin.bin_type.width,
            "height": representative_bin.bin_type.height,
            "thickness": representative_bin.bin_type.thickness,
            "material": representative_bin.bin_type.material,
            "utilization": sum(bp.utilization() for bp in group["bins"]) / len(group["bins"]),
            "quantity": group["quantity"],
            "items": items_list,
            "cuts": [
                {
                    "type": cut.cut_type.value,
                    "position": cut.position,
                    "start": {"x": cut.start[0], "y": cut.start[1]},
                    "end": {"x": cut.end[0], "y": cut.end[1]},
                }
                for cut in representative_bin.cuts
            ],
        }

    def to_dict(self) -> dict:
        """Convert solution to dictionary format (JSON-serializable)."""
        # Group identical bins
        bin_groups = self._group_identical_bins()

        return {
            "metadata": {
                "objectiveValue": self.num_bins(),
                "utilization": self.total_utilization(),
                "executionTime": self.metadata.get("execution_time", 0),
                "algorithmName": self.metadata.get("algorithm", "Unknown"),
                "binsUsed": self.num_bins(),
                "isComplete": self.is_complete(),
            },
            "bins": [
                self._format_bin_group(group)
                for group in bin_groups
            ],
            "unplaced": [
                {
                    "itemId": item.id,
                    "quantity": qty,
                }
                for item, qty in self.unplaced
            ],
        }


@dataclass
class Problem:
    """
    Complete problem specification.

    Attributes:
        items: List of items to pack
        bins: List of available bin types
        kerf: Kerf width (blade thickness)
        utilization_threshold: Minimum acceptable utilization
        time_limit: Maximum execution time in seconds
    """
    items: List[Item]
    bins: List[Bin]
    kerf: float = 3.0
    utilization_threshold: float = 0.78
    time_limit: float = 5.0

    @classmethod
    def from_dict(cls, data: dict) -> 'Problem':
        """
        Create Problem from dictionary (JSON) format.

        Args:
            data: Dictionary with items, bins, and parameters

        Returns:
            Problem instance
        """
        items = [
            Item(
                id=item_data["id"],
                width=float(item_data["width"]),
                height=float(item_data["height"]),
                thickness=float(item_data["thickness"]),
                material=item_data["material"],
                quantity=int(item_data["quantity"]),
                rotatable=bool(item_data.get("rotatable", True)),
            )
            for item_data in data["items"]
        ]

        bins = [
            Bin(
                id=bin_data["id"],
                width=float(bin_data["width"]),
                height=float(bin_data["height"]),
                thickness=float(bin_data["thickness"]),
                material=bin_data["material"],
                available=int(bin_data.get("available", -1)),
            )
            for bin_data in data["bins"]
        ]

        params = data.get("parameters", {})

        return cls(
            items=items,
            bins=bins,
            kerf=float(params.get("kerf", 3.0)),
            utilization_threshold=float(params.get("utilizationThreshold", 0.78)),
            time_limit=float(params.get("timeLimit", 5.0)),
        )

    def group_by_material(self) -> Dict[Tuple[float, str], List[Item]]:
        """
        Group items by thickness and material.

        Returns:
            Dictionary mapping (thickness, material) to list of items
        """
        groups = {}
        for item in self.items:
            key = (item.thickness, item.material)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups

    def get_compatible_bins(self, item: Item) -> List[Bin]:
        """
        Get bins compatible with an item.

        A bin is compatible if:
        1. Material matches the item's material (boards can only have one material)
        2. Thickness matches the item's thickness
        3. Physical dimensions are large enough (in either orientation)

        Args:
            item: Item to check

        Returns:
            List of compatible bins (matching material/thickness and large enough)
        """
        return [
            bin_type
            for bin_type in self.bins
            if (bin_type.material == item.material and
                bin_type.thickness == item.thickness and
                # Item can fit in either orientation
                ((bin_type.width >= item.width and bin_type.height >= item.height) or
                 (bin_type.width >= item.height and bin_type.height >= item.width)))
        ]
