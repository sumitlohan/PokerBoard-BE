from rest_framework import  serializers

from apps.group.models import Group, GroupUser


class GroupUserSerializer(serializers.ModelSerializer):
    """
    Group serializer for adding group members
    """
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

class GroupSerializer(serializers.ModelSerializer):
    """
    Group serializer fetching/adding groups
    """

    class Meta:
        model = Group
        fields = ['id', 'name','created_by', 'created_at', 'updated_at']
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
