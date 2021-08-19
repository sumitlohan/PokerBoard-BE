from rest_framework import serializers as rest_framework_serializers

from apps.user.models import Token, User
from apps.user import validators as field_validator


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
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, password):
        field_validator.CustomPasswordValidator.validate(self,password)
        return password
