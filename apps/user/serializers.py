from django.contrib.auth import hashers, authenticate
from django.core import exceptions

from rest_framework import serializers as rest_framework_serializers

from apps.user import models as user_models


class UserSerializer(rest_framework_serializers.ModelSerializer):
    """
    Custom User Serializer class
    """

    class Meta:
        model = user_models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Hashing the password and creating a new user
        """
        validated_data['password'] = hashers.make_password(validated_data['password'])
        user = super().create(validated_data)
        return user


class LoginSerializer(rest_framework_serializers.Serializer):
    """
    Validating login credentials
    """
    email = rest_framework_serializers.EmailField()
    password = rest_framework_serializers.CharField()

    def validate(self, attrs):
        """
        Validating if user exists with given credentials
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if user: 
            if not user.is_active:
                raise exceptions.ValidationError('User account is disabled.')
        else:
            raise exceptions.ValidationError('Unable to log in with provided credentials.')

        attrs['user'] = user
        return attrs


class UserTokenSerializer(UserSerializer):
    """
    Generating token for already registered user
    """
    token = rest_framework_serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['token']

    def get_token(self, user):
        """
        Creating token for already registered user
        """
        return user_models.Token.objects.create(user=user).key
