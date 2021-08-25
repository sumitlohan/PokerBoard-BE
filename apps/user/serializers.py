from django.contrib.auth import hashers, authenticate
from django.core import exceptions
from django.template.defaultfilters import first
from django.contrib.auth import hashers

from rest_framework import serializers as rest_framework_serializers

from apps.user import models as user_models


class UserSerializer(rest_framework_serializers.ModelSerializer):
    """
    Custom User Serializer class
    """

    class Meta:
        model = user_models.User
        fields = ['first_name', 'last_name', 'email', 'password']
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

class LoginSerializer(rest_framework_serializers.ModelSerializer):
    token = rest_framework_serializers.SerializerMethodField()
    email = rest_framework_serializers.EmailField()

    class Meta:
        model = user_models.User
        fields = ['email', 'password', 'token', 'first_name', 'last_name', 'id']
        extra_kwargs = {
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        '''
        Validating if user exists with given credentials
        '''
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def get_token(self, user):
        '''
        Creating token for already registered user
        '''
        return user_models.Token.objects.create(user=user).key

    def create(self, validated_data):
        user = validated_data['user']
        return user
