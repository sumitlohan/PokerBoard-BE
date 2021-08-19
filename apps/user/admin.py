from django.contrib import admin

import apps.user.models as user_model


admin.site.register(user_model.User)
admin.site.register(user_model.Token)
