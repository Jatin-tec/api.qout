from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.api.serializers import LoginSerializer
from users.models import CustomUser


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = CustomUser.objects.get(email=validated_data['email'])

        return Response({
            'user': {
                'email': user.email,
                'role': user.role.name,
            },
            'tokens': validated_data['tokens']
            }, status=status.HTTP_200_OK)
