from django.contrib.auth import hashers
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers as rest_framework_serializers

from apps.user import(
    constants as user_constants,
    models as user_models
)


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
        """
        Hashing the password and creating a new user
        """
        validated_data['password'] = hashers.make_password(validated_data['password'])
        return super().create(validated_data)


class AccountSerializer(rest_framework_serializers.Serializer):
    """
    Email verification serializer
    """
    token = rest_framework_serializers.CharField(max_length=150, write_only=True)

    def validate_token(self, attrs):
        """
        Checking if the token is valid for account activation
        """
        account_activation_token = PasswordResetTokenGenerator()
        if account_activation_token.check_token(self.instance, attrs):
            return self.instance
        raise rest_framework_serializers.ValidationError(user_constants.EMAIL_VALIDATION_ERROR)
   
    def update(self, user, validated_data):
        """
        Activating user's account
        """
        user.is_account_verified = True
        user.save(update_fields=["is_account_verified"])
        return user
