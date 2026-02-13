from django.contrib import admin
from orders.models import Customer, Product, Order, OrderItem, OrderStatusHistory

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cpf_cnpj", "email", "phone", "status")
    search_fields = ("name", "cpf_cnpj", "email")
    list_filter = ("status",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "price", "stock", "status")
    search_fields = ("sku", "name")
    list_filter = ("status",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "customer", "status", "total_value", "created_at")
    search_fields = ("number", "customer__name")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline, OrderStatusHistoryInline]