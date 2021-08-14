from .base import BaseSettings


class LocalSettings(BaseSettings):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<Enter Database Name>',
        'USER': '<Enter Database Username>',
        'PASSWORD': '<Enter Database Password>',
    }
}
