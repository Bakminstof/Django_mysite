from django.contrib import admin
from django.http import HttpRequest

from shopapp.models import Item, Order, Tax, Discount


class ItemInline(admin.TabularInline):  # Many-to-many rls
    model = Order.items.through
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price_usd']
    list_display_links = ['name']
    ordering = ['name']
    search_fields = ['name', 'description']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'tax_value']
    list_display_links = ['id']
    search_fields = ['value']

    @staticmethod
    def tax_value(obj):
        return f'{obj.value}%'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'discount_value']
    list_display_links = ['id']
    search_fields = ['value']

    @staticmethod
    def discount_value(obj):
        return f'{obj.value}%'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'tax_value', 'discount_value', 'total_price_usd']
    list_display_links = ['name',]
    ordering = ['name']
    search_fields = ['name', 'description', 'items']
    inlines = [ItemInline]

    @staticmethod
    def tax_value(obj):
        return f'{obj.tax.value}%'

    @staticmethod
    def discount_value(obj):
        return f'{obj.discount.value}%'

    def get_queryset(self, request: HttpRequest):
        return Order.objects.select_related('user').prefetch_related('items')
