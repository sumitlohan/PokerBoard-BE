from apps.invite.tasks import send_email_task
from apps.pokerboard.serializers import PokerboardSerializer

def send_email_handler(**kwargs):
    """
    Django signal handler for sending invitation email
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        send_email_task.delay(instance.id, instance.invitee, PokerboardSerializer(instance=instance.pokerboard).data, instance.role)
