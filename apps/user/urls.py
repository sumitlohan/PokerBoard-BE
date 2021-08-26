def create(self, validated_data):
        """
        Hashing the password and creating a new user
        """
        return user_models.Token.objects.create(user=user).keyfrom django.urls import path

from apps.user import views


urlpatterns = [
    path('register', views.RegisterApiView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
]
