from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
\
        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        refresh = RefreshToken.for_user(user)

        return {
            'email': user.email,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)