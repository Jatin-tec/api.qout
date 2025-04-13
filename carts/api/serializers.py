from rest_framework import serializers
from carts.models import Cart, CartItem

class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        items = CartItem.objects.filter(cart=obj)
        return CartItemSerializer(items, many=True).data

    class Meta:
        model = Cart
        fields = ["id", "status", "create_at", "update_at"]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "cart", "product", "quantity", "create_at", "update_at"]
        depth = 2

