from rest_framework import viewsets, mixins

from apps.user.models import User as user_models
from apps.user.serializers import UserSerializer as user_serializers


class RegisterApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    User registration API
    """
    serializer_class = user_serializers
    queryset = user_models.objects.all()
