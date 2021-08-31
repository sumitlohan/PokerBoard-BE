from django.urls import path

from apps.invite import views


urlpatterns = [
      path('invite', views.InviteUserApi.as_view(), name='invite'),
]
