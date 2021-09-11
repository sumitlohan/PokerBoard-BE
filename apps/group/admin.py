from django.contrib import admin

import apps.group.models as group_models


admin.site.register(group_models.Group)
admin.site.register(group_models.GroupMember)
