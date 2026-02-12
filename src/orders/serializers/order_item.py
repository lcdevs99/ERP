from rest_framework import serializers
from orders.models import OrderItem, Product
from .product import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(status="ACTIVE"),  # só produtos ativos
        source="product",
        write_only=True
    )
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "product", "quantity", "unit_price", "subtotal"]
        read_only_fields = ["unit_price", "subtotal"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value