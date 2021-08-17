from django.dispatch import receiver
from django.db import models

from apps.user.models import User
from apps.user.tasks import send_email_task


@receiver(models.signals.post_save, sender=User)
def handler(sender, instance, created, **kwargs):
    if created:
        send_email_task.delay(instance.email, instance.first_name)
