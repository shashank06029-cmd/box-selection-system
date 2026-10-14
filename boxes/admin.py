"""
Box Selection System - Django Admin Configuration

Provides admin interface for managing:
- Products
- Shipping boxes
- Orders
- Order items
"""

from django.contrib import admin

from .models import Box, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = [
        "name",
        "dimensions",
        "weight",
        "volume",
    ]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["name"]

    @admin.display(description="Dimensions (L×W×H)")
    def dimensions(self, obj):
        """Display product dimensions in a readable format."""
        return f"{obj.length} × {obj.width} × {obj.height} cm"

    @admin.display(description="Volume")
    def volume(self, obj):
        """Display product volume."""
        return f"{obj.volume():.2f} cm³"


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    """Admin configuration for Box model."""
    list_display = [
        "name",
        "internal_dimensions",
        "max_weight",
        "cost",
        "internal_volume",
    ]
    list_filter = ["name"]
    search_fields = ["name"]
    ordering = ["cost"]

    @admin.display(description="Internal Dimensions (L×W×H)")
    def internal_dimensions(self, obj):
        """Display box internal dimensions in a readable format."""
        return (
            f"{obj.internal_length} × {obj.internal_width} × "
            f"{obj.internal_height} cm"
        )

    @admin.display(description="Internal Volume")
    def internal_volume(self, obj):
        """Display box internal volume."""
        return f"{obj.internal_volume():.2f} cm³"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    list_display = ["id", "created_at", "item_count", "total_weight"]
    list_filter = ["created_at"]
    readonly_fields = ["id", "created_at", "item_count", "total_weight"]
    search_fields = ["id"]
    ordering = ["-created_at"]

    @admin.display(description="Items")
    def item_count(self, obj):
        """Display number of items in the order."""
        return obj.items.count()

    @admin.display(description="Total Weight")
    def total_weight(self, obj):
        """Display total weight of the order."""
        from .services import calculate_total_weight
        try:
            weight = calculate_total_weight(obj)
            return f"{weight:.2f} kg"
        except Exception:
            return "N/A"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for OrderItem model."""
    list_display = ["order", "product", "quantity", "item_weight"]
    list_filter = ["order", "product"]
    search_fields = ["order__id", "product__name"]

    @admin.display(description="Item Weight")
    def item_weight(self, obj):
        """Display total weight for this order item."""
        total = float(obj.product.weight) * obj.quantity
        return f"{total:.2f} kg"