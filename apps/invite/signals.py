from apps.invite.tasks import send_email_task
import apps.pokerboard.serializers as pokerboard_serializers

def send_email_handler(**kwargs):
    """
    Django signal handler for sending invitation email
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        send_email_task.delay(instance.id, instance.invitee, pokerboard_serializers.PokerboardSerializer(instance=instance.pokerboard).data, instance.role)
