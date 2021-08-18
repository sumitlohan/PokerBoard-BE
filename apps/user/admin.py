from django.contrib import admin
from apps.user.models import User,Token

admin.site.register(User)
admin.site.register(Token)
