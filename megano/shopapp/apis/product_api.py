from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shopapp.models import Product
from shopapp.serializers import ProductSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404


class ProductDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Get product by ID",
        responses={200: ProductSerializer()},
    )
    def get(self, request, pk):
        """
        Get product by ID
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductReviewAPIView(APIView):
    @swagger_auto_schema(
        tags=['product'],
        request_body=ReviewSerializer,
        responses={
            200: ReviewSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
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




