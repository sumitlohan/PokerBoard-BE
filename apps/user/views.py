from rest_framework import generics, parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from apps.user.serializer import UserSerializer, LoginSerializer


class RegisterApi(generics.GenericAPIView):
    serializer_class = UserSerializer
    """
    User registration API
    """
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user, context=self.get_serializer_context()).data
        return Response(user_data)


class LoginView(APIView):
    '''Login API
    '''

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key,
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

        return Response(content)
