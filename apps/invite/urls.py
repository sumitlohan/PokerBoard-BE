from django.urls import path

from rest_framework import routers

import apps.invite.views as invite_views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', invite_views.PokerboardMembersApi, basename="members")

# urlpatterns = [
#       path('invite', invite_views.InviteUserApi.as_view(), name='invite'),
#       path('invite/<int:pk>', invite_views.AcceptInviteApi.as_view(), name='accept-invite'),
#       path('remove/<int:pk>', invite_views.RemoveInviteeApi.as_view(), name='remove-invitee'),
#       path('<int:pk>', invite_views.PokerboardMembersApi.as_view(), name='members')
# ]

urlpatterns = router.urls
