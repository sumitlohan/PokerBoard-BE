import json
import requests

from django.conf import settings

from rest_framework import serializers

from apps.pokerboard.models import Pokerboard
from apps.user.serializers import UserSerializer


class PokerboardSerializer(serializers.ModelSerializer):
    """
    Pokerboard serializer
    """
    tickets = serializers.ListField(child=serializers.SlugField(),write_only=True)
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
        # TODO : for each ticket code, create a Ticket object

        return super().create(validated_data)


class CommentSerializer(serializers.Serializer):
    """
    Comment serializer with comment and the issue to comment on
    """
    comment = serializers.CharField()
    issue = serializers.SlugField()
