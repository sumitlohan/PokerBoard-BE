from apps.user.tasks import send_email_task


def send_email_handler(**kwargs):
    """
    Django signal handler for sending email whenever a user is created
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        send_email_task.delay(instance.email, instance.first_name)
