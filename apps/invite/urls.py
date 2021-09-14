from django.urls import path

from rest_framework import routers

import apps.invite.views as invite_views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', invite_views.PokerboardMembersApi, basename="members")

urlpatterns = router.urls
