from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models import Count

from tags.models import TaggedItem
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


class TagInline(GenericTabularInline):
    model = TaggedItem
    extra = 1
    autocomplete_fields = ["tag"]


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html(
                f"""
        <img src="{instance.image.url}" class="thumbnail"/>
        """
            )
        return ""


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["collection"]
    actions = ["clear_inventory"]
    list_display = ["title", "unit_price", "inventory_status", "collection"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_filter = ["last_update", "collection", InventoryFilter]
    ordering = ["inventory", "id"]
    search_fields = ["title"]
    inlines = [TagInline, ProductImageInline]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "LOW"
        return "OK"

    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(request, f"{update_count} products were successfully updated")

    class Media:
        css = {"all": ["store/styles.css"]}


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": customer.id})
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ["product"]
    extra = 1
    min_num = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer_full_name", "payment_status"]
    list_per_page = 10
    list_editable = ["payment_status"]
    list_select_related = ["customer"]
    inlines = [OrderItemInline]

    def customer_full_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        # admin:app_model_page
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": collection.id})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))
