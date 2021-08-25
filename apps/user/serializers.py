import datetime
from django.contrib.auth import hashers, authenticate
from django.core import exceptions
from django.template.defaultfilters import first

from rest_framework import serializers as rest_framework_serializers

from apps.user import models as user_models


class UserSerializer(rest_framework_serializers.ModelSerializer):
    """
    Custom User Serializer class 
    """
    token = rest_framework_serializers.SerializerMethodField()

    class Meta:
        model = user_models.User
        fields = ['first_name', 'last_name', 'email', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_token(self, user):
        """
        Creating token for the user
        """
        return user_models.Token.objects.create(user=user).key

    def create(self, validated_data):
        validated_data['password'] = hashers.make_password(validated_data['password'])
        user = super().create(validated_data)
        return user

class LoginSerializer(rest_framework_serializers.ModelSerializer):
    token = rest_framework_serializers.SerializerMethodField()
    email = rest_framework_serializers.EmailField()
    password = rest_framework_serializers.CharField(write_only=True)

    class Meta:
        model = user_models.User
        fields = ['email', 'password', 'token', 'first_name', 'last_name', 'id']
        extra_kwargs = {
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'id': {'read_only': True},
            # 'password': {'write_only': True}
        }

    def validate(self, attrs):
        # import pdb
        # pdb.set_trace()
        print(attrs)
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
        """
        Creating token for the user
        """
        # import pdb
        # pdb.set_trace()

        token, created =  user_models.Token.objects.get_or_create(user=user, expired_at__gt=datetime.datetime.now())

        if token:
            return token.key
        return user_models.Token.objects.create(user=user)


    def create(self, validated_data):
        # import pdb
        # pdb.set_trace()
        email = validated_data['email']
        password = validated_data['password']
        user = authenticate(email=email, password=password)
        
        return user
