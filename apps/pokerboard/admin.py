from django.contrib import admin

from apps.pokerboard import models as pokerboard_models

admin.site.register(pokerboard_models.Pokerboard)
