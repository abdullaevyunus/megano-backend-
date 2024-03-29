from shopapp.models import Order, Product
from shopapp.serializers import OrderSerializer, OrderProductPOSTSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


class OrderListCreateAPIView(APIView):
    """
    Orders List and Create
    """

    def get(self, request):
        """
        Get orders
        """
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """
        Post order ID
        """
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
    def get(self, request, pk):
        """
        Get order detail
        """
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request, pk):
        """
        Confirm order
        """
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            order.status = request.data.get('status', order.status)
            order.save()
            return Response({"message": "Order status updated successfully"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


