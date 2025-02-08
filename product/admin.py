from django.contrib import admin
from .models import Product, Category, Brand, HiddenProduct
from .models import Wallet, Transaction, Withdrawal

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'discount', 'units_in_stock', 'category', 'brand', 'expiry_date', 'is_hidden')
    list_filter = ('category', 'brand', 'expiry_date', 'is_hidden')
    search_fields = ('name', 'code', 'description')
    list_editable = ('price', 'discount', 'units_in_stock', 'is_hidden')
    fields = ('name', 'code', 'price', 'discount', 'units_in_stock', 'category', 'brand', 'expiry_date', 'image', 'image2',
              'description', 'is_hidden')

    def save_model(self, request, obj, form, change):
        # Custom save logic can be added here
        super().save_model(request, obj, form, change)


# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Brand Admin
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Hidden Product Admin
@admin.register(HiddenProduct)
class HiddenProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'units_in_stock', 'is_hidden')
    search_fields = ('name', 'code')
    list_filter = ('is_hidden', 'category', 'brand')

    def get_queryset(self, request):
        # Show only hidden products in this admin view
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=True)



@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'last_login_date')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'transaction_type', 'points', 'created_at', 'product_details')

    def product_details(self, obj):
        if obj.product:
            return f"{obj.product.name} - {obj.product_price} USD"
        return "No Product"

    product_details.short_description = 'Product and Price'  # Custom column name in admin


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'full_name', 'mobile_money_number', 'points', 'status', 'created_at')
    actions = ['mark_as_sent']

    def mark_as_sent(self, request, queryset):
        queryset.update(status='SENT')

    mark_as_sent.short_description = "Mark selected withdrawals as sent"


# Register models to the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)

# Customizing the admin site interface
admin.site.site_header = "My Custom Admin"
admin.site.site_title = "My Admin Portal"
admin.site.index_title = "Welcome to My Admin Dashboard"
