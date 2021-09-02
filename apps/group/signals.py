import apps.group.models as group_models


def create_default_group_member(**kwargs):
    """
    Creates default group member i.e creator of the group
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        group_models.GroupMember.objects.create(user=instance.created_by, group=instance)
