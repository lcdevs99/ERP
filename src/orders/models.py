from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.cpf})"


class LoanProposal(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="proposals")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal {self.id} - {self.customer.name} - {self.status}"