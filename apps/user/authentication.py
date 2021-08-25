import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.user import models as user_models


class CustomTokenAuthentication(TokenAuthentication):
    """
    Checking if the token has expired 
    """
    model = user_models.Token

    def authenticate_credentials(self, key, request=None):
        """
        Check if the token is valid with the provided key
        """
        user, token = super().authenticate_credentials(key)
        time_now = datetime.datetime.now()
        if token.expired_at < time_now:
            raise AuthenticationFailed({"error": "Token has expired"})
        return user, token
