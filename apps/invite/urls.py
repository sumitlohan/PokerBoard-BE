from django.urls import path

import apps.invite.views as invite_views


urlpatterns = [
      path('invite', invite_views.InviteUserApi.as_view(), name='invite'),
]
