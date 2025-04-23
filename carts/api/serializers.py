from rest_framework import serializers
from carts.models import Cart, CartSession, CartItem
from products.models import Product
from project.settings import HOST
import random


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['barcode', 'name', 'price', 'weight', 'image']

    def get_image(self, obj):
        if obj.image:
            return f"{HOST}{obj.image.url}"
        return None

class CartItemSerializer(serializers.ModelSerializer):
    cart_id = serializers.CharField(source='session.cart.cart_id', read_only=True)
    product = ProductSerializer(read_only=True)
    store = serializers.CharField(source='session.cart.store.name', read_only=True)
    barcode = serializers.CharField(write_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.product.image:
            return f"{HOST}{obj.product.image.url}"
        return None

    class Meta:
        model = CartItem
        fields = ['cart_id', 'image', 'product', 'store', 'barcode', 'quantity', 'scanned_at']


class CartSessionSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = CartSession
        fields = ['id', 'user', 'cart', 'started_at', 'ended_at', 'is_checked_out', 'items']
        read_only_fields = ['started_at', 'ended_at', 'is_checked_out', 'user', 'cart']


class CartSerializer(serializers.ModelSerializer):
    store = serializers.CharField(source='store.name', read_only=True)
    charge = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_id', 'store', 'items', 'status', 'charge']
        read_only_fields = ['cart_id', 'store', 'items']

    def get_charge(self, obj):
        charge = random.randint(0, 100)
        return charge
    
    def get_items(self, obj):
        cart_items = CartItem.objects.filter(session__cart=obj)
        serializer = CartItemSerializer(cart_items, many=True)
        return serializer.data
