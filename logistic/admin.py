from django.contrib import admin

from logistic.models import StockProduct, Product, Stock


class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    inlines = [StockProductInline]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass

@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = ['stock', 'product', 'quantity', 'price']
