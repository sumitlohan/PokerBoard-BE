from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core import exceptions
from django.core.validators import validate_email

from rest_framework import  serializers
from rest_framework.authtoken.models import Token

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','token']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_token(self, user):
        return Token.objects.get_or_create(user = user)[0].key

    def create(self, validated_data):
        user = User(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if validate_email(email):
            user_request = get_object_or_404(
                User,
                email=email,
            )

            email = user_request.username

        user = authenticate(username=email, password=password)

        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
