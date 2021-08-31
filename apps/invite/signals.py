from apps.invite.tasks import send_email_task


def send_email_handler(**kwargs):
    """
    Django signal handler for sending invitation email
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        send_email_task.delay(instance.invitee, instance.pokerboard, instance.role)
