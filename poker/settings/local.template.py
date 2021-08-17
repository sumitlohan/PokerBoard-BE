from poker.settings.base import BaseSettings

class LocalSettings(BaseSettings):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '<Enter Database Name>',
            'USER': '<Enter Database Username>',
            'PASSWORD': '<Enter Database Password>',
        }
    }
    CELERY_BROKER_URL = '<Enter Broker URL>'
    CELERY_BROKER_USER = '<Enter Broker Name>'
    CELERY_BROKER_PASSWORD = '<Enter Broker Name>'
    CELERY_BROKER_VHOST = '<Enter Broker Name>'

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = '<Enter Email>'
    EMAIL_HOST_PASSWORD = '<Enter Email Password>'
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
