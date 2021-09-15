import json
from unittest.mock import patch
import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from channels.testing import WebsocketCommunicator
from ddf import G
from rest_framework.test import APITestCase

from apps.pokerboard import (
    models as pokerboard_models
)
from apps.user import models as user_models
from poker.asgi import application


class SessionTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    CREATE_SESSION_URL = reverse('create-game-session')
    GET_VOTES = reverse('votes')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        self.token = G(user_models.Token, user=self.user).key
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user)
        self.ticket = G(pokerboard_models.Ticket, pokerboard=self.pokerboard, estimate=6)


        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_session(self: APITestCase) -> None:
        """
        Test create pokerboard
        """
        data = {
            "ticket": self.ticket.id
        }
        response = self.client.post(self.CREATE_SESSION_URL, data=data)
        session = pokerboard_models.GameSession.objects.get(ticket=self.ticket)
        expected_data = {
            "id": session.id,
            "ticket": {
                "id": self.ticket.id,
                "ticket_id": self.ticket.ticket_id,
                "estimate": self.ticket.estimate,
                "rank": self.ticket.rank
            },
            "status": pokerboard_models.GameSession.IN_PROGRESS,
            "timer_started_at": None
        }
        
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, response.data)
    
    def test_create_session_without_title(self: APITestCase) -> None:
        """
        Test create pokerboard without title
        """
        data = {}
        expected_data = {
            "ticket": [
                "This field is required."
            ]
        }
        response = self.client.post(self.CREATE_SESSION_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_get_active_session_does_not_exist(self: APITestCase) -> None:
        """
        
        """
        expected_data = {
            "ticket": None,
            "status": None,
            "timer_started_at": None
        }
        response = self.client.get(reverse("active-game-session", args=[self.pokerboard.id]))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)

    def test_get_active_session(self: APITestCase) -> None:
        """
        
        """
        session = G(pokerboard_models.GameSession, ticket=self.ticket)
        expected_data = {
            "id": session.id,
            "ticket": {
                "id": self.ticket.id,
                "ticket_id": self.ticket.ticket_id,
                "estimate": self.ticket.estimate,
                "rank": self.ticket.rank,
            },
            "status": pokerboard_models.GameSession.IN_PROGRESS,
            "timer_started_at": session.timer_started_at
        }
        response = self.client.get(reverse("active-game-session", args=[self.pokerboard.id]))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)

    def test_get_votes(self: APITestCase) -> None:
        """
        
        """
        session = G(pokerboard_models.GameSession, ticket=self.ticket)
        vote = G(pokerboard_models.Vote, game_session=session, user=self.user)
        expected_data = [
            {
                "id": self.ticket.id,
                "ticket_id": self.ticket.ticket_id,
                "estimate": self.ticket.estimate,
                "rank": self.ticket.rank,
            },
        ]
        response = self.client.get(self.GET_VOTES)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_data, response.data)


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWebsocket:
    """
    Test websockets
    """
    @pytest.fixture
    def setup(self):
        """
        Setup a game session and user
        """
        self.user = G(get_user_model())
        self.token = user_models.Token.objects.create(user=self.user)
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user)
        self.ticket = G(pokerboard_models.Ticket, pokerboard=self.pokerboard, estimate=6)
        self.session = G(pokerboard_models.GameSession, ticket=self.ticket, status=pokerboard_models.GameSession.IN_PROGRESS)
    
    async def test_websocket_connect(self, setup):
        """
        Test websocket connection
        """
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={self.token.key}")
        connected, subprotocol = await communicator.connect()

        assert connected
        await communicator.receive_from()
 
    async def test_websocket_connect_cannot_connect_estimated_session(self, setup):
        """
        Test websocket connection incase of an estimated session
        """
        session_2 = G(pokerboard_models.GameSession, status=pokerboard_models.GameSession.ESTIMATED)
        communicator = WebsocketCommunicator(application, f"/session/{session_2.id}?token={self.token.key}")
        connected, subprotocol = await communicator.connect()

        assert not connected

    async def test_websocket_skip(self, setup):
        """
        Test skip message
        """
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={self.token.key}")
        connected, subprotocol = await communicator.connect()

        assert connected
        await communicator.receive_from()
        await communicator.send_json_to({"message_type": "skip", "message": "skip"})
        res = json.loads(await communicator.receive_from())
        expected_data = {"type": "skip"}
        assert res == expected_data

    async def test_websocket_skip_other_user_cannot_skip(self, setup):
        """
        Test skip message, only manager can skip
        """
        user_2 = G(get_user_model())
        token = G(user_models.Token, user=user_2)
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={token.key}")
        connected, subprotocol = await communicator.connect()

        assert connected
        await communicator.receive_from()
        await communicator.send_json_to({"message_type": "skip", "message": "skip"})
        res = json.loads(await communicator.receive_from())
        expected_data = {"error": "Can't skip"}
        assert res == expected_data
    
    async def test_websocket_initialise_game(self, setup):
        """
        Test initialise game
        """
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={self.token.key}")
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.receive_from()

        await communicator.send_json_to({"message_type": "initialise_game", "message": "initialise_game"})
        res = json.loads(await communicator.receive_from())
        expected_data = {
                            'type': 'initialise_game',
                            'votes': [],
                            'users': [
                                {'id': self.user.id,
                                'email': self.user.email,
                                'first_name': self.user.first_name,
                                'last_name': self.user.last_name
                                }
                            ],
                            'timer': 'null'
                        }
        assert res == expected_data

    async def test_websocket_start_timer(self, setup):
        """
        Test start timer message
        """
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={self.token.key}")
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.receive_from()

        await communicator.send_json_to({"message_type": "start_timer", "message": "start_timer"})
        res = json.loads(await communicator.receive_from())
        assert res["type"] == "start_timer"
        assert "timer_started_at" in res.keys()

    async def test_websocket_start_timer_other_user_cannot_start_timer(self, setup):
        """
        Test start timer message, only manager can start timer
        """
        user_2 = G(get_user_model())
        token = G(user_models.Token, user=user_2)
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={token.key}")
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.receive_from()

        await communicator.send_json_to({"message_type": "start_timer", "message": "start_timer"})
        res = json.loads(await communicator.receive_from())
        expected_data = {"error": "Can't start timer"}
        assert res == expected_data


    async def test_websocket_vote(self,setup):
        """
        Test vote message
        """
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={self.token.key}")
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.receive_from()

        await communicator.send_json_to({"message_type": "vote", "message": {"estimate": 6}})
        res = json.loads(await communicator.receive_from())
        vote = pokerboard_models.Vote.objects.get(user=self.user, game_session=self.session)
        assert vote
        expected_data = {
                            'type': 'vote',
                            'vote': {
                                "id": vote.id,
                                "estimate": vote.estimate,
                                "game_session": self.session.id,
                                'user': {
                                    'id': self.user.id,
                                    'email': self.user.email,
                                    'first_name': self.user.first_name,
                                    'last_name': self.user.last_name
                                },
                            },
                        }
        assert res == expected_data

    async def test_websocket_vote_invalid_estimate(self,setup):
        """
        Test vote message with invalid estimate
        """
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={self.token.key}")
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.receive_from()

        await communicator.send_json_to({"message_type": "vote", "message": {}})
        res = json.loads(await communicator.receive_from())
        expected_data = {'error': 'Invalid estimate'}
        assert res == expected_data

    async def test_websocket_estimate_other_user_cannot_estimate(self, setup):
        """
        Test estimate message, only manager can finalize estimate
        """
        user_2 = G(get_user_model())
        token = G(user_models.Token, user=user_2)
        communicator = WebsocketCommunicator(application, f"/session/{self.session.id}?token={token.key}")
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.receive_from()

        await communicator.send_json_to({"message_type": "estimate", "message": {"estimate": 6}})
        res = json.loads(await communicator.receive_from())
        expected_data = {"error": "Only manager can finalize estimate"}

    

