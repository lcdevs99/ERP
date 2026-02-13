from django.db import models
from django.utils import timezone

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

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

    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveProductManager() 
    all_objects = models.Manager() 

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.sku} - {self.name}"