from django.contrib import admin
from products.models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name', 'description', 'price', 'weight')
    list_filter = ('barcode', 'name', 'description', 'price', 'weight')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)