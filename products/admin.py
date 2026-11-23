from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'subcategory', 'price', 'in_stock')
    list_filter = ('category', 'subcategory')
    search_fields = ('title', 'artikul')
    inlines = [ProductImageInline]


admin.site.register(Chip)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    inlines = [SubcategoryInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    inlines = [CartProductInline]


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'amount')
