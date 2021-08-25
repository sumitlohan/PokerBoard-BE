from django.urls import path

from apps.user import views


urlpatterns = [
    path('register', views.RegisterApiView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
]
