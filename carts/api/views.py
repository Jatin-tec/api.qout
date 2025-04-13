from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from store.models import Store
from products.models import Product
from carts.models import Cart, UserCart, CartItem

from products.api.serializers import ProductSerializer
from carts.api.serializers import CartSerializer

class CartView(APIView):

    def get(self, request, store_slug):
        user = request.user
        shop = get_object_or_404(Store, store_slug=store_slug)
        user_cart = get_object_or_404(UserCart, user=user, shop=shop)
        
        cart_serializer = CartSerializer(user_cart.cart)
        return Response(cart_serializer.data)
    
    def post(self, request, store_slug):
        try:
            barcode = request.query_params.get("barcode")
            quantity = int(request.query_params.get("quantity", 1))
            shop = get_object_or_404(Store, store_slug=store_slug)
            product = get_object_or_404(Product, barcode=barcode, store=shop)
            user_cart, created = UserCart.objects.get_or_create(user=request.user, shop=shop)
            cart = user_cart.cart

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)