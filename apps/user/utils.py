import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.conf import settings


def get_expire_date():
    """
    Generating expiry date for token
    """
    return datetime.datetime.now() + settings.TOKEN_TTL

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generating token for email activation
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
