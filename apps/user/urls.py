from django.urls import path

from rest_framework.authtoken import views as login_view

from apps.user import views


urlpatterns = [
    path('register', views.RegisterApi.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
]
