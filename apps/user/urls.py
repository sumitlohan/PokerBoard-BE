from django.urls import path

from apps.user.views import RegisterApi, LoginApi

urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('api/login', LoginApi.as_view())
]
