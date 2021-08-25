from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.user'

    def ready(self) -> None:
        from apps.user.signals import send_email_handler
        from apps.user.models import User
        post_save.connect(send_email_handler, sender=User)
