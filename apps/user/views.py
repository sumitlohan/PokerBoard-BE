from rest_framework import viewsets, mixins

from apps.user import serializers as user_serializers


class RegisterApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer
