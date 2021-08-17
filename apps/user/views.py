from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.serializer import UserSerializer, LoginSerializer


#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user=user)
        user_data = UserSerializer(user, context=self.get_serializer_context()).data
        return Response({
            "user": user_data,
            "token" : token
        })

    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Login API  
class LoginApi(TokenObtainPairView):
    serializer_class = LoginSerializer
