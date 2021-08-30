from django.db import models
from django.utils.translation import TranslatorCommentWarning

from apps.user.models import CustomBase, User
from apps.group.models import Group
from apps.pokerboard.models import Pokerboard

class Invite(CustomBase):
    """
    Invite details class
    """
    ROLE = (
        ("SPECTATOR", "Spectator"),
        ("CONTRIBUTOR", "Contributor"),
        ("GUEST", "Guest")
    )
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Invited by")
    invitee = models.EmailField(help_text="Person invited")
    pokerboard = models.ForeignKey(Pokerboard, on_delete=models.CASCADE, help_text="Pokerboard")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, help_text="Name of group through which invited, if invited via group")
    role = models.CharField(choices=ROLE, max_length=10, help_text="Role")
    is_accepted = models.BooleanField(default=False, help_text="Accepted or not?")
    invite_time = models.DateTimeField(help_text="Time at which invited")

    def __str__(self):
        return f'{self.invitee} - {self.pokerboard}'
