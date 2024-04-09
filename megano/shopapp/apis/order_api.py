from drf_yasg.utils import swagger_auto_schema
from shopapp.models import Order, OrderProduct
from shopapp.serializers import OrderGETSerializer,OrderPOSTSerializer, OrderProductPOSTSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class OrderListCreateAPIView(APIView):
    """
    Orders List and Create
    """

    @swagger_auto_schema(
        tags=['order'],
        responses={
            200: OrderGETSerializer,
            404: 'Not Found'
        },
    )
    def get(self, request):
        """
        Get orders
        """
        orders = Order.objects.filter(user=request.user)
        serializer = OrderGETSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['order'],
        request_body=OrderProductPOSTSerializer,
        responses={
            200: OrderProductPOSTSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def post(self, request, format=None):
        user = request.user
        products_data = request.data
        for product_data in products_data:
            product_data["user"] = user.id

        serializer = OrderProductPOSTSerializer(data=products_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"orderId": serializer.data[0]["id"]}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderAPIView(APIView):
    """
    Order details
    """

    @swagger_auto_schema(
        tags=['order'],
        responses={
            200: OrderGETSerializer,
            404: 'Not Found'
        },
    )
    def get(self, request, pk):
        """
        Get order detail
        """
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderGETSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        tags=['order'],
        request_body=OrderPOSTSerializer,
        responses={
            200: OrderPOSTSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def post(self, request, pk, format=None):
        try:
            product = OrderProduct.objects.get(pk=pk)
        except OrderProduct.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderPOSTSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            order.products.add(product)
            return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)