from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.group.serializer import GroupSerializer, GroupUserSerializer
from apps.group.permissions import IsGroupAdminPermission
from apps.group.models import Group


class GroupApi(generics.CreateAPIView, generics.ListAPIView):
    """
    Group API for creating group and get list of groups
    a user is associated with.
    """
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data)

    def get(self, request):
        groups = Group.objects.filter(members__user=request.user)
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)


class GroupUserApi(generics.CreateAPIView):
    """
    Group user API for adding group member
    """
    serializer_class = GroupUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsGroupAdminPermission]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = Group.objects.get(id=request.data.get('group'))
        self.check_object_permissions(self.request, group)

        serializer.save()
        return Response(serializer.data)

