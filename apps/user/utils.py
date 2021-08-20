import datetime

from django.conf import settings


def get_expire_date():
    return datetime.datetime.now() + settings.TOKEN_TTL
