from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shopapp.models import Product
from shopapp.serializers import ProductSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404


class ProductDetailView(APIView):
    def get(self, request, pk):
        """
        Get product by ID
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductReviewAPIView(APIView):

    def post(self, request, pk):
        """
        Post review to product
        """
        product = Product.objects.get(pk=pk)
        request.data['product'] = product.pk
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


