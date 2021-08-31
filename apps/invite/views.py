from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.invite.models import Invite
from apps.invite.serializer import  InviteUserSerializer
from apps.invite.permissions import IsManagerPermission

class InviteUserApi(CreateAPIView):
    """
    Group user API for adding group member
    """
    serializer_class = InviteUserSerializer
    permission_classes = [IsManagerPermission]


class AcceptInviteApi(UpdateAPIView):
    queryset = Invite.objects.all()

    def put(self, request, pk = None, *args, **kwargs):
        instance = self.queryset.get(id=pk)
        # TODO: Check if user's account is verified
        if instance.invitee == self.request.user.email and instance.is_accepted == False:
            instance.is_accepted = True
            instance.save()
            return Response(status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)