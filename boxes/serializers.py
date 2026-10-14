"""
Box Selection System - API Serializers

Handles data validation and serialization for:
- Product data
- Order creation and retrieval
- Order items
"""

import logging

from rest_framework import serializers

from .models import Order, OrderItem, Product

logger = logging.getLogger(__name__)


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    
    Includes all product fields with proper validation.
    """

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "length",
            "width",
            "height",
            "weight",
        ]
        read_only_fields = ["id"]

    def validate_length(self, value):
        """Validate product length is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Length must be greater than zero."
            )
        return value

    def validate_width(self, value):
        """Validate product width is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Width must be greater than zero."
            )
        return value

    def validate_height(self, value):
        """Validate product height is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Height must be greater than zero."
            )
        return value

    def validate_weight(self, value):
        """Validate product weight is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Weight must be greater than zero."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    
    Handles nested order item creation with product validation.
    """
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def validate_product(self, value):
        """Validate that the product exists and is active."""
        if not value:
            raise serializers.ValidationError(
                "Product must be selected."
            )
        return value

    def validate_quantity(self, value):
        """Validate that quantity is positive."""
        if value < 1:
            raise serializers.ValidationError(
                "Quantity must be at least 1."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model with nested items.
    
    Handles creation of orders with multiple products.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "items"]
        read_only_fields = ["id", "created_at"]

    def validate_items(self, value):
        """Validate that order has at least one item."""
        if not value or len(value) == 0:
            raise serializers.ValidationError(
                "At least one product is required."
            )
        return value

    def create(self, validated_data):
        """
        Create an order with nested items.
        
        Args:
            validated_data: Validated order and item data
            
        Returns:
            Created Order instance
        """
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                **item_data
            )

        logger.info(f"Created order {order.id} with {len(items_data)} items")
        return order