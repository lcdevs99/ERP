# src/orders/services.py
from django.db import transaction, IntegrityError
from rest_framework import serializers
from orders.models import Order, OrderItem, Product, OrderStatusHistory

VALID_TRANSITIONS = {
    "PENDENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["SEPARADO", "CANCELADO"],
    "SEPARADO": ["ENVIADO"],
    "ENVIADO": ["ENTREGUE"],
    "ENTREGUE": [],
    "CANCELADO": [],
}

class OrderService:
    @staticmethod
    def create_order(validated_data, items_data, idempotency_key=None):
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
                product = Product.objects.select_for_update().get(pk=item_data["product"].id)
                quantity = item_data["quantity"]

                if product.status != "ACTIVE":
                    raise serializers.ValidationError({"detail": f"Produto {product.name} está inativo"})
                if quantity <= 0:
                    raise serializers.ValidationError({"detail": f"Quantidade inválida para {product.name}"})
                if product.stock < quantity:
                    raise serializers.ValidationError({"detail": f"Estoque insuficiente para {product.name}"})

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

    @staticmethod
    def update_order(instance, validated_data, items_data=None, user=None):
        new_status = validated_data.get("status", instance.status)
        if new_status:
            new_status = new_status.upper()

        with transaction.atomic():
            if new_status != instance.status:
                allowed = VALID_TRANSITIONS.get(instance.status, [])
                if new_status not in allowed:
                    raise serializers.ValidationError(
                        {"detail": f"Transição inválida de {instance.status} para {new_status}"}
                    )

                if new_status == "CANCELADO" and instance.status in ["PENDENTE", "CONFIRMADO"]:
                    for item in instance.items.all():
                        product = item.product
                        product.stock += item.quantity
                        product.save()

                OrderStatusHistory.objects.create(
                    order=instance,
                    previous_status=instance.status,
                    new_status=new_status,
                    changed_by=user,
                    notes=validated_data.get("notes", "")
                )

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.status = new_status
            instance.save()

            if items_data is not None:
                instance.items.all().delete()
                total_value = 0
                for item_data in items_data:
                    product = Product.objects.get(pk=item_data["product"].id)
                    quantity = item_data["quantity"]
                    unit_price = product.price
                    subtotal = unit_price * quantity
                    OrderItem.objects.create(
                        order=instance,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal,
                    )
                    total_value += subtotal
                instance.total_value = total_value
                instance.save()

        return instance