import json
from typing import Any
from typing_extensions import OrderedDict

from django.db.models import IntegerField
from django.db.models.expressions import Case, When
from django.http import request

from rest_framework import serializers

from apps.group import models as group_models
from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models,
    utils as pokerboard_utils
)
from apps.user import serializers as user_serializers


class TicketSerializer(serializers.ModelSerializer):
    """
    Ticket serializer for displaying ticket details
    """

    class Meta:
        model = pokerboard_models.Ticket
        fields = ["id", "ticket_id", "estimate", "rank"]


class PokerboardSerializer(serializers.ModelSerializer):
    """
    Pokerboard serializer for displaying/retrieving pokerboards
    """
    tickets = TicketSerializer(many=True, read_only=True)
    manager = user_serializers.UserSerializer(read_only=True)

    class Meta:
        model = pokerboard_models.Pokerboard
        fields = ["id", "title", "description", "estimation_type", "duration", "manager", "status", "tickets", "created_at"]


class CreatePokerboardSerializer(PokerboardSerializer):
    """
    Create Pokerboard serializer which requires a list of tickets and
    validate them by calling an api, creates Ticket objects for the same.
    """
    tickets = serializers.ListField(child=serializers.SlugField(), write_only=True)

    class Meta(PokerboardSerializer.Meta):
        extra_kwargs = {
            "status": {
                "read_only": True
            },
        }

    def validate(self: serializers.ModelSerializer, attrs: Any) -> Any:
        """
        Validates list of tickets by calling an API
        """
        attrs = super().validate(attrs)
        tickets = attrs["tickets"]
        # removing [] from ["KD-1", "KD-2"]. ["KD-1", "KD-2"] -> "KD-1", "KD-2"
        ticket_ids = json.dumps(tickets)[1:-1]
        jql = f"issue IN ({ticket_ids})"
        url = f"{pokerboard_constants.JIRA_API_URL_V2}search?jql={jql}"

        # validate ticket Id's
        pokerboard_utils.query_jira("GET", url)
        attrs["manager"] = self.context.get("request").user
        return attrs

    def create(self: serializers.ModelSerializer, validated_data: OrderedDict) -> OrderedDict:
        """
        Creates Pokerboard object and list of Ticket objects
        """
        tickets = validated_data.pop("tickets")
        pokerboard = super().create(validated_data)
        pokerboard_models.Ticket.objects.bulk_create(
            [pokerboard_models.Ticket(pokerboard=pokerboard, ticket_id=ticket, rank=idx+1) for idx, ticket in enumerate(tickets)]
        )
        return pokerboard


class CommentSerializer(serializers.Serializer):
    """
    Comment serializer with comment and the issue to comment on
    """
    comment = serializers.CharField()
    issue = serializers.SlugField()


class TicketOrderSerializer(serializers.ListSerializer):
    child = TicketSerializer()

    def create(self: serializers.ListSerializer, validated_data: list) -> list:
        """
        Order tickets according to ticket_id's
        """
        pokerboard = self.context.get('pk')
        ticket_ids = list(map(lambda x: x["ticket_id"], validated_data))
        tickets = pokerboard_models.Ticket.objects.filter(ticket_id__in=ticket_ids, pokerboard=pokerboard)\
                    .order_by(Case(
                        *[When(ticket_id=n, then=i) for i, n in enumerate(ticket_ids)],
                        output_field=IntegerField(),
                    ))\
                    .all()
        for ticket, updated_ticket in zip(tickets, validated_data):
            ticket.rank = updated_ticket.get('rank')
        pokerboard_models.Ticket.objects.bulk_update(tickets, ['rank'])

        return validated_data


class PokerboardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = pokerboard_models.Invite
        fields = ['id', 'type', 'invitee', 'pokerboard', 'group', 'role', 'is_accepted', 'group_name']
        extra_kwargs = {
            'type': {'write_only': True},
            'is_accepted': {'read_only': True},
            'group': {'read_only': True},
            # 'pokerboard': {'read_only': True}
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
        print(self.context.get('request'))
        type = attrs.get('type')
        pokerboard = attrs.get('pokerboard')
        if type==1:
            invitee = attrs.get('invitee')
            if pokerboard_models.Invite.objects.filter(pokerboard=pokerboard, invitee=invitee, group=None):
                raise serializers.ValidationError("User already invited")
        else:
            group_name = attrs.get('group_name')
            group = group_models.Group.objects.filter(name=group_name).first()
            if not group:
                raise serializers.ValidationError("Group does not exist")
            else:
                if pokerboard_models.Invite.objects.filter(pokerboard=pokerboard, group=group):
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
            pokerboard_models.Invite.objects.create(pokerboard=pokerboard, invitee=invitee, role=role)
        else:
            group = validated_data['group']
            group_name = validated_data['group_name']
            members = group_models.GroupMember.objects.filter(group=group)
            for member in members:
                pokerboard_models.Invite.objects.create(invitee=str(member.user), pokerboard=pokerboard, group=group, group_name=group_name, role=role)
        return validated_data
