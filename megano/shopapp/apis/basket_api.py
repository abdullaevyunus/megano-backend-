from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shopapp.models import Basket, OrderProduct, Product
from shopapp.serializers import BasketGetSerializer, BasketPOSTSerializer


class BasketAPIView(APIView):
    """
    Products in basket
    """

    @swagger_auto_schema(
        tags=['basket'],
        responses={
            200: BasketGetSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def get(self, request, format=None):
        """
        Get products
        """
        basket_items = Basket.objects.exclude(count=0)
        basket_counts = {item.id: item.count for item in basket_items}
        products = Product.objects.filter(id__in=basket_counts.keys())
        for product in products:
            product.count = basket_counts.get(product.id, 0)
        serializer = BasketGetSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['basket'],
        request_body=BasketPOSTSerializer,
        responses={
            200: BasketPOSTSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Add products to basket
        """
        serializer = BasketPOSTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['basket'],
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
    )
    def delete(self, request, format=None):
        """
        Delet products from basket
        """
        basket_id = request.data.get('id')
        basket_count = request.data.get('count')

        try:
            basket = Basket.objects.get(id=basket_id, count=basket_count)
        except Basket.DoesNotExist:
            return Response({"error": "Basket does not exist"}, status=status.HTTP_404_NOT_FOUND)

        basket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)