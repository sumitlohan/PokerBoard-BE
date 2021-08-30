from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.user import serializers as user_serializers


class RegisterApiView(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer
    permission_classes = [AllowAny]


class LoginView(CreateAPIView):
    '''
    Login API
    '''
    serializer_class = user_serializers.LoginSerializer
