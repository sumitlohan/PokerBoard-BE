from django.apps import AppConfig
from django.db.models.signals import post_save


class InviteConfig(AppConfig):
    name = 'apps.invite'

    def ready(self) -> None:
        from apps.invite.signals import send_email_handler
        from apps.invite.models import Invite
        post_save.connect(send_email_handler, sender=Invite)
