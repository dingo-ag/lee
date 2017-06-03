from django.contrib import admin
from apps.shop.models import Product, Category, Manufacturer, Comment, DeliveryService, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'image', 'category', 'description', 'characteristics', 'status',
              'size', 'total_count', 'price', 'discount', 'manufacturer', 'product_code']
    list_display = ['name', 'category', 'status', 'price', 'total_count']
    list_filter = ['category', 'status', 'manufacturer']
    search_fields = ['name', 'manufacturer']
    readonly_fields = ['id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class CategoryManufacturer(admin.ModelAdmin):
    pass


@admin.register(DeliveryService)
class DeliveryServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    fields = ['id', 'product', 'count']
    readonly_fields = ['id']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'status', 'created', 'delivery_service', 'shipping_address', 'tracking_number',
              'description', 'system_comment']
    readonly_fields = ['created']
    inlines = (OrderItemInline,)
    list_display = ['id', 'user', 'status', 'tracking_number']
    list_filter = ['status', 'modified', 'user']
