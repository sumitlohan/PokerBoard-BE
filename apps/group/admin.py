from django.contrib import admin

import apps.group.models as group_members


admin.site.register(group_members.Group)
admin.site.register(group_members.GroupMember)
