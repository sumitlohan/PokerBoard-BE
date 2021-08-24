from django.urls import path

from rest_framework import routers

from apps.group.views import GroupApi, GroupUserApi

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', GroupApi, basename="groups")
urlpatterns = [
      path('create-members', GroupUserApi.as_view())
] + router.urls
