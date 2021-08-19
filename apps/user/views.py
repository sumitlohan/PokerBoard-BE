from rest_framework import generics
from rest_framework.response import Response

from apps.user.serializers import UserSerializer


class RegisterApi(generics.GenericAPIView):
    """
    User registration API
    """
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(
            user, context=self.get_serializer_context()).data
        return Response(user_data)
