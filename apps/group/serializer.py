from rest_framework import  serializers

from apps.user.models import User
from apps.user.serializers import UserSerializer
from apps.group.models import Group, GroupUser


class GroupUserSerializer(serializers.ModelSerializer):
    """
    Group serializer for adding group members
    """
    user = UserSerializer(many=False)

    class Meta:  
        model = GroupUser
        fields = ['id', 'user', 'group', 'created_at', 'updated_at']
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
    user = UserSerializer(many=False, read_only=True)
    email = serializers.EmailField(write_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.only("id"))

    def validate(self, attrs):
        email = attrs["email"]
        group = attrs["group"]
        user_objs = User.objects.filter(email=email)
        if not user_objs:
            raise serializers.ValidationError("No such user")
        user = user_objs.first()
        member = GroupUser.objects.filter(user=user, group=group)
        if member:
            raise serializers.ValidationError("A member can't be added to a group twice")
        attrs.update({"user": user})
        return attrs

    def create(self, validated_data):
        group = validated_data["group"]
        user = validated_data["user"]
        GroupUser.objects.create(user=user, group=group)
        return validated_data


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
