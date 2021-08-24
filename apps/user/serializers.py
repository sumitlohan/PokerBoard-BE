from rest_framework import serializers as rest_framework_serializers

from django.contrib.auth import hashers
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.user import models as user_models
from apps.user.utils import TokenGenerator


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
        current_site = get_current_site(self.context['request'])
        account_activation_token = TokenGenerator()
        subject = 'Activate Your Account'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return user
