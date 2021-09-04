import json
from typing import Any
from typing_extensions import OrderedDict

from django.conf import settings
from django.db import connection

from rest_framework import serializers

import apps.pokerboard.constants as pokerboard_constants
import apps.pokerboard.models as pokerboard_models
import apps.pokerboard.utils as pokerbord_utils
import apps.user.serializers as user_serializers


class TicketSerializer(serializers.ModelSerializer):
    """
    Ticket serializer for displaying ticket details
    """

    class Meta:
        model = pokerboard_models.Ticket
        fields = ["id", "ticket_id", "pokerboard", "estimate", "rank"]


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
        tickets = attrs["tickets"]
        # removing [] from ["KD-1", "KD-2"]. ["KD-1", "KD-2"] -> "KD-1", "KD-2"
        ticket_ids = json.dumps(tickets)[1:-1]
        jql = f"issue IN ({ticket_ids})"
        url = f"{pokerboard_constants.JIRA_API_URL_V2}search?jql={jql}"

        # validate ticket Id's
        pokerbord_utils.query_jira("GET", url)
        attrs["manager"] = self.context.get("request").user
        return super().validate(attrs)
    
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
    def create(self, validated_data):
        print(len(connection.queries))
        tickets = [pokerboard_models.Ticket.objects.get(ticket_id=ticket.get('ticket_id')) for ticket in validated_data]
        for ticket, updated_ticket in zip(tickets, validated_data):
            ticket.rank = updated_ticket.get('rank')
        updated_tickets = pokerboard_models.Ticket.objects.bulk_update(tickets, ['rank'])
        print(len(connection.queries))

        return validated_data
