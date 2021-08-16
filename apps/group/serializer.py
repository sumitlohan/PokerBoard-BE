from django.contrib.auth.models import Group
from rest_framework import  serializers
from .models import Group, GroupUser


class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = ['user','group', 'created_at', 'updated_at']

class GroupSerializer(serializers.ModelSerializer):
    members = GroupUserSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id', 'name','created_by', 'members', 'created_at', 'updated_at']
        extra_kwargs = {
        }


