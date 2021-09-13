from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from apps.invite import (
    models as invite_models,
    serializer as invite_serializers,
    permissions as invite_permissions
)
from apps.pokerboard import models as pokerboard_models


class PokerboardMembersApi(ListAPIView):
    serializer_class = invite_serializers.PokerboardMemberSerializer

    def get(self, request, pk=None):
        pokerboard = pokerboard_models.Pokerboard.objects.get(id=pk)
        queryset = invite_models.Invite.objects.filter(pokerboard=pokerboard.id).filter(is_accepted=True)
        pokerboard_member_serializer = self.serializer_class(queryset, many=True)
        return Response(pokerboard_member_serializer.data)
        

class InviteUserApi(CreateAPIView):
    """
    API for inviting user to pokerboard
    """
    serializer_class = invite_serializers.InviteUserSerializer
    permission_classes = [invite_permissions.IsManagerPermission]


class AcceptInviteApi(UpdateAPIView):
    """
    Invitation acception API
    """
    permission_classes = [AllowAny]
    queryset = invite_models.Invite.objects.all()

    def put(self, request, pk = None, *args, **kwargs):
        instance = self.queryset.get(id=pk)
        # TODO: Check if user's account is verified
        if instance.invitee == self.request.user.email and instance.is_accepted == False:
            instance.is_accepted = True
            instance.save()
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

class RemoveInviteeApi(DestroyAPIView):
    permission_classes = [invite_permissions.IsManagerPermission]
    queryset = invite_models.Invite.objects.filter(is_accepted=True)

    def delete(self, request, pk = None, *args, **kwargs):
        instance = self.queryset.get(id=pk)
        if instance:
            instance.delete()

            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)
