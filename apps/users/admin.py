from django.contrib import admin

from .models import User, ShippingAddress, WishlistItem, Wishlist


@admin.register(ShippingAddress)
class ShippingAddress(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'phone', 'is_active']
    fields = ['email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active']


class WishlistItemInline(admin.StackedInline):
    model = WishlistItem


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    inlines = [WishlistItemInline]
