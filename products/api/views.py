import logging
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from products.models import Product
from products.api.serializers import ProductSerializer

logger = logging.getLogger('app')

class ProductView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, barcode=None):
        if barcode:
            product = get_object_or_404(Product, barcode=barcode)
            serializer = ProductSerializer(product)
            logger.info(f"Product details retrieved for barcode {barcode}.")
            return Response(serializer.data)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        logger.info("All products retrieved.")
        return Response(serializer.data)

class ProductAddView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            logger.info(f"Product added: {product.name} (Barcode: {product.barcode}).")
            return Response({"message": "Product added successfully.", "product_id": product.id}, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to add product: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductEditView(APIView):
    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Product updated: {product.name} (ID: {id}).")
            return Response({"message": "Product updated successfully."}, status=status.HTTP_200_OK)
        logger.error(f"Failed to update product (ID: {id}): {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def sum_(request, num1, num2):
    result = num1 + num2
    return JsonResponse({"result":result})