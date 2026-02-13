from django.db import models
from .order import Order
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    previous_status = models.CharField(max_length=15, choices=Order.STATUS_CHOICES)
    new_status = models.CharField(max_length=15, choices=Order.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="status_changes"
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.order.number}: {self.previous_status} -> {self.new_status}"