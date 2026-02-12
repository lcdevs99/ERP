from django.db import models

class Customer(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Ativo"),
        ("INACTIVE", "Inativo"),
    ]

    name = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=18, unique=True)  # aceita CPF ou CNPJ
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="ACTIVE")

    def __str__(self):
        return f"{self.name} ({self.cpf_cnpj})"