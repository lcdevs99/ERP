from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from orders.models import Product
from orders.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Soft delete
    def perform_destroy(self, instance):
        instance.soft_delete()

    # Filtros e ordenação
    filterset_fields = ["status", "sku"]
    ordering_fields = ["price", "stock", "name"]

    @action(detail=True, methods=["patch"], url_path="stock")
    def update_stock(self, request, pk=None):
        product = self.get_object()
        new_stock = request.data.get("stock")
        if new_stock is not None:
            product.stock = new_stock
            product.save()
            return Response({"stock": product.stock}, status=status.HTTP_200_OK)
        return Response({"error": "Stock not provided"}, status=status.HTTP_400_BAD_REQUEST)