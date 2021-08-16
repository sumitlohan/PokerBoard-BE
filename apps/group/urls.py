from django.urls import path
from .views import GroupApi, GroupUserApi

urlpatterns = [
      path('', GroupApi.as_view()),
      path('member', GroupUserApi.as_view())
]