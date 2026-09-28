from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from .services import calculate_total_weight, recommend_box


class ProductListView(APIView):

    def get(self, request):
        products = Product.objects.all().order_by("id")
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)


class RecommendBoxView(APIView):

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.create()

        for item in serializer.validated_data["items"]:
            order.items.create(
                product=item["product"],
                quantity=item["quantity"],
            )

        box = recommend_box(order)
        total_weight = calculate_total_weight(order)

        if box is None:
            order.delete()

            return Response(
                {
                    "success": False,
                    "message": "No suitable box found.",
                    "total_weight": total_weight,
                },
                status=status.HTTP_400_BAD_REQUEST,
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
                "total_weight": total_weight,
            },
            status=status.HTTP_200_OK,
        )


def home(request):
    return render(request, "boxes/index.html")