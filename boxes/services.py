"""
Box Selection System - Core Services

Provides the business logic for box recommendation:
- Packing algorithm to determine if products fit in a box
- Weight calculation for orders
- Box recommendation based on constraints
"""

import logging
from itertools import permutations
from typing import Any, List, Optional, Tuple

from .models import Box, Order, Product

logger = logging.getLogger(__name__)

# Packing tolerance to account for floating-point precision
PACKING_TOLERANCE = 0.01


def get_orientations(dimensions: Tuple[float, float, float]) -> List[Tuple[float, float, float]]:
    """
    Generate all unique orientations for a product.
    
    Args:
        dimensions: Tuple of (length, width, height)
        
    Returns:
        List of unique dimension permutations representing orientations
    """
    return list(set(permutations(dimensions)))


def can_pack_products(
    products: List[Product], 
    box: Box,
    tolerance: float = PACKING_TOLERANCE
) -> bool:
    """
    Determine if a list of products can be packed into a box.
    
    Uses a 3D bin packing algorithm with rotation support.
    Products are sorted by volume (largest first) for better packing efficiency.
    
    Args:
        products: List of products to pack
        box: The box to pack into
        tolerance: Tolerance for floating-point comparisons
        
    Returns:
        True if all products can be packed, False otherwise
    """
    try:
        box_dimensions = (
            float(box.internal_length),
            float(box.internal_width),
            float(box.internal_height),
        )

        # Sort products by volume (largest first) for better packing
        products = sorted(
            products,
            key=lambda product: product.volume(),
            reverse=True,
        )

        placed_products: List[Tuple[float, float, float, float, float, float]] = []

        for product in products:
            product_orientations = get_orientations(
                (
                    float(product.length),
                    float(product.width),
                    float(product.height),
                )
            )

            placed = False

            for orientation in product_orientations:
                length, width, height = orientation

                # Check if orientation fits in box dimensions
                if (
                    length > box_dimensions[0] + tolerance
                    or width > box_dimensions[1] + tolerance
                    or height > box_dimensions[2] + tolerance
                ):
                    continue

                if not placed_products:
                    placed_products.append(
                        (length, width, height, 0, 0, 0)
                    )
                    placed = True
                    break

                # Try to place product at various positions
                for _, _, _, x, y, z in placed_products:
                    positions = [
                        (x + length, y, z),
                        (x, y + width, z),
                        (x, y, z + height),
                    ]

                    for px, py, pz in positions:
                        if (
                            px + length <= box_dimensions[0] + tolerance
                            and py + width <= box_dimensions[1] + tolerance
                            and pz + height <= box_dimensions[2] + tolerance
                        ):
                            overlap = False

                            for (
                                placed_length,
                                placed_width,
                                placed_height,
                                placed_x,
                                placed_y,
                                placed_z,
                            ) in placed_products:
                                if not (
                                    px + length <= placed_x + tolerance
                                    or placed_x + placed_length <= px + tolerance
                                    or py + width <= placed_y + tolerance
                                    or placed_y + placed_width <= py + tolerance
                                    or pz + height <= placed_z + tolerance
                                    or placed_z + placed_height <= pz + tolerance
                                ):
                                    overlap = True
                                    break

                            if not overlap:
                                placed_products.append(
                                    (
                                        length,
                                        width,
                                        height,
                                        px,
                                        py,
                                        pz,
                                    )
                                )
                                placed = True
                                break

                    if placed:
                        break

                if placed:
                    break

            if not placed:
                logger.debug(
                    f"Failed to pack product {product.name} into box {box.name}"
                )
                return False

        logger.debug(f"Successfully packed {len(products)} products into {box.name}")
        return True

    except Exception as e:
        logger.error(f"Error in packing algorithm: {e}")
        return False


def calculate_total_weight(order: Order) -> float:
    """
    Calculate the total weight of all items in an order.
    
    Args:
        order: The order to calculate weight for
        
    Returns:
        Total weight in kilograms
    """
    try:
        total_weight = 0.0

        for item in order.items.select_related("product"):
            item_weight = float(item.product.weight) * item.quantity
            total_weight += item_weight

        logger.debug(f"Order {order.id} total weight: {total_weight} kg")
        return total_weight

    except Exception as e:
        logger.error(f"Error calculating weight for order {order.id}: {e}")
        raise


def recommend_box(order: Order) -> Optional[Box]:
    """
    Recommend the most cost-effective box for an order.
    
    Algorithm:
    1. Calculate total weight of all items
    2. Filter boxes by weight capacity
    3. Test packing products into each valid box
    4. Return the cheapest box that can contain all products
    
    Args:
        order: The order to find a box for
        
    Returns:
        The most cost-effective box, or None if no suitable box exists
    """
    try:
        items = order.items.select_related("product").all()

        if not items:
            logger.warning(f"Order {order.id} has no items")
            return None

        total_weight = calculate_total_weight(order)
        valid_boxes: List[Box] = []

        # Collect all products with quantities
        products: List[Product] = []
        for item in items:
            products.extend([item.product] * item.quantity)

        logger.info(
            f"Checking {len(products)} products ({total_weight} kg) against available boxes"
        )

        # Use prefetch_related for better query performance
        all_boxes = Box.objects.all()
        
        for box in all_boxes:
            # Quick weight check first
            if total_weight > float(box.max_weight) + PACKING_TOLERANCE:
                logger.debug(
                    f"Box {box.name} rejected: weight {total_weight} > {box.max_weight}"
                )
                continue

            # Detailed packing check
            if can_pack_products(products, box):
                valid_boxes.append(box)
                logger.debug(f"Box {box.name} is valid for this order")

        if not valid_boxes:
            logger.warning(
                f"No suitable box found for order {order.id} "
                f"({len(products)} products, {total_weight} kg)"
            )
            return None

        # Select the cheapest valid box
        recommended_box = min(valid_boxes, key=lambda box: float(box.cost))
        logger.info(
            f"Recommended box {recommended_box.name} (cost: {recommended_box.cost}) "
            f"for order {order.id}"
        )
        return recommended_box

    except Exception as e:
        logger.error(f"Error recommending box for order {order.id}: {e}")
        return None