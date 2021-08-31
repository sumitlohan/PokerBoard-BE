from django.db import models

from apps.user.models import CustomBase
from apps.group.models import Group
from apps.pokerboard.models import Pokerboard

class Invite(CustomBase):
    """
    Invite model
    """
    ROLE = (
        ("SPECTATOR", "Spectator"),
        ("CONTRIBUTOR", "Contributor"),
        ("GUEST", "Guest")
    )
    invitee = models.EmailField(null=True, help_text="Person invited")
    pokerboard = models.ForeignKey(Pokerboard, on_delete=models.CASCADE, help_text="Pokerboard")
    group_name = models.CharField(max_length=20, null=True, help_text="Name of group")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True,
            help_text="Name of group through which invited, if invited via group")
    role = models.CharField(choices=ROLE, max_length=20, help_text="Role")
    is_accepted = models.BooleanField(default=False, help_text="Accepted or not?")

    def __str__(self):
        return f'Invitee: {self.invitee} - Pokerboard: {self.pokerboard} - Group: {self.group}'
