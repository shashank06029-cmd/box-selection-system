"""
Box Selection System - Data Models

Defines the core entities for the shipping box recommendation system:
- Product: Items to be shipped with dimensions and weight
- Box: Shipping containers with capacity constraints
- Order: Customer orders containing multiple products
- OrderItem: Individual products within an order
"""

import logging

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

logger = logging.getLogger(__name__)


def validate_positive_value(value):
    """Validate that a value is positive."""
    if value <= 0:
        raise ValidationError(
            "%(value)s must be greater than zero.",
            params={"value": value},
        )


class Product(models.Model):
    """
    Represents a product that can be shipped.
    
    Attributes:
        name: Product name/description
        length: Product length in cm
        width: Product width in cm
        height: Product height in cm
        weight: Product weight in kg
    """
    name = models.CharField(max_length=200)

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Product length in centimeters"
    )
    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Product width in centimeters"
    )
    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Product height in centimeters"
    )

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Product weight in kilograms"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        """Validate product dimensions and weight."""
        super().clean()
        if self.length <= 0 or self.width <= 0 or self.height <= 0:
            raise ValidationError(
                "All dimensions must be greater than zero."
            )
        if self.weight <= 0:
            raise ValidationError("Weight must be greater than zero.")

    def volume(self):
        """
        Calculate the volume of the product.
        
        Returns:
            float: Volume in cubic centimeters
        """
        return float(self.length) * float(self.width) * float(self.height)


class Box(models.Model):
    """
    Represents a shipping box with capacity constraints.
    
    Attributes:
        name: Box name/description
        internal_length: Internal length in cm
        internal_width: Internal width in cm
        internal_height: Internal height in cm
        max_weight: Maximum weight capacity in kg
        cost: Cost of using this box
    """
    name = models.CharField(max_length=200)

    internal_length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Internal length in centimeters"
    )
    internal_width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Internal width in centimeters"
    )
    internal_height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Internal height in centimeters"
    )

    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Maximum weight capacity in kilograms"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Cost of using this box"
    )

    class Meta:
        verbose_name = "Box"
        verbose_name_plural = "Boxes"
        ordering = ["cost"]

    def __str__(self):
        return self.name

    def clean(self):
        """Validate box dimensions and capacity."""
        super().clean()
        if (self.internal_length <= 0 or 
            self.internal_width <= 0 or 
            self.internal_height <= 0):
            raise ValidationError(
                "All internal dimensions must be greater than zero."
            )
        if self.max_weight <= 0:
            raise ValidationError("Max weight must be greater than zero.")
        if self.cost <= 0:
            raise ValidationError("Cost must be greater than zero.")

    def internal_volume(self):
        """
        Calculate the internal volume of the box.
        
        Returns:
            float: Internal volume in cubic centimeters
        """
        return (
            float(self.internal_length) * 
            float(self.internal_width) * 
            float(self.internal_height)
        )


class Order(models.Model):
    """
    Represents a customer order containing multiple products.
    
    Attributes:
        created_at: Timestamp when the order was created
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """
    Represents a single item within an order.
    
    Attributes:
        order: The parent order
        product: The product being ordered
        quantity: Number of units ordered
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        db_index=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_index=True
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ["order", "product"]
        indexes = [
            models.Index(fields=["order", "product"]),
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def clean(self):
        """Validate order item."""
        super().clean()
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")