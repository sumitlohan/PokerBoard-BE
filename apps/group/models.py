from django.dispatch import receiver
from django.db import models

from apps.user.models import CustomBase, User


class Group(CustomBase):
    """
    Group model
    """
    name = models.CharField(max_length=50, help_text="group name")
    created_by = models.ForeignKey(User, related_name="groups_created", on_delete=models.CASCADE)


class GroupUser(CustomBase):
    """
    GroupUser model for storing membership details
    """
    class Meta:
        unique_together = (('user', 'group'))
    user = models.ForeignKey(User, related_name="groups", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="members", on_delete=models.CASCADE)


@receiver(models.signals.post_save, sender=Group)
def handler(sender, instance, created, **kwargs):
    if created:
        GroupUser.objects.create(user=instance.created_by, group = instance)

