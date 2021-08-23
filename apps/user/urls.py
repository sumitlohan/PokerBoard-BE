from django.urls import path
from apps.user import views


urlpatterns = [
    path('register', views.RegisterApi.as_view(), name='register'),
]
