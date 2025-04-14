from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ['category', 'barcode', 'name', 'description', 'price', 'weight']
