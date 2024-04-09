from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shopapp.serializers import PaymentSerializer
from shopapp.models import Order



class PaymentAPIView(APIView):
    """
    Payment details
    """

    @swagger_auto_schema(
        tags=['payment'],
        request_body=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        request.data['order'] = pk
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)