from rest_framework import serializers
from products.models import Product
from project.settings import HOST

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'image', 'category', 'barcode', 'name', 'description', 'price', 'weight']

    def get_image(self, obj):
        if obj.image:
            return f"{HOST}{obj.image.url}"
        return None