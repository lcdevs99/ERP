from django.contrib import admin
from .models import Customer, LoanProposal

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "cpf", "birth_date")
    search_fields = ("name", "email", "cpf")


@admin.register(LoanProposal)
class LoanProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__name", "customer__cpf")

    def get_queryset(self, request):
        # otimização para evitar N+1 ao listar propostas
        return super().get_queryset(request).select_related("customer")