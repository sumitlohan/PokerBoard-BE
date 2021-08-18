from rest_framework import serializers as rest_framework_serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.user.models import Token, User


class UserSerializer(rest_framework_serializers.ModelSerializer):
    """
    Custom User Serializer class 
    """
    token = rest_framework_serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_token(self, user):
        return Token.objects.create(user=user).key

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        try:
            validate_password(validated_data['password'], user=user)
        except ValidationError as e:
            raise rest_framework_serializers.ValidationError({"error":e})
        user.set_password(validated_data['password'])
        user.save()
        return user
