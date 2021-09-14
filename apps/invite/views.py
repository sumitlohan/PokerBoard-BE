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

class PokerboardMembersApi(ModelViewSet):
    serializer_class = invite_serializers.InviteUserSerializer
    pokerboard_member_serializer = invite_serializers.PokerboardMemberSerializer
    queryset = invite_models.Invite.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [AllowAny]
        if self.action == 'create' or self.action == 'destroy': 
            permission_classes = [invite_permissions.IsManagerPermission]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Invites a user/group to pokerboard
        Only pokerboard's manager can perform this action
        """
        pokerboard = pokerboard_models.Pokerboard.objects.get(id=self.request.data['pokerboard'])
        self.check_object_permissions(self.request, pokerboard)
        return super().perform_create(serializer)

    def retrieve(self, request, pk = None):
        """
        Gets all the pokerboard's members
        """
        invitee = invite_models.Invite.objects.filter(pokerboard=pk, is_accepted=True)
        members = self.pokerboard_member_serializer(invitee, many=True)
        return Response(members.data)

    def update(self, request, pk = None, *args, **kwargs):
        """
        Invitation acception API
        """
        instance = self.queryset.get(id=pk)
        if instance.invitee == self.request.user.email and instance.is_accepted == False:
            instance.is_accepted = True
            instance.save()
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None, *args, **kwargs):
        """
        Removes member from pokerboard
        Only pokerboard's manager can perform this action
        """
        pokerboard = pokerboard_models.Pokerboard.objects.get(id=self.request.data['pokerboard'])
        self.check_object_permissions(self.request, pokerboard)
        instance = self.queryset.get(id=pk)
        if instance:
            instance.delete()

            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)
