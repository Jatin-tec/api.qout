from rest_framework import serializers
from carts.models import Cart, CartSession, CartItem
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['barcode', 'name', 'price', 'weight', 'image']


class CartItemSerializer(serializers.ModelSerializer):
    cart_id = serializers.CharField(source='session.cart.cart_id', read_only=True)
    product = ProductSerializer(read_only=True)
    store = serializers.CharField(source='session.cart.store.name', read_only=True)
    barcode = serializers.CharField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['cart_id', 'product', 'store', 'barcode', 'quantity', 'scanned_at']


class CartSessionSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = CartSession
        fields = ['id', 'user', 'cart', 'started_at', 'ended_at', 'is_checked_out', 'items']
        read_only_fields = ['started_at', 'ended_at', 'is_checked_out', 'user', 'cart']
