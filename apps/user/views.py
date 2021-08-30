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
    serializer_class = user_serializers.LoginSerializer
    user_token_serializer = user_serializers.UserTokenSerializer
    
    def post(self, request):
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        return Response(self.user_token_serializer(login_serializer.validated_data['user']).data)
