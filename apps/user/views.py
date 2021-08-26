from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.user import(
    serializers as user_serializers,
    models as user_models
)


class RegisterApiView(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer


class ActivateAccount(UpdateAPIView):
    """ 
    Activating User account if token is valid
    """
    serializer_class = user_serializers.AccountSerializer
    queryset = user_models.User.objects.all()
