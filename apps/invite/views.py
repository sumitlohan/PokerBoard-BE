from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

import apps.invite.models as invite_models
import apps.invite.serializer as invite_serializer
import apps.invite.permissions as invite_permissions

class InviteUserApi(CreateAPIView):
    """
    Group user API for adding group member
    """
    serializer_class = invite_serializer.InviteUserSerializer
    permission_classes = [invite_permissions.IsManagerPermission]


class AcceptInviteApi(UpdateAPIView):
    queryset = invite_models.Invite.objects.all()

    def put(self, request, pk = None, *args, **kwargs):
        instance = self.queryset.get(id=pk)
        # TODO: Check if user's account is verified
        if instance.invitee == self.request.user.email and instance.is_accepted == False:
            instance.is_accepted = True
            instance.save()
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)
