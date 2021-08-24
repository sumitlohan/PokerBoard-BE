from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from rest_framework import  serializers

from apps.user.models import User
from apps.user.serializer import UserSerializer
from apps.group.models import Group, GroupUser


class GroupUserSerializer(serializers.ModelSerializer):
    """
    Group serializer for adding group members
    """
    user = UserSerializer(many=False)
    class Meta:  
        model = GroupUser
        fields = ['id','user','group', 'created_at', 'updated_at']
        kwargs = {
            'id': {
                'read_only': True,
            },
            'created_at': {
                'read_only': True
            },
            'updated_at': {
                'read_only': True
            },
        }

class AddGroupMemberSerializer(serializers.Serializer):
    """
    Serializer for adding group member
    """
    email = serializers.EmailField()
    groupId = serializers.IntegerField()
    def create(self, validated_data):
        try:
            email = validated_data["email"]
            group = validated_data["group"]
            user = User.objects.get(email=email)
            
            GroupUser.objects.create(user=user, group=group)
            return {
                "email": email
            }
        except ObjectDoesNotExist:
            raise serializers.ValidationError("No such user")
        except IntegrityError:
            raise serializers.ValidationError("A member can't be added to a group twice")


class GroupSerializer(serializers.ModelSerializer):
    """
    Group serializer fetching/adding groups
    """

    members = GroupUserSerializer(many=True, required=False)
    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
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
