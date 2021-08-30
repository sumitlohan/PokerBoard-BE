from django.db import models
from django.utils.translation import TranslatorCommentWarning

from apps.user.models import CustomBase, User
from apps.pokerboard.models import Pokerboard

class Invite(CustomBase):
    """
    Invite details class
    """
    ROLE = (
        ("SPECTATOR", "Spectator"),
        ("CONTRIBUTOR", "Contributor"),

    )
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Inviter")
    invitee = models.EmailField(help_text="Invitee")
    pokerboard = models.ForeignKey(Pokerboard, on_delete=models.CASCADE, help_text="Pokerboard")
    group = models.ForeignKey(Group, null=True)
    role = models.CharField(choices=ROLE, max_length=10, help_text="Role")
    is_accepted = models.BooleanField(default=False, help_text="Accepted or not?")
    invite_time = models.DateTimeField(help_text="Time at which invited")
