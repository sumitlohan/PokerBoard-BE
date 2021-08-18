from apps.group.models import GroupUser


def create_default_group_member(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        GroupUser.objects.create(user=instance.created_by, group = instance)
