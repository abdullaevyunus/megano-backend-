from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shopapp.serializers import PaymentSerializer



class PaymentAPIView(APIView):
    """
    Payment details
    """
    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
