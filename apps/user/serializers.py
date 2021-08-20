from rest_framework import serializers as rest_framework_serializers

from apps.user.models import(
    Token as AuthToken,
    User as user_models
)
from apps.user import validators as field_validator


class UserSerializer(rest_framework_serializers.ModelSerializer):
    """
    Custom User Serializer class 
    """
    token = rest_framework_serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = user_models
        fields = ['first_name', 'last_name', 'email', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, password):
        field_validator.CustomPasswordValidator.validate(password)
        return password

    def create(self, validated_data):
        user = user_models(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user.token=AuthToken.objects.create(user=user).key
        return user
