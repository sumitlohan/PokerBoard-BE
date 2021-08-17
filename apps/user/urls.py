from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterApi, LoginApi

urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      path('api/login', LoginApi.as_view())
]
