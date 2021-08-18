from apps.user.tasks import send_email_task


def send_email_handler(sender, instance, created, **kwargs):
    if created:
        send_email_task.delay(instance.email, instance.first_name)
