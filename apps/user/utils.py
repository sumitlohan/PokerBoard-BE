from django.conf import settings
from django.utils import timezone

def get_expire_date():
        return timezone.now() + settings.TOKEN_TTL
