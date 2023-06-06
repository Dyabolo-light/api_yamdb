from rest_framework import serializers

from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(max_length=5, required=True)

    class Meta:
        model = CustomUser
        fields = ['confirmation_code', 'username']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
