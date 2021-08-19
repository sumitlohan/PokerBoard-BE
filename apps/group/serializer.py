from rest_framework import  serializers

from apps.group.models import Group, GroupUser
from apps.user.serializer import UserSerializer


class GroupUserSerializer(serializers.ModelSerializer):
    """
    Group serializer for adding group members
    """
    user = UserSerializer(many=False)
    class Meta:  
        model = GroupUser
        fields = ['id','user','group', 'created_at', 'updated_at']
        kwargs = {
            'created_at': {
                'read_only': True
            },
            'updated_at': {
                'read_only': True
            },
        }

class AddGroupMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()


class GroupSerializer(serializers.ModelSerializer):
    """
    Group serializer fetching/adding groups
    """

    members = GroupUserSerializer(many=True, required=False)
    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_by': {
                'read_only': True,
            },
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            },
        }
