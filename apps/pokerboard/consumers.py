from datetime import datetime
import json

from django.contrib.auth.models import AnonymousUser

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework import serializers

from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models,
    serializers as pokerboard_serializers,
    utils as pokerboard_utils,
)
from apps.user import serializers as user_serializers


class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Runs on connection initiate
        """
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
            return
        clients = getattr(self.channel_layer, self.room_group_name, [])
        clients.append(self.scope["user"])
        setattr(self.channel_layer, self.room_group_name, clients)
        await self.accept()

        serializer = user_serializers.UserSerializer(clients, many=True)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast',
                'message': {
                    'type': 'join',
                    'users': serializer.data
                }
            }
        )

    async def estimate(self, event):
        """
        Finalize estimation of a ticket
        """
        try:
            manager = self.session.ticket.pokerboard.manager
            if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
                self.session.status = pokerboard_models.GameSession.ESTIMATED
                self.session.save()
                ticket = self.session.ticket
                ticket.estimate = event["message"]["estimate"]

                url = f"{pokerboard_constants.JIRA_API_URL_V2}issue/{ticket.ticket_id}"
                data = json.dumps({
                    "update": {
                        'customfield_10016': [
                            {
                                "set": ticket.estimate
                            }
                        ]
                    }
                })
                pokerboard_utils.JiraApi.query_jira(
                    "PUT", url, payload=data, status_code=204)
                ticket.save()
                return {
                    "type": event["type"],
                    "estimate": event["message"]["estimate"]
                }
            else:
                await self.send(text_data=json.dumps({
                    "error": "Only manager can finalize estimate"
                }))
        except serializers.ValidationError as e:
            print(e)
            await self.send(text_data=json.dumps({
                "error": "Estimation failed"
            }))

    async def skip(self, event):
        """
        Skip current voting session
        """
        manager = self.session.ticket.pokerboard.manager
        if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
            self.session.status = pokerboard_models.GameSession.SKIPPED
            self.session.save()
            pokerboard_utils.moveTicketToEnd(self.session.ticket)
            return {
                "type": event["type"],
            }
        else:
            await self.send(text_data=json.dumps({
                "error": "Can't skip"
            }))
        

    async def initialise_game(self, event):
        """
        Initialise game, fetches connceted users and votes already given
        """
        votes = pokerboard_models.Vote.objects.filter(
            game_session=self.session)
        vote_serializer = pokerboard_serializers.VoteSerializer(
            instance=votes, many=True)
        clients = list(
            set(getattr(self.channel_layer, self.room_group_name, [])))
        serializer = user_serializers.UserSerializer(
            instance=clients, many=True)
        return {
            "type": event["type"],
            "votes": vote_serializer.data,
            "users": serializer.data,
            "timer": json.dumps(self.session.timer_started_at, default=self.myconverter)
        }

    async def vote(self, event):
        """
        Places/update a vote on a ticket
        """
        try:
            serializer = pokerboard_serializers.VoteSerializer(
                data=event["message"])
            serializer.is_valid(raise_exception=True)
            pokerboard_utils.validate_vote(
                self.session.ticket.pokerboard.estimation_type, serializer.validated_data["estimate"])
            serializer.save(game_session=self.session, user=self.scope["user"])
            return {
                "type": event["type"],
                "vote": serializer.data
            }
        except serializers.ValidationError as e:
            print(e)
            await self.send(text_data=json.dumps({
                "error": "Invalid estimate"
            }))

    async def start_timer(self, event):
        """
        Starts timer on current voting session
        """
        manager = self.session.ticket.pokerboard.manager
        if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
            now = datetime.now()
            self.session.timer_started_at = now
            self.session.save()
            return {
                "type": event["type"],
                "timer_started_at": json.dumps(now, default=self.myconverter),
            }
        else:
            await self.send(text_data=json.dumps({
                "error": "Can't start timer"
            }))

    def myconverter(self, o):
        """
        convert datetime into json
        """
        if isinstance(o, datetime):
            return o.__str__()

    async def receive(self, text_data):
        """
        Runs on recieving any message, acts as a gateway of websocket communication
        """
        try:
            text_data_json = json.loads(text_data)
            serializer = pokerboard_serializers.MessageSerializer(
                data=text_data_json)
            serializer.is_valid(raise_exception=True)
            message = text_data_json['message']
            message_type = text_data_json['message_type']
            method_to_call = getattr(self, message_type)
            res = await method_to_call({
                'type': message_type,
                'message': message,
                'user': self.scope["user"].id
            })
            # Send message to room group
            if res:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'broadcast',
                        'message': res
                    }
                )
        except serializers.ValidationError:
            await self.send(text_data=json.dumps({
                "error": "Something went wrong"
            }))

    async def broadcast(self, event):
        """
        Broadcast a message to connected channels in current group
        """
        await self.send(text_data=json.dumps(event["message"]))

    async def disconnect(self, code):
        """
        Runs when a user disconnects
        """
        clients = getattr(self.channel_layer, self.room_group_name, [])
        clients.remove(self.scope["user"])
        setattr(self.channel_layer, self.room_group_name, clients)
        serializer = user_serializers.UserSerializer(
            list(set(clients)), many=True)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast',
                'message': {
                    'type': 'leave',
                    'users': serializer.data
                }
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
