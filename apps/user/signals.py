from django.contrib.auth.tokens import PasswordResetTokenGenerator

from apps.user.tasks import send_email_task


def send_email_handler(**kwargs):
    """
    Django signal handler for sending email whenever a user is created
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        account_activation_token = PasswordResetTokenGenerator()
        token = account_activation_token.make_token(instance)
        send_email_task.delay(instance.first_name, instance.pk, token, instance.email)
