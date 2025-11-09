"""
Guillotine cut tree construction and validation.

Constructs a valid sequence of guillotine cuts for a bin packing.
"""

from typing import List, Optional, Tuple
from tessellate.core.models import BinPacking, PlacedItem, Cut, CutType


class GuillotineTreeNode:
    """Node in a guillotine cutting tree."""

    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initialize a tree node representing a rectangle.

        Args:
            x: X-coordinate
            y: Y-coordinate
            width: Rectangle width
            height: Rectangle height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item: Optional[PlacedItem] = None
        self.left: Optional['GuillotineTreeNode'] = None
        self.right: Optional['GuillotineTreeNode'] = None
        self.cut: Optional[Cut] = None

    def is_leaf(self) -> bool:
        """Check if node is a leaf (contains an item)."""
        return self.left is None and self.right is None


class GuillotineTreeBuilder:
    """Build guillotine cutting trees for bin packings."""

    @staticmethod
    def build_tree(bin_packing: BinPacking, kerf: float = 3.0) -> Optional[GuillotineTreeNode]:
        """
        Build a guillotine cutting tree for a bin packing.

        This uses a simple heuristic to construct valid guillotine cuts.

        Args:
            bin_packing: Bin packing to build tree for
            kerf: Kerf width

        Returns:
            Root node of the tree, or None if construction fails
        """
        if not bin_packing.items:
            return None

        root = GuillotineTreeNode(
            0, 0,
            bin_packing.bin_type.width,
            bin_packing.bin_type.height
        )

        # Simple strategy: sort items by position and recursively partition
        items = sorted(bin_packing.items, key=lambda item: (item.y, item.x))

        success = GuillotineTreeBuilder._partition_recursive(
            root, items, kerf
        )

        if success:
            # Extract cuts from tree
            bin_packing.cuts = GuillotineTreeBuilder._extract_cuts(root)
            return root
        else:
            return None

    @staticmethod
    def _partition_recursive(
        node: GuillotineTreeNode,
        items: List[PlacedItem],
        kerf: float
    ) -> bool:
        """
        Recursively partition a rectangle with guillotine cuts.

        Args:
            node: Current node
            items: Items to fit in this node
            kerf: Kerf width

        Returns:
            True if partitioning successful
        """
        if not items:
            return True

        if len(items) == 1:
            # Leaf node - single item
            node.item = items[0]
            return True

        # Try to find a guillotine cut that separates items
        # Strategy 1: Try horizontal cut
        cut_y = GuillotineTreeBuilder._find_horizontal_cut(
            node, items, kerf
        )

        if cut_y is not None:
            # Create horizontal cut
            items_bottom = [
                item for item in items
                if item.y < cut_y
            ]
            items_top = [
                item for item in items
                if item.y >= cut_y
            ]

            if items_bottom and items_top:
                node.cut = Cut(
                    cut_type=CutType.HORIZONTAL,
                    position=cut_y,
                    start=(node.x, cut_y),
                    end=(node.x + node.width, cut_y)
                )

                node.left = GuillotineTreeNode(
                    node.x, node.y,
                    node.width, cut_y - node.y - kerf
                )
                node.right = GuillotineTreeNode(
                    node.x, cut_y,
                    node.width, node.y + node.height - cut_y
                )

                return (
                    GuillotineTreeBuilder._partition_recursive(node.left, items_bottom, kerf) and
                    GuillotineTreeBuilder._partition_recursive(node.right, items_top, kerf)
                )

        # Strategy 2: Try vertical cut
        cut_x = GuillotineTreeBuilder._find_vertical_cut(
            node, items, kerf
        )

        if cut_x is not None:
            items_left = [
                item for item in items
                if item.x < cut_x
            ]
            items_right = [
                item for item in items
                if item.x >= cut_x
            ]

            if items_left and items_right:
                node.cut = Cut(
                    cut_type=CutType.VERTICAL,
                    position=cut_x,
                    start=(cut_x, node.y),
                    end=(cut_x, node.y + node.height)
                )

                node.left = GuillotineTreeNode(
                    node.x, node.y,
                    cut_x - node.x - kerf, node.height
                )
                node.right = GuillotineTreeNode(
                    cut_x, node.y,
                    node.x + node.width - cut_x, node.height
                )

                return (
                    GuillotineTreeBuilder._partition_recursive(node.left, items_left, kerf) and
                    GuillotineTreeBuilder._partition_recursive(node.right, items_right, kerf)
                )

        # If we can't find a valid cut, return False
        # (This means the packing may not be guillotine-compatible)
        return False

    @staticmethod
    def _find_horizontal_cut(
        node: GuillotineTreeNode,
        items: List[PlacedItem],
        kerf: float
    ) -> Optional[float]:
        """Find a valid horizontal guillotine cut position."""
        # Try cutting at the top of items in the lower part
        potential_cuts = sorted(set(item.top() + kerf for item in items))

        for cut_y in potential_cuts:
            if node.y < cut_y < node.y + node.height:
                # Check if this cut cleanly separates items
                items_bottom = [item for item in items if item.top() + kerf <= cut_y]
                items_top = [item for item in items if item.y >= cut_y]

                if items_bottom and items_top and len(items_bottom) + len(items_top) == len(items):
                    return cut_y

        return None

    @staticmethod
    def _find_vertical_cut(
        node: GuillotineTreeNode,
        items: List[PlacedItem],
        kerf: float
    ) -> Optional[float]:
        """Find a valid vertical guillotine cut position."""
        # Try cutting at the right edge of items in the left part
        potential_cuts = sorted(set(item.right() + kerf for item in items))

        for cut_x in potential_cuts:
            if node.x < cut_x < node.x + node.width:
                # Check if this cut cleanly separates items
                items_left = [item for item in items if item.right() + kerf <= cut_x]
                items_right = [item for item in items if item.x >= cut_x]

                if items_left and items_right and len(items_left) + len(items_right) == len(items):
                    return cut_x

        return None

    @staticmethod
    def _extract_cuts(node: GuillotineTreeNode) -> List[Cut]:
        """Extract all cuts from the tree in order."""
        cuts = []

        if node.cut:
            cuts.append(node.cut)

        if node.left:
            cuts.extend(GuillotineTreeBuilder._extract_cuts(node.left))

        if node.right:
            cuts.extend(GuillotineTreeBuilder._extract_cuts(node.right))

        return cuts
