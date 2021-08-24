from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.generics import CreateAPIView, get_object_or_404

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from apps.group.serializer import AddGroupMemberSerializer, GroupSerializer
from apps.group.permissions import IsGroupAdminPermission
from apps.group.models import Group, GroupUser
from apps.user.models import User


class GroupApi(ModelViewSet):
    """
    Group API for creating group and get list of groups
    a user is associated with.
    """
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsGroupAdminPermission]

    def perform_create(self, serializer):
        pk = serializer.validated_data["groupId"]
        group = get_object_or_404(Group.objects.all(), id=pk)
        self.check_object_permissions(self.request, group)
        serializer.save(group=group)
