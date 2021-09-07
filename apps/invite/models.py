from django.db import models

import apps.user.models as user_models
import apps.group.models as group_models
import apps.pokerboard.models as pokerboard_models

class Invite(user_models.CustomBase):
    """
    Invite model
    """
    ROLE = (
        ("SPECTATOR", "Spectator"),
        ("CONTRIBUTOR", "Contributor"),
    )
    invitee = models.EmailField(null=True, help_text="Person invited")
    pokerboard = models.ForeignKey(pokerboard_models.Pokerboard, on_delete=models.CASCADE, help_text="Pokerboard")
    group_name = models.CharField(max_length=20, null=True, help_text="Name of group")
    group = models.ForeignKey(group_models.Group, on_delete=models.CASCADE, null=True,
            help_text="Name of group through which invited, if invited via group")
    role = models.CharField(choices=ROLE, max_length=20, help_text="Role")
    is_accepted = models.BooleanField(default=False, help_text="Accepted or not?")

    def __str__(self):
        return f'Invitee: {self.invitee} - Pokerboard: {self.pokerboard} - Group: {self.group}'
