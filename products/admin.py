from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'subcategory', 'price', 'in_stock')
    list_filter = ('category', 'subcategory')
    search_fields = ('title', 'artikul')
    inlines = [ProductImageInline]


admin.site.register(Chip)
admin.site.register(Category)
admin.site.register(Subcategory)
