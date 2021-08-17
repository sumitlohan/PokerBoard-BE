from django.contrib import admin

from apps.group.models import Group, GroupUser


admin.site.register(Group)
admin.site.register(GroupUser)

