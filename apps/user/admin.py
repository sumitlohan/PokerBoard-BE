from django.contrib import admin

import apps.user.models as user_models


admin.site.register(user_models.User)
admin.site.register(user_models.Token)
