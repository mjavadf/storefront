from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "unit_price",
        "inventory_status",
    ]
    list_editable = ["unit_price"]
    list_per_page = 10
    ordering = ["inventory"]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "LOW"
        return "OK"


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer_full_name", "payment_status"]
    list_per_page = 10
    list_editable = ["payment_status"]
    list_select_related = ["customer"]

    def customer_full_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"
