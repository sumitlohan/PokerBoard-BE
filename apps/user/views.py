from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.user import serializers as user_serializers


class RegisterApiView(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer


class LoginView(CreateAPIView):
    """
    Login API
    """
    def post(self, request):
        login_serializer = user_serializers.LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user_token_serializer = user_serializers.UserTokenSerializer(login_serializer.validated_data['user'])
        return Response(user_token_serializer.data)
