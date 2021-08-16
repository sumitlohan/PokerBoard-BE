from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.group.serializer import GroupSerializer, GroupUserSerializer
from apps.group.permissions import IsGroupAdminPermission
from apps.group.models import Group

class GroupApi(generics.GenericAPIView):
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {
            "created_by": request.user.id
        }
        data.update(request.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self, request):
        groups = list(map(lambda x: x.group ,request.user.groups.all()))
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)


class GroupUserApi(generics.GenericAPIView):
    serializer_class = GroupUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsGroupAdminPermission]


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = Group.objects.get(id=request.data.get('group'))
        self.check_object_permissions(self.request, group)

        serializer.save()
        return Response(serializer.data)