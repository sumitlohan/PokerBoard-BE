from django.db import models

import apps.user.models as user_models


class Group(user_models.CustomBase):
    """
    Group model for storing name and group admin details
    """
    name = models.CharField(unique=True, max_length=50, help_text="Name of the group")
    created_by = models.ForeignKey(user_models.User, related_name="groups_created", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name


class GroupUser(user_models.CustomBase):
    """
    GroupUser model for storing membership details
    """
    user = models.ForeignKey(user_models.User, related_name="groups", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="members", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self) -> str:
        return f"{self.user.email} - {self.group.name}"
