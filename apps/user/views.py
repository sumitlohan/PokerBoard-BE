from rest_framework import generics, parsers, renderers
from rest_framework.response import Response

from rest_framework.generics import CreateAPIView

from apps.user import serializers as user_serializers

from apps.user import models as user_models



class RegisterApi(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer


class LoginView(CreateAPIView):
    '''
    Login API
    '''
    serializer_class = user_serializers.LoginSerializer
