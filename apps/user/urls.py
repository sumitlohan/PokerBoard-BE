from django.urls import path

from apps.user.views import RegisterApi

urlpatterns = [
      path('accounts/register', RegisterApi.as_view()),
]
