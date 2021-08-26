from rest_framework.generics import CreateAPIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.group.serializer import AddGroupMemberSerializer, GroupSerializer
from apps.group.permissions import IsGroupAdminPermission
from apps.group.models import Group


class GroupApi(ModelViewSet):
    """
    Group API for creating group and get list of groups
    a user is associated with.
    """
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        groups = Group.objects.filter(members__user=self.request.user)
        return groups


class GroupUserApi(CreateAPIView):
    """
    Group user API for adding group member
    """
    serializer_class = AddGroupMemberSerializer
    permission_classes = [IsAuthenticated, IsGroupAdminPermission]

    def perform_create(self, serializer):
        group = serializer.validated_data["group"]
        self.check_object_permissions(self.request, group)
        serializer.save()
