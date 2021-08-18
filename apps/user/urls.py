from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from apps.user.views import RegisterApi, LoginView

urlpatterns = [
      path('accounts/register', RegisterApi.as_view()),
      path('accounts/login', LoginView.as_view()),
]
