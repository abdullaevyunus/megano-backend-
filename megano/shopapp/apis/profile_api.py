from drf_yasg.utils import swagger_auto_schema

from shopapp.models import Profile
from shopapp.serializers import ProfileSerializer, ChangePasswordSerializer, ChangeAvatarSerializer, ImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.contrib.auth.hashers import check_password



class ProfileAPIView(APIView):
    """
    User's profile
    """

    @swagger_auto_schema(
        tags=['profile'],
        responses={
            200: ProfileSerializer,
            404: 'Not Found'
        },
    )
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

    @swagger_auto_schema(
        tags=['profile'],
        request_body=ProfileSerializer,
        responses={
            200: ProfileSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def post(self, request):
        user = request.user
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """
    Change password of profile
    """
    @swagger_auto_schema(
        tags=['profile'],
        request_body=ChangePasswordSerializer,
        responses={
            200: ChangePasswordSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data.get('currentPassword')
            new_password = serializer.validated_data.get('newPassword')
            user = request.user
            if not check_password(current_password, user.password):
                return Response({'detail': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAvatarAPIView(APIView):
    """
    Change profile image
    """
    @swagger_auto_schema(
        tags=['profile'],
        request_body=ImageSerializer,
        responses={
            200: ImageSerializer,
            400: 'Bad Request',
            404: 'Not Found'
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)