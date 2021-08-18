from django.urls import path

from apps.group.views import GroupApi, GroupUserApi

urlpatterns = [
      path('', GroupApi.as_view()),
      path('create-members', GroupUserApi.as_view())
]
