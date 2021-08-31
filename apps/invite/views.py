from rest_framework.generics import CreateAPIView

import apps.invite.models as invite_models
import apps.invite.serializer as invite_serializer
import apps.invite.permissions as invite_permissions

class InviteUserApi(CreateAPIView):
    """
    Group user API for adding group member
    """
    serializer_class = invite_serializer.InviteUserSerializer
    permission_classes = [invite_permissions.IsManagerPermission]
