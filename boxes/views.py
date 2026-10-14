"""
Box Selection System - API Views

Provides REST API endpoints for:
- Product listing
- Box recommendation
- Order creation
"""

import logging

from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from .services import calculate_total_weight, recommend_box

logger = logging.getLogger(__name__)


class ProductListView(APIView):
    """
    API endpoint to list all products.
    
    GET /api/products/
        Returns: List of all products with their dimensions and weight
    """

    def get(self, request):
        """
        Retrieve all products ordered by ID.
        
        Returns:
            Response: JSON array of products
        """
        try:
            products = Product.objects.all().order_by("id")
            serializer = ProductSerializer(products, many=True)
            logger.debug(f"Retrieved {products.count()} products")

            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error retrieving products: {e}")
            return Response(
                {"error": "Failed to retrieve products"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecommendBoxView(APIView):
    """
    API endpoint to recommend a shipping box for an order.
    
    POST /api/recommend-box/
        Body: {
            "items": [
                {"product": product_id, "quantity": qty},
                ...
            ]
        }
        Returns: Recommended box details or error message
    """

    def post(self, request):
        """
        Create an order and recommend the best box.
        
        Validates order data, creates the order, calculates total weight,
        and finds the most cost-effective box that can contain all items.
        """
        logger.info(f"Received box recommendation request: {request.data}")

        # Validate order data
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Validation failed: {serializer.errors}")
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Create order with items
            order = Order.objects.create()

            for item in serializer.validated_data["items"]:
                order.items.create(
                    product=item["product"],
                    quantity=item["quantity"],
                )

            logger.info(f"Created order {order.id} with items")

            # Get box recommendation
            box = recommend_box(order)
            total_weight = calculate_total_weight(order)

            if box is None:
                logger.warning(
                    f"No suitable box found for order {order.id}. Deleting order."
                )
                order.delete()

                return Response(
                    {
                        "success": False,
                        "message": "No suitable box found.",
                        "total_weight": float(total_weight),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            logger.info(
                f"Successfully recommended box {box.id} for order {order.id}"
            )
            return Response(
                {
                    "success": True,
                    "order_id": order.id,
                    "recommended_box": {
                        "id": box.id,
                        "name": box.name,
                        "cost": float(box.cost),
                        "max_weight": float(box.max_weight),
                    },
                    "total_weight": float(total_weight),
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error in box recommendation: {e}", exc_info=True)
            return Response(
                {"error": "An error occurred while processing your request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def home(request):
    """
    Render the main application page.
    
    GET /
        Returns: HTML page with the box selection interface
    """
    logger.debug("Rendering home page")
    return render(request, "boxes/index.html")
