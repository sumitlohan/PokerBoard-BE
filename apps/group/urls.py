from django.urls import path

from apps.group.views import GroupApi, GroupUserApi

urlpatterns = [
      path('', GroupApi.as_view({
            'get': 'list',
            'post': 'create'
      })),
      path('<int:pk>', GroupApi.as_view({
            'get': 'retrieve'
      })),
      path('<int:pk>/create-members', GroupUserApi.as_view({'post': 'post'}))
]
