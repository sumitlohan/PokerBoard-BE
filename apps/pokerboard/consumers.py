import json
from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework import serializers

from apps.pokerboard import (
    models as pokerboard_models,
    serializers as pokerboard_serializers,
    utils as pokerboard_utils,
)
from apps.user import serializers as user_serializers


class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        session_id = self.scope['url_route']['kwargs']['pk']
        self.room_name = str(session_id)
        self.room_group_name = 'session_%s' % self.room_name
        session = pokerboard_models.GameSession.objects.get(id=session_id)
        self.session = session

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        if type(self.scope["user"]) == AnonymousUser or session.status != pokerboard_models.GameSession.IN_PROGRESS:
            await self.close()
        clients = getattr(self.channel_layer, self.room_group_name, [])
        if not len(clients):
            setattr(self.channel_layer, self.room_group_name, [self.scope["user"]])
        else:
            
            clients.append(self.scope["user"])
            setattr(self.channel_layer, self.room_group_name, clients)
        await self.accept()

    async def estimate(self, event):
        try:
            manager = self.session.ticket.pokerboard.manager
            if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
                self.session.status = pokerboard_models.GameSession.ESTIMATED
                self.session.save()
                ticket = self.session.ticket
                ticket.estimate = event["message"]["estimate"]

                # TODO: replace this url with constants url
                url = f"https://kaam-dhandha.atlassian.net/rest/api/2/issue/{ticket.ticket_id}"
                data = json.dumps({
                    "update": {
                        'customfield_10016': [
                            {
                                "set": ticket.estimate
                            }
                        ]
                    }
                })
                pokerboard_utils.query_jira("PUT", url, payload=data, status_code=204)
                ticket.save()
                await self.send(text_data=json.dumps({
                    "type": event["type"],
                    "estimate": event["message"]["estimate"]
                }))
        except serializers.ValidationError as e:
            await self.send(text_data=json.dumps({
                "error": "Estimation failed"
            }))

    async def skip(self, event):
        manager = self.session.ticket.pokerboard.manager
        if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
            self.session.status = pokerboard_models.GameSession.SKIPPED
            self.session.save()
            await self.send(text_data=json.dumps({
                "type": event["type"],
            }))
    
    async def initialise_game(self, event):
        votes = pokerboard_models.Vote.objects.filter(game_session=self.session)
        vote_serializer = pokerboard_serializers.VoteSerializer(instance=votes, many=True)
        clients = list(set(getattr(self.channel_layer, self.room_group_name, [])))
        serializer = user_serializers.UserSerializer(instance=clients, many=True)
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "votes": vote_serializer.data,
            "users": serializer.data
        }))


    async def vote(self, event):
        try:
            serializer = pokerboard_serializers.VoteSerializer(data=event["message"])
            serializer.is_valid(raise_exception=True)
            pokerboard_utils.validate_vote(self.session.ticket.pokerboard.estimation_type, serializer.validated_data["estimate"])

            serializer.save(game_session=self.session, user=self.scope["user"])
            await self.send(text_data=json.dumps({
                "type": event["type"],
                "vote":serializer.data
            }))
        except IntegrityError as e:
            await self.send(text_data=json.dumps({
                "error": "A user can't vote two times on a ticket"
            }))
        except serializers.ValidationError as e:
            print(e)
            await self.send(text_data=json.dumps({
                "error": "Invalid estimate"
            }))

    async def start_timer(self, event):
        manager = self.session.ticket.pokerboard.manager
        if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
            now = datetime.now()
            self.session.timer_started_at = now
            self.session.save()
            await self.send(text_data=json.dumps({
                "type": event["type"],
            }))

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            serializer = pokerboard_serializers.MessageSerializer(data=text_data_json)
            serializer.is_valid(raise_exception=True)
            message = text_data_json['message']
            message_type = text_data_json['message_type']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': message_type,
                    'message': message
                }
            )
        except serializers.ValidationError:
            await self.send(text_data=json.dumps({
                "error": "Something went wrong"
            }))

    async def disconnect(self, code):
        clients = getattr(self.channel_layer, self.room_group_name, [])
        clients.remove(self.scope["user"])
        setattr(self.channel_layer, self.room_group_name, clients)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
