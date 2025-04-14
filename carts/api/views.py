import logging
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from products.models import Product
from carts.models import Cart, CartSession, CartItem
from carts.api.serializers import CartSessionSerializer, CartItemSerializer

logger = logging.getLogger('app')

class StartCartSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, cart_id=cart_id)
        if cart.status == "active":
            logger.warning(f"Cart {cart_id} already in use by another session.")
            return Response({"error": "Cart already in use."}, status=status.HTTP_400_BAD_REQUEST)

        cart_session = CartSession.objects.create(user=request.user, cart=cart)
        cart.status = "active"
        cart.save()

        logger.info(f"Cart session started by user {request.user.email} for cart {cart_id}.")
        return Response(CartSessionSerializer(cart_session).data, status=status.HTTP_201_CREATED)


class AddCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(CartSession, id=session_id, user=request.user, is_checked_out=False)
        serializer = CartItemSerializer(data=request.data)

        if 'barcode' not in request.data:
            logger.error(f"Barcode missing in add item request by user {request.user.email} for session {session_id}.")
            return Response({"error": "Barcode is required."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            barcode = serializer.validated_data['barcode']
            try:
                product = Product.objects.get(barcode=barcode, store=session.cart.store)
            except Product.DoesNotExist:
                logger.error(f"Product with barcode {barcode} not found in store {session.cart.store.name} for session {session_id}.")
                return Response({"error": "Product not found in the store."}, status=status.HTTP_404_NOT_FOUND)

            item, created = CartItem.objects.get_or_create(
                session=session,
                product=product,
                defaults={'quantity': serializer.validated_data['quantity']}
            )

            if not created:
                item.quantity += serializer.validated_data['quantity']
                item.save()
            logger.info(f"User {request.user.email} added product {item.product.name} to cart session {session_id}.")
            return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

        logger.error(f"Failed to add item to cart session {session_id} by user {request.user.email}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(CartSession, id=session_id, user=request.user, is_checked_out=False)

        if 'barcode' not in request.data:
            logger.error(f"Barcode missing in remove item request by user {request.user.email} for session {session_id}.")
            return Response({"error": "Barcode is required."}, status=status.HTTP_400_BAD_REQUEST)

        barcode = request.data['barcode']
        try:
            product = Product.objects.get(barcode=barcode, store=session.cart.store)
        except Product.DoesNotExist:
            logger.error(f"Product with barcode {barcode} not found in store {session.cart.store.name} for session {session_id}.")
            return Response({"error": "Product not found in the store."}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = CartItem.objects.get(session=session, product=product)
        except CartItem.DoesNotExist:
            logger.error(f"Product {product.name} not found in cart session {session_id} for user {request.user.email}.")
            return Response({"error": "Product not found in the cart."}, status=status.HTTP_404_NOT_FOUND)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            logger.info(f"User {request.user.email} decreased quantity of product {item.product.name} in session {session_id}.")
            return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)
        else:
            item.delete()
            logger.info(f"User {request.user.email} removed product {item.product.name} from session {session_id}.")
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

        logger.info(f"User {request.user.email} checked out cart session {session_id}.")
        return Response({"message": "Checkout successful"}, status=status.HTTP_200_OK)
