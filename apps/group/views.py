from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data)

    def list(self, request):
        groups = self.get_queryset()
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        groups = Group.objects.filter(members__user=self.request.user)
        return groups

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GroupUserApi(ModelViewSet):
    """
    Group user API for adding group member
    """
    serializer_class = AddGroupMemberSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsGroupAdminPermission]

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        self.check_object_permissions(request, group)
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        GroupUser.objects.create(user=user, group=group)
        return Response({"status": "success"})

