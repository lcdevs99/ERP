from django.db import models

class Product(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Ativo"),
        ("INACTIVE", "Inativo"),
    ]

    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="ACTIVE")

    def __str__(self):
        return f"{self.sku} - {self.name}"