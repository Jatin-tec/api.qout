from django.contrib import admin
from products.models import Product, Category

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('product_id', 'barcode', 'name', 'description', 'price', 'weight', 'category', 'store')
        export_order = ('product_id', 'barcode', 'name', 'description', 'price', 'weight', 'category', 'store')
        import_id_fields = ('product_id',)


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('product_id', 'barcode', 'name', 'description', 'price', 'weight', 'store', 'category')
    list_filter = ('product_id', 'barcode', 'name', 'description', 'price', 'weight', 'store', 'category')
    search_fields = ('product_id', 'barcode', 'name', 'description', 'price', 'weight', 'store', 'category')
    
    resource_class = ProductResource


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'store')
        export_order = ('id', 'name', 'store')


class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'store')
    list_filter = ('id', 'name', 'store')
    search_fields = ('id', 'name', 'store')
    
    resource_class = CategoryResource


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)