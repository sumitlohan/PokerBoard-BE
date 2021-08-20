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
        token = TokenAuthentication.authenticate_credentials(self, key)
        time_now = datetime.datetime.now()
        if token[1].expired_at < time_now:
            raise AuthenticationFailed(
                {"error": "Token has expired"}
            )
        return token[1].user, token[1]
