from rest_framework import serializers

import apps.user.models as user_models
import apps.user.serializers as user_serializers
import apps.group.models as group_models


class GroupUserSerializer(serializers.ModelSerializer):
    """
    Group serializer for adding group members
    """
    user = user_serializers.UserSerializer()

    class Meta:
        model = group_models.GroupUser
        fields = ['id', 'user', 'group', 'created_at', 'updated_at']


class AddGroupMemberSerializer(serializers.Serializer):
    """
    Serializer for adding group member
    """
    user = user_serializers.UserSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=group_models.Group.objects.only("id"))

    def validate(self, attrs):
        """
        Checks if user with given email exists or not.
        If exists, check if the user has already been added to the group.
        """
        email = attrs["email"]
        group = attrs["group"]
        user = user_models.User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("No such user")
        member = group_models.GroupUser.objects.filter(user=user, group=group)
        if member:
            raise serializers.ValidationError("A member can't be added to a group twice")
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """
        Creates group user object
        """
        group = validated_data["group"]
        user = validated_data["user"]
        instance = group_models.GroupUser.objects.create(user=user, group=group)
        return instance


class GroupSerializer(serializers.ModelSerializer):
    """
    Group serializer fetching/adding groups
    """

    members = GroupUserSerializer(many=True, read_only=True)

    class Meta:
        model = group_models.Group
        fields = ['id', 'name', 'members', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'created_by': {
                'read_only': True,
            },
        }
