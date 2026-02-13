from rest_framework import serializers
from orders.models import OrderStatusHistory

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["id", "previous_status", "new_status", "changed_at", "changed_by", "notes"]
        read_only_fields = ["previous_status", "new_status", "changed_at", "changed_by"]