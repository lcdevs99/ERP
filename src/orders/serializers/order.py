from django.db import transaction, IntegrityError
from rest_framework import serializers
from orders.models import Order, OrderItem, Customer, Product, OrderStatusHistory
from .customer import CustomerSerializer
from .order_item import OrderItemSerializer
from .order_status_history import OrderStatusHistorySerializer

VALID_TRANSITIONS = {
    "PENDENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["SEPARADO", "CANCELADO"],
    "SEPARADO": ["ENVIADO"],
    "ENVIADO": ["ENTREGUE"],
    "ENTREGUE": [],
    "CANCELADO": [],
}

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
            "id",
            "number",
            "customer_id",
            "customer",
            "status",
            "created_at",
            "total_value",
            "notes",
            "items",
            "status_history",
            "idempotency_key",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        idempotency_key = validated_data.pop("idempotency_key", None)

        if idempotency_key:
            existing = Order.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                return existing

        with transaction.atomic():
            try:
                order = Order.objects.create(**validated_data, idempotency_key=idempotency_key)
            except IntegrityError:
                return Order.objects.get(idempotency_key=idempotency_key)

            total_value = 0
            for item_data in items_data:
                # Corrigido: acessar o objeto product corretamente
                product = Product.objects.select_for_update().get(pk=item_data["product"].id)
                quantity = item_data["quantity"]

                if product.status != "ACTIVE":
                    raise serializers.ValidationError(
                        {"detail": f"Produto {product.name} está inativo"}
                    )
                if quantity <= 0:
                    raise serializers.ValidationError(
                        {"detail": f"Quantidade inválida para {product.name}"}
                    )
                if product.stock < quantity:
                    raise serializers.ValidationError(
                        {"detail": f"Estoque insuficiente para {product.name}"}
                    )

                product.stock -= quantity
                product.save()

                unit_price = product.price
                subtotal = unit_price * quantity
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal,
                )
                total_value += subtotal

            order.total_value = total_value
            order.save()

        return order

    def update(self, instance, validated_data):
        new_status = validated_data.get("status", instance.status)

        with transaction.atomic():
            if new_status != instance.status:
                allowed = VALID_TRANSITIONS.get(instance.status, [])
                if new_status not in allowed:
                    raise serializers.ValidationError(
                        {"detail": f"Transição inválida de {instance.status} para {new_status}"}
                    )

                if new_status == "CANCELADO" and instance.status in ["PENDING", "CONFIRMED"]:
                    for item in instance.items.all():
                        product = item.product
                        product.stock += item.quantity
                        product.save()

                OrderStatusHistory.objects.create(
                    order=instance,
                    previous_status=instance.status,
                    new_status=new_status,
                    changed_by=self.context["request"].user if self.context.get("request") else None,
                    notes=validated_data.get("notes", "")
                )

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

        return instance