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
        return user_models.Token.objects.create(user=user).key

    def create(self, validated_data):
        user = user_models.User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.is_active = False
        user.set_password(validated_data['password'])
        user.save()
        return user
