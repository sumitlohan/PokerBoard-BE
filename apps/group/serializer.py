from django.contrib.auth.models import Group
from rest_framework import  serializers
from apps.group.models import Group, GroupUser


class GroupUserSerializer(serializers.ModelSerializer):
    """
    Group serializer
    """


    class Meta:
        model = GroupUser
        fields = ['user','group', 'created_at', 'updated_at']


class GroupSerializer(serializers.ModelSerializer):
    """
    Group serializer
    """
    members = GroupUserSerializer(many=True)


    class Meta:
        model = Group
        fields = ['id', 'name','created_by', 'members', 'created_at', 'updated_at']


