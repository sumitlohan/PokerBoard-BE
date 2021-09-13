from django.urls import path

import apps.invite.views as invite_views


urlpatterns = [
      path('invite', invite_views.InviteUserApi.as_view(), name='invite'),
      path('invite/<int:pk>', invite_views.AcceptInviteApi.as_view(), name='accept-invite'),
      path('remove/<int:pk>', invite_views.RemoveInviteeApi.as_view(), name='remove-invitee'),
      path('<int:pk>', invite_views.PokerboardMembersApi.as_view(), name='members')
]
