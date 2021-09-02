from apps import invite
from rest_framework import  serializers

from apps.invite.models import Invite
from apps.group.models import Group, GroupMember

        

class InviteUserSerializer(serializers.ModelSerializer):
    """
    Checking if user/ group is already invited and group exists
    Sending invitation to those eligible
    """
    class Meta:
        model = Invite
        fields = ['invitee', 'pokerboard', 'group', 'role', 'is_accepted', 'group_name']
        extra_kwargs = {
            'is_accepted': {'read_only': True},
            'group': {'read_only': True},
        }

    def validate(self, attrs):
        """
        Checking if user/ group is already invited and if group exists or not
        """
        invitee = attrs.get('invitee')
        group_name = attrs.get('group_name')
        pokerboard = attrs.get('pokerboard')

        if invitee:
            if Invite.objects.filter(pokerboard=pokerboard, invitee=invitee, group=None):
                raise serializers.ValidationError("User already invited")
        else:
            group = Group.objects.filter(name=group_name).first()
            if not group:
                raise serializers.ValidationError("Group does not exist")
            else:
                if Invite.objects.filter(pokerboard=pokerboard, group=group):
                    raise serializers.ValidationError("Group already invited")
            attrs['group'] = group
        return attrs

    def create(self, validated_data):
        """
        Sends invite to those eligible
        """
        invitee = validated_data['invitee']
        pokerboard = validated_data['pokerboard']
        role = validated_data['role']

        if invitee:
            Invite.objects.create(pokerboard=pokerboard, invitee=invitee, role=role)
        else:
            group = validated_data['group']
            members = GroupMember.objects.filter(group=group)
            for member in members:
                Invite.objects.create(invitee=str(member.user), pokerboard=pokerboard, group=group, role=role)
        return validated_data
