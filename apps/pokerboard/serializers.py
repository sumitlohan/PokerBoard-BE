import json
from django.db import models
import requests

from django.conf import settings

from rest_framework import serializers

from apps.pokerboard.models import Pokerboard, Ticket
from apps.user.serializers import UserSerializer


class TicketSerializer(serializers.ModelSerializer):
    """
    Pokerboard serializer
    """
    class Meta:
        model = Ticket
        fields = "__all__"


class PokerboardSerializer(serializers.ModelSerializer):
    """
    Pokerboard serializer
    """
    tickets = TicketSerializer(many=True, read_only=True)
    manager = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Pokerboard
        fields = ["id", "title", "description", "estimation_type", "duration", "manager", "status", "tickets", "created_at"]
        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "created_at": {
                "read_only": True
            },
            "status": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        tickets = attrs["tickets"]
        ticket_ids = json.dumps(tickets)[1:-1]
        jql = f"issue IN ({ticket_ids})"
        url = f"{settings.JIRA_URL}search?jql={jql}"

        response = requests.request("GET", url, headers=settings.JIRA_HEADERS)
        if response.status_code!=200:
            raise serializers.ValidationError("Invalid ticket")
        return super().validate(attrs)
    
    def create(self, validated_data):
        tickets = validated_data.pop("tickets")
        pokerboard = super().create(validated_data)

        for idx, ticket in enumerate(tickets):
            Ticket.objects.create(pokerboard=pokerboard, ticket_id=ticket, rank=idx+1)

        return pokerboard

class CreatePokerboardSerializer(serializers.ModelSerializer):
    """
    Pokerboard serializer
    """
    tickets = serializers.ListField(child=serializers.SlugField(), write_only=True)
    manager = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Pokerboard
        fields = ["id", "title", "description", "estimation_type", "duration", "manager", "status", "tickets", "created_at"]
        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "created_at": {
                "read_only": True
            },
            "status": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        tickets = attrs["tickets"]
        ticket_ids = json.dumps(tickets)[1:-1]
        jql = f"issue IN ({ticket_ids})"
        url = f"{settings.JIRA_URL}search?jql={jql}"

        response = requests.request("GET", url, headers=settings.JIRA_HEADERS)
        if response.status_code!=200:
            raise serializers.ValidationError("Invalid ticket")
        return super().validate(attrs)
    
    def create(self, validated_data):
        tickets = validated_data.pop("tickets")
        pokerboard = super().create(validated_data)

        for idx, ticket in enumerate(tickets):
            Ticket.objects.create(pokerboard=pokerboard, ticket_id=ticket, rank=idx+1)

        return pokerboard


class CommentSerializer(serializers.Serializer):
    """
    Comment serializer with comment and the issue to comment on
    """
    comment = serializers.CharField()
    issue = serializers.SlugField()


class TicketOrderSerializer(serializers.ModelSerializer):
    direction = serializers.CharField()

    class Meta:
        model = Ticket
        fields = ["direction"]

    def update(self, instance, validated_data):
        rank = instance.rank
        direction = validated_data["direction"]
        second_rank = rank -1 if direction == "UP" else rank+1
        second_ticket = Ticket.objects.filter(pokerboard=instance.pokerboard, rank=second_rank).first()
        if not second_ticket:
            raise serializers.ValidationError(f"Can't go {direction}")
        second_ticket.rank = rank
        instance.rank = second_rank
        second_ticket.save()
        instance.save()
        return validated_data

