from django.contrib import admin
from apps import pokerboard

from apps.pokerboard import models as pokerboard_models

admin.site.register(pokerboard_models.Pokerboard)
admin.site.register(pokerboard_models.Ticket)
