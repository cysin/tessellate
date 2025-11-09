"""Geometric utility functions for rectangle packing."""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Rectangle:
    """Simple rectangle representation."""
    x: float
    y: float
    width: float
    height: float

    def right(self) -> float:
        return self.x + self.width

    def top(self) -> float:
        return self.y + self.height

    def area(self) -> float:
        return self.width * self.height

    def contains_point(self, px: float, py: float) -> bool:
        """Check if point is inside rectangle."""
        return self.x <= px < self.right() and self.y <= py < self.top()

    def intersects(self, other: 'Rectangle') -> bool:
        """Check if this rectangle intersects with another."""
        return not (
            self.right() <= other.x or
            other.right() <= self.x or
            self.top() <= other.y or
            other.top() <= self.y
        )


def find_maximal_rectangles(
    bin_width: float,
    bin_height: float,
    placed: List[Rectangle],
    kerf: float = 0
) -> List[Rectangle]:
    """
    Find all maximal free rectangles in a bin.

    This implements the Maximal Rectangles algorithm.

    Args:
        bin_width: Width of the bin
        bin_height: Height of the bin
        placed: List of already placed rectangles
        kerf: Minimum spacing around placed items

    Returns:
        List of maximal free rectangles
    """
    if not placed:
        return [Rectangle(0, 0, bin_width, bin_height)]

    # Start with full bin
    free_rects = [Rectangle(0, 0, bin_width, bin_height)]

    # Subtract each placed rectangle (with kerf)
    for rect in placed:
        # Expand rect by kerf
        expanded = Rectangle(
            max(0, rect.x - kerf),
            max(0, rect.y - kerf),
            rect.width + 2 * kerf,
            rect.height + 2 * kerf
        )

        new_free_rects = []
        for free_rect in free_rects:
            # Split free_rect by subtracting expanded
            splits = split_rectangle(free_rect, expanded)
            new_free_rects.extend(splits)

        free_rects = new_free_rects

    # Remove non-maximal rectangles
    free_rects = remove_redundant_rectangles(free_rects)

    return free_rects


def split_rectangle(free_rect: Rectangle, placed_rect: Rectangle) -> List[Rectangle]:
    """
    Split a free rectangle by subtracting a placed rectangle.

    Args:
        free_rect: The free rectangle
        placed_rect: The placed rectangle to subtract

    Returns:
        List of resulting free rectangles (0-4 rectangles)
    """
    if not free_rect.intersects(placed_rect):
        return [free_rect]

    result = []

    # Left split
    if placed_rect.x > free_rect.x:
        result.append(Rectangle(
            free_rect.x,
            free_rect.y,
            placed_rect.x - free_rect.x,
            free_rect.height
        ))

    # Right split
    if placed_rect.right() < free_rect.right():
        result.append(Rectangle(
            placed_rect.right(),
            free_rect.y,
            free_rect.right() - placed_rect.right(),
            free_rect.height
        ))

    # Bottom split
    if placed_rect.y > free_rect.y:
        result.append(Rectangle(
            free_rect.x,
            free_rect.y,
            free_rect.width,
            placed_rect.y - free_rect.y
        ))

    # Top split
    if placed_rect.top() < free_rect.top():
        result.append(Rectangle(
            free_rect.x,
            placed_rect.top(),
            free_rect.width,
            free_rect.top() - placed_rect.top()
        ))

    return result


def remove_redundant_rectangles(rectangles: List[Rectangle]) -> List[Rectangle]:
    """
    Remove rectangles that are contained in other rectangles.

    Args:
        rectangles: List of rectangles

    Returns:
        List with redundant rectangles removed
    """
    result = []
    for i, rect1 in enumerate(rectangles):
        is_redundant = False
        for j, rect2 in enumerate(rectangles):
            if i != j and contains(rect2, rect1):
                is_redundant = True
                break
        if not is_redundant:
            result.append(rect1)
    return result


def contains(outer: Rectangle, inner: Rectangle) -> bool:
    """Check if outer rectangle completely contains inner rectangle."""
    return (
        outer.x <= inner.x and
        outer.y <= inner.y and
        outer.right() >= inner.right() and
        outer.top() >= inner.top()
    )


def can_fit(rect: Rectangle, item_width: float, item_height: float) -> bool:
    """Check if an item can fit in a rectangle."""
    return rect.width >= item_width and rect.height >= item_height
