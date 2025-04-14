import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.api.serializers import LoginSerializer, RegisterSerializer, ProfileSerializer
from users.models import CustomUser

logger = logging.getLogger('app')


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = CustomUser.objects.get(email=validated_data['email'])

        logger.info(f"User {user.email} logged in successfully.")
        return Response({
            'user': {
                'email': user.email,
                'role': user.role.name,
            },
            'tokens': validated_data['tokens']
            }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(f"New user registered: {user.email}.")
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        logger.info(f"Profile viewed for user {request.user.email}.")
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Profile updated for user {request.user.email}.")
        return Response(serializer.data)
