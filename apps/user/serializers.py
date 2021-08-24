from rest_framework import serializers as rest_framework_serializers

from apps.user import models as user_models

from django.contrib.auth import hashers


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
