from django.contrib.auth import get_user_model
from django.urls import reverse

from channels.testing import WebsocketCommunicator
from ddf import G
from rest_framework.test import APITestCase

from poker.asgi import application
from apps.pokerboard import (
    consumers as pokerboard_consumers,
    models as pokerboard_models
)
from apps.user import models as user_models


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
            "ticket": self.ticket.id,
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
            "ticket": {
                "ticket_id": "",
                "estimate": None,
                "rank": None,
            },
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

    async def test_websocket_connection(self: APITestCase) -> None:
        session = G(pokerboard_models.GameSession, ticket=self.ticket)

        communicator = WebsocketCommunicator(application, f"/session/{session.id}")
        connected, subprotocol = await communicator.connect()

        # await communicator.send_to(text_data="")
        assert connected
        await communicator.send_json_to({"message_type": "world"})
        res = await communicator.receive_from()
        print(res)
        pass

