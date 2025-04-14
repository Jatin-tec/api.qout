from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from products.models import Product
from products.api.serializers import ProductSerializer

class ProductView(APIView):
    def get(self, request, barcode=None):
        if barcode:
            product = get_object_or_404(Product, barcode=barcode)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        products = Product.objects.all()
        print(products)
        serializer = ProductSerializer(products, many=True)
        print(serializer )
        return Response(serializer.data)

class ProductAddView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response({"message": "Product added successfully.", "product_id": product.id}, status=status.HTTP_201_CREATED)

class ProductEditView(APIView):
    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product updated successfully."}, status=status.HTTP_200_OK)

def sum_(request, num1, num2):
    result = num1 + num2
    return JsonResponse({"result":result})