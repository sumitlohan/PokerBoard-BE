from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.user.models import Token


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Expiring token for mobile and desktop clients.
    It expires every {n} hrs requiring client to supply valid username 
    and password for new one to be created.
    """

    model = Token

    def authenticate_credentials(self, key, request=None):
        models = self.get_model()
        
        try:
            token = models.objects.select_related("user").get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed(
                {"error": "Invalid or Inactive Token"}
            )

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": "Invalid user"}
            )

        utc_now = timezone.now()

        if token.expired_at < utc_now :
            raise AuthenticationFailed(
                {"error": "Token has expired"}
            )
        return token.user, token
