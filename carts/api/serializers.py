from rest_framework import serializers
from carts.models import Cart, CartSession, CartItem
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'barcode', 'name', 'price', 'weight', 'image']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'scanned_at']

class CartSessionSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = CartSession
        fields = ['id', 'user', 'cart', 'started_at', 'ended_at', 'is_checked_out', 'items']
        read_only_fields = ['started_at', 'ended_at', 'is_checked_out', 'user', 'cart']
