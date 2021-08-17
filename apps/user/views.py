from rest_framework import generics
from rest_framework.response import Response

from apps.user.serializer import UserSerializer


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
