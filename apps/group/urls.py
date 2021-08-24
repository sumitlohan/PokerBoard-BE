from django.urls import path

from rest_framework import routers

from apps.group.views import GroupApi, GroupUserApi

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', GroupApi, basename="groups")
urlpatterns = [
      # path('', GroupApi.as_view({
      #       'get': 'list',
      #       'post': 'create'
      # })),
      # path('<int:pk>', GroupApi.as_view({
      #       'get': 'retrieve'
      # })),
      path('create-members', GroupUserApi.as_view())
] + router.urls
