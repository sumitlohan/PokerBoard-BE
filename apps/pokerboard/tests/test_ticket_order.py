from django.contrib.auth import get_user_model
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

from apps.pokerboard import models as pokerboard_models
from apps.user import models as user_models


class TicketOrderTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    TICKETS_URL = reverse('tickets')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        self.token = G(user_models.Token, user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user)
        self.tickets = [
            G(pokerboard_models.Ticket, pokerboard=self.pokerboard, rank=1),
            G(pokerboard_models.Ticket, pokerboard=self.pokerboard, rank=2),
        ]

    def test_order_tickets(self: APITestCase) -> None:
        """
        Test change ticket ordering
        """
        ranks = [2,1]
        data = []
        expected_data = []
        for ticket, rank in zip(self.tickets, ranks):
            obj = {
                "ticket_id": ticket.ticket_id,
                "pokerboard": ticket.pokerboard.id,
                "rank": rank
            }
            data.append(obj)
            expected_obj = {
                "ticket_id": ticket.ticket_id,
                "pokerboard": ticket.pokerboard.id,
                "rank": rank,
                "estimate": None
            }
            expected_data.append(expected_obj)
        
        response = self.client.put(self.TICKETS_URL, data=data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_data, response.data)
