from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from products.models import Product
from carts.models import Cart, CartSession, CartItem
from carts.api.serializers import CartSessionSerializer, CartItemSerializer

class StartCartSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        if cart.status == "active":
            return Response({"error": "Cart already in use."}, status=status.HTTP_400_BAD_REQUEST)

        cart_session = CartSession.objects.create(
            user=request.user, cart=cart
        )
        cart.status = "active"
        cart.save()

        return Response(CartSessionSerializer(cart_session).data, status=status.HTTP_201_CREATED)


class AddCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(CartSession, id=session_id, user=request.user, is_checked_out=False)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            item, created = CartItem.objects.get_or_create(
                session=session,
                product=serializer.validated_data['product'],
                defaults={'quantity': serializer.validated_data['quantity']}
            )
            if not created:
                item.quantity += serializer.validated_data['quantity']
                item.save()
            return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID required"}, status=status.HTTP_400_BAD_REQUEST)

        session = get_object_or_404(CartSession, id=session_id, user=request.user, is_checked_out=False)
        item = get_object_or_404(CartItem, session=session, product_id=product_id)

        item.delete()
        return Response({"message": "Item removed"}, status=status.HTTP_200_OK)


class ViewCartSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, session_id):
        session = get_object_or_404(CartSession, id=session_id, user=request.user)
        return Response(CartSessionSerializer(session).data)


class CheckoutCartSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(CartSession, id=session_id, user=request.user, is_checked_out=False)
        session.ended_at = now()
        session.is_checked_out = True
        session.save()

        cart = session.cart
        cart.status = "idle"
        cart.save()

        return Response({"message": "Checkout successful"}, status=status.HTTP_200_OK)
