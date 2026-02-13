from rest_framework import serializers
from orders.models import Order, Customer
from .customer import CustomerSerializer
from .order_item import OrderItemSerializer
from .order_status_history import OrderStatusHistorySerializer
from orders.services import OrderService  # importa o service

class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.filter(status="ACTIVE"),
        source="customer",
        write_only=True
    )
    customer = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True, required=False)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    idempotency_key = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = [
            "id", "number", "customer_id", "customer", "status",
            "created_at", "total_value", "notes", "items",
            "status_history", "idempotency_key",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        idempotency_key = validated_data.pop("idempotency_key", None)
        return OrderService.create_order(validated_data, items_data, idempotency_key)

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        user = None
        if self.context.get("request") and self.context["request"].user.is_authenticated:
            user = self.context["request"].user
        return OrderService.update_order(instance, validated_data, items_data, user)