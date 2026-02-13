from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Customer(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Ativo"),
        ("INACTIVE", "Inativo"),
    ]

    name = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=18, unique=True) 
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="ACTIVE")

    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()       
    all_objects = models.Manager() 

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.name} ({self.cpf_cnpj})"