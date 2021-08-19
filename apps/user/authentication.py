from django.conf import settings
from django.utils import timezone

from rest_framework import (
    authentication as rest_framework_authentication,
    exceptions as rest_framework_exceptions
)

from apps.user import models as user_model


class CustomTokenAuthentication(rest_framework_authentication.TokenAuthentication):
    """
    Checking if the token has expired 
    """

    model = user_model.Token

    def authenticate_credentials(self, key, request=None):
        model = self.get_model()

        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise rest_framework_exceptions.AuthenticationFailed(
                {"error": "Invalid or Inactive Token"}
            )

        if not token.user.is_active:
            raise rest_framework_exceptions.AuthenticationFailed(
                {"error": "Invalid user"}
            )

        time_now = timezone.now()

        if token.expired_at < time_now:
            raise rest_framework_exceptions.AuthenticationFailed(
                {"error": "Token has expired"}
            )
        return token.user, token
