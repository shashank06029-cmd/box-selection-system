from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Box, Order, Product
from .services import calculate_total_weight, recommend_box


class ProductModelTests(TestCase):
    """Tests for Product model validation."""

    def test_product_rejects_zero_dimensions(self):
        """Test that products cannot have zero dimensions."""
        product = Product(
            name="Invalid Product",
            length=0,
            width=5,
            height=2,
            weight=1,
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_rejects_negative_weight(self):
        """Test that products cannot have negative weight."""
        product = Product(
            name="Invalid Product",
            length=10,
            width=5,
            height=2,
            weight=-1,
        )
        with self.assertRaises(ValidationError):
            product.full_clean()


class BoxRecommendationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.laptop = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=5,
            weight=2,
        )

        self.mouse = Product.objects.create(
            name="Mouse",
            length=10,
            width=6,
            height=4,
            weight=0.2,
        )

        self.small_box = Box.objects.create(
            name="Small Box",
            internal_length=25,
            internal_width=20,
            internal_height=10,
            max_weight=3,
            cost=30,
        )

        self.medium_box = Box.objects.create(
            name="Medium Box",
            internal_length=35,
            internal_width=25,
            internal_height=15,
            max_weight=5,
            cost=50,
        )

        self.large_box = Box.objects.create(
            name="Large Box",
            internal_length=50,
            internal_width=40,
            internal_height=30,
            max_weight=10,
            cost=80,
        )

    def test_single_product_recommendation(self):
        order = Order.objects.create()
        order.items.create(
            product=self.laptop,
            quantity=1,
        )

        box = recommend_box(order)

        self.assertEqual(box, self.medium_box)

    def test_multiple_products_recommendation(self):
        order = Order.objects.create()
        order.items.create(
            product=self.laptop,
            quantity=1,
        )
        order.items.create(
            product=self.mouse,
            quantity=1,
        )

        box = recommend_box(order)

        self.assertEqual(box, self.medium_box)

    def test_quantity_weight_calculation(self):
        order = Order.objects.create()
        order.items.create(
            product=self.laptop,
            quantity=2,
        )

        total_weight = calculate_total_weight(order)

        self.assertEqual(total_weight, 4.0)

    def test_multiple_quantity_recommendation(self):
        order = Order.objects.create()
        order.items.create(
            product=self.mouse,
            quantity=4,
        )

        box = recommend_box(order)

        self.assertEqual(box, self.small_box)

    def test_no_suitable_box(self):
        oversized_product = Product.objects.create(
            name="Oversized TV",
            length=100,
            width=100,
            height=100,
            weight=20,
        )

        order = Order.objects.create()
        order.items.create(
            product=oversized_product,
            quantity=1,
        )

        box = recommend_box(order)

        self.assertIsNone(box)

    def test_empty_order(self):
        order = Order.objects.create()

        box = recommend_box(order)

        self.assertIsNone(box)

    def test_lowest_cost_valid_box_is_selected(self):
        order = Order.objects.create()
        order.items.create(
            product=self.mouse,
            quantity=1,
        )

        box = recommend_box(order)

        self.assertEqual(box, self.small_box)

    def test_api_rejects_empty_items(self):
        response = self.client.post(
            "/api/recommend-box/",
            {"items": []},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_api_rejects_zero_quantity(self):
        response = self.client.post(
            "/api/recommend-box/",
            {
                "items": [
                    {
                        "product": self.laptop.id,
                        "quantity": 0,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_api_rejects_invalid_product(self):
        response = self.client.post(
            "/api/recommend-box/",
            {
                "items": [
                    {
                        "product": 9999,
                        "quantity": 1,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_product_rotation(self):
        rotated_product = Product.objects.create(
            name="Rotated Product",
            length=20,
            width=25,
            height=5,
            weight=1,
        )

        order = Order.objects.create()
        order.items.create(
            product=rotated_product,
            quantity=1,
        )

        box = recommend_box(order)

        self.assertEqual(box, self.small_box)