from itertools import permutations

from .models import Box


def get_orientations(dimensions):
    return list(set(permutations(dimensions)))


def can_pack_products(products, box):
    box_dimensions = (
        float(box.internal_length),
        float(box.internal_width),
        float(box.internal_height),
    )

    products = sorted(
        products,
        key=lambda product: (
            float(product.length)
            * float(product.width)
            * float(product.height)
        ),
        reverse=True,
    )

    placed_products = []

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

            if (
                length > box_dimensions[0]
                or width > box_dimensions[1]
                or height > box_dimensions[2]
            ):
                continue

            if not placed_products:
                placed_products.append(
                    (length, width, height, 0, 0, 0)
                )
                placed = True
                break

            for _, _, _, x, y, z in placed_products:
                positions = [
                    (x + length, y, z),
                    (x, y + width, z),
                    (x, y, z + height),
                ]

                for px, py, pz in positions:
                    if (
                        px + length <= box_dimensions[0]
                        and py + width <= box_dimensions[1]
                        and pz + height <= box_dimensions[2]
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
                                px + length <= placed_x
                                or placed_x + placed_length <= px
                                or py + width <= placed_y
                                or placed_y + placed_width <= py
                                or pz + height <= placed_z
                                or placed_z + placed_height <= pz
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
            return False

    return True


def calculate_total_weight(order):
    total_weight = 0

    for item in order.items.select_related("product"):
        total_weight += float(item.product.weight) * item.quantity

    return total_weight


def recommend_box(order):
    items = order.items.select_related("product").all()

    if not items:
        return None

    total_weight = calculate_total_weight(order)
    valid_boxes = []

    products = []

    for item in items:
        products.extend([item.product] * item.quantity)

    for box in Box.objects.all():
        if total_weight > float(box.max_weight):
            continue

        if can_pack_products(products, box):
            valid_boxes.append(box)

    if not valid_boxes:
        return None

    return min(valid_boxes, key=lambda box: float(box.cost))