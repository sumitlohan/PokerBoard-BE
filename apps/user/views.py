from rest_framework.generics import CreateAPIView, UpdateAPIView

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.user import (
    models as user_models,
    serializers as user_serializers
)


class RegisterApiView(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer
    permission_classes = [AllowAny]


class LoginView(CreateAPIView):
    """
    Login API
    """
    serializer_class = user_serializers.LoginSerializer
    user_token_serializer = user_serializers.UserTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        return Response(self.user_token_serializer(login_serializer.validated_data['user']).data)


class ActivateAccountView(UpdateAPIView):
    """ 
    Activating User account if token is valid
    """
    serializer_class = user_serializers.AccountVerificationSerializer
    queryset = user_models.User.objects.all()
