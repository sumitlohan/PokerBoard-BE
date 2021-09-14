from rest_framework import  serializers

from apps.group import models as group_models
from apps.invite import models as invite_models

class PokerboardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = invite_models.Invite
        fields = ['id', 'type', 'invitee', 'pokerboard', 'group', 'role', 'is_accepted', 'group_name']
        extra_kwargs = {
            'type': {'write_only': True},
            'is_accepted': {'read_only': True},
            'group': {'read_only': True},
        }

class InviteUserSerializer(PokerboardMemberSerializer):
    """
    Checking if user/ group is already invited and group exists
    Sending invitation to those eligible
    """

    def validate(self, attrs):
        """
        Checking if user/ group is already invited and if group exists or not
        """
        type = attrs.get('type')
        pokerboard = attrs.get('pokerboard')
        if type==1:
            invitee = attrs.get('invitee')
            if invite_models.Invite.objects.filter(pokerboard=pokerboard, invitee=invitee, group=None):
                raise serializers.ValidationError("User already invited")
        else:
            group_name = attrs.get('group_name')
            group = group_models.Group.objects.filter(name=group_name).first()
            if not group:
                raise serializers.ValidationError("Group does not exist")
            else:
                if invite_models.Invite.objects.filter(pokerboard=pokerboard, group=group):
                    raise serializers.ValidationError("Group already invited")
            attrs['group'] = group
        return attrs

    def create(self, validated_data):
        """
        Sends invite to those eligible
        """
        type = validated_data['type']
        pokerboard = validated_data['pokerboard']
        role = validated_data['role']

        if type==1:
            invitee = validated_data['invitee']
            invite_models.Invite.objects.create(pokerboard=pokerboard, invitee=invitee, role=role)
        else:
            group = validated_data['group']
            group_name = validated_data['group_name']
            members = group_models.GroupMember.objects.filter(group=group)
            for member in members:
                invite_models.Invite.objects.create(invitee=str(member.user), pokerboard=pokerboard, group=group, group_name=group_name, role=role)
        return validated_data
