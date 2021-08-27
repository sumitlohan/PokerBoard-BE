from apps.pokerboard.models import Pokerboard
from rest_framework import serializers


class PokerboardSerializer(serializers.ModelSerializer):
    """
    Pokerboard serializer
    """
    tickets = serializers.ListField(child=serializers.SlugField(),write_only=True)

    class Meta:
        model = Pokerboard
        fields = ["id", "title", "description", "estimation_type", "duration", "manager", "status", "tickets"]
        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "manager": {
                "read_only": True
            },
            "status": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        print(attrs)
        # TODO : validate tickets by calling api

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


