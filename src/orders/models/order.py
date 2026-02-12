from django.db import models
from .customer import Customer
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONFIRMADO", "Confirmado"),
        ("SEPARADO", "Separado"),
        ("ENVIADO", "Enviado"),
        ("ENTREGUE", "Entregue"),
        ("CANCELADO", "Cancelado"),
    ]

    number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")
    created_at = models.DateTimeField(auto_now_add=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    idempotency_key = models.CharField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.number:
            from uuid import uuid4
            self.number = str(uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.number} - {self.customer.name} - {self.status}"