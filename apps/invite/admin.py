from django.contrib import admin

from apps.invite import models as invite_models

admin.site.register(invite_models.Invite)
