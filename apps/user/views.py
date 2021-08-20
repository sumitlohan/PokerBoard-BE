from rest_framework import viewsets
from rest_framework.response import Response

from apps.user.models import User as user_models
from apps.user.serializers import UserSerializer as user_serializers


class RegisterApi(viewsets.ModelViewSet):
    """
    User registration API
    """
    serializer_class = user_serializers
    queryset = user_models.objects.all()
    http_method_names = ['post']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = user_serializers(user, context=self.get_serializer_context()).data
        return Response(user_data)
