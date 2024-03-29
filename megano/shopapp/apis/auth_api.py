from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json


class SignUpView(APIView):
    @swagger_auto_schema(tags=['auth'])

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            username = data.get('username')
            password = data.get('password')

            if not name or not username or not password:
                return Response({'error': 'Name, username, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, password=password)
            user.name = name
            user.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    @swagger_auto_schema(tags=['auth'])

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):
    @swagger_auto_schema(tags=['auth'])

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not logged in'}, status=status.HTTP_400_BAD_REQUEST)
