from rest_framework.generics import CreateAPIView

from apps.user import serializers as user_serializers


class RegisterApiView(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer


class LoginView(CreateAPIView):
    '''
    Login API
    '''
    serializer_class = user_serializers.LoginSerializer
