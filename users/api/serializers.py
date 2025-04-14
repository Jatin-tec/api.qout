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
        
        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)
       
        print(user, user.is_active, 'user')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        refresh = RefreshToken.for_user(user)

        print(refresh, 'refresh')

        return {
            'email': user.email,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'phone']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            phone=validated_data['phone']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'email_verified']
