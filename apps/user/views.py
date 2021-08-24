from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


from apps.user import models as user_models
from apps.user.utils import TokenGenerator
from apps.user import serializers as user_serializers


class RegisterApi(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer


class ActivateAccount(CreateAPIView):
    """ 
    Activating User account if token is valid
    """
    def create(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = user_models.User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, user_models.User.DoesNotExist):
            user = None

        account_activation_token = TokenGenerator()
        if user is not None and account_activation_token.check_token(user, token):
            user.is_account_verified = True
            user.save()
            login(request, user)
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid!')
