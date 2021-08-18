from apps.user.tasks import send_email_task


def send_email_handler(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        send_email_task.delay(instance.email, instance.first_name)
