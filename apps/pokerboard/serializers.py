import json
from typing import Any
from typing_extensions import OrderedDict

from rest_framework import serializers

from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models,
    utils as pokerboard_utils
)
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
        pokerboard = validated_data[0]["pokerboard"]
        ticket_ids = list(map(lambda x: x["ticket_id"], validated_data))
        tickets = pokerboard_models.Ticket.objects.filter(ticket_id__in=ticket_ids, pokerboard=pokerboard).all()
        for ticket, updated_ticket in zip(tickets, validated_data):
            ticket.rank = updated_ticket.get('rank')
        updated_tickets = pokerboard_models.Ticket.objects.bulk_update(tickets, ['rank'])

        return validated_data
