from rest_framework.generics import CreateAPIView

from apps.invite.models import Invite
from apps.invite.serializer import  InviteUserSerializer
from apps.invite.permissions import IsManagerPermission

class InviteUserApi(CreateAPIView):
    """
    Group user API for adding group member
    """
    serializer_class = InviteUserSerializer
    permission_classes = [IsManagerPermission]
