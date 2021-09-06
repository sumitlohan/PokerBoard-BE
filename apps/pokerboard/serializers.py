import json
from typing import Any
from typing_extensions import OrderedDict

from django.conf import settings

from rest_framework import serializers

import apps.pokerboard.models as pokerboard_models
import apps.pokerboard.utils as pokerbord_utils
from apps.pokerboard.constants import MESSAGE_TYPES
import apps.user.serializers as user_serializers

class TicketSerializer(serializers.ModelSerializer):
    """
    Ticket serializer for displaing ticket details
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
        ticket_ids = json.dumps(tickets)[1:-1]
        jql = f"issue IN ({ticket_ids})"
        url = f"{settings.JIRA_URL}search?jql={jql}"

        response = pokerbord_utils.query_jira("GET", url)
        request = self.context.get("request")
        manager = request.user
        attrs["manager"] = manager
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


class TicketOrderSerializer(serializers.ModelSerializer):
    """
    Ticket order serializer for moving tickets UP and DOWN in ranks.
    """
    direction = serializers.CharField()

    class Meta:
        model = pokerboard_models.Ticket
        fields = ["direction"]

    def update(self: serializers.ModelSerializer, instance: pokerboard_models.Ticket, validated_data: OrderedDict) -> OrderedDict:
        """
        Updates the rank of a ticket
        """
        rank = instance.rank
        direction = validated_data["direction"]
        second_rank = rank -1 if direction == "UP" else rank+1
        second_ticket = pokerboard_models.Ticket.objects.filter(pokerboard=instance.pokerboard, rank=second_rank).first()
        if not second_ticket:
            raise serializers.ValidationError(f"Can't go {direction}")
        second_ticket.rank = rank
        instance.rank = second_rank
        second_ticket.save()
        instance.save()
        return validated_data

class VoteSerializer(serializers.ModelSerializer):
    user = user_serializers.UserSerializer(read_only=True)
    class Meta:
        model = pokerboard_models.Vote
        fields = ["estimate", "game_session", "id", "user"]
        extra_kwargs = {
            "game_session": {
                "read_only": True
            }
        }

class GameSessionSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()
    
    class Meta:
        model = pokerboard_models.GameSession
        fields = ["id", "ticket", "status", "timer_started_at"]
        extra_kwargs = {
            "timer_started_at": {
                "required": False
            }
        }

    

class CreateGameSessionSerializer(GameSessionSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=pokerboard_models.Ticket.objects.only("id"))
    status = serializers.ChoiceField(choices=pokerboard_models.GameSession.STATUS_CHOICES, required=False)

    def validate_ticket(self, attrs):
        active_sessions = pokerboard_models.GameSession.objects.filter(ticket__pokerboard=attrs.pokerboard, status=pokerboard_models.GameSession.IN_PROGRESS).count()
        if active_sessions > 0:
            raise serializers.ValidationError("An active game session already exists for this pokerboard")
        return attrs

    def create(self, validated_data):
        validated_data["status"] = pokerboard_models.GameSession.IN_PROGRESS
        validated_data["timer_started_at"] = None
        return super().create(validated_data)

class MessageSerializer(serializers.Serializer):
    message_type = serializers.ChoiceField(choices=MESSAGE_TYPES)
    message = serializers.OrderedDict()
