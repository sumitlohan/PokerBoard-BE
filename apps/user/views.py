from rest_framework.generics import CreateAPIView

from apps.user import serializers as user_serializers


class RegisterApi(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer
