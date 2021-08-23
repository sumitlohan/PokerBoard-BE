from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from django.contrib.auth import login
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from apps.user import models as user_models
from apps.user.tokens import account_activation_token
from apps.user import serializers as user_serializers


class RegisterApi(CreateAPIView):
    """
    User registration API
    """
    serializer_class = user_serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return Response(serializer.data)


class ActivateAccount(RetrieveAPIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = user_models.User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, user_models.User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response('Thank you for your email confirmation. Now you can login your account.')
        else:
            return Response('Activation link is invalid!')
