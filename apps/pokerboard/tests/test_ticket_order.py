from django.urls import reverse

from rest_framework.test import APITestCase

from apps.pokerboard import models as pokerboard_models
from apps.user import models as user_models


class TicketOrderTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    TICKETS_URL = reverse('tickets')

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """
        data = {
            "email": "rohit@gmail.com",
            "password": "root",
            "first_name": "Rohit",
            "last_name": "Jain",
        }

        self.user = user_models.User.objects.create(**data)
        self.token = user_models.Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.pokerboard = pokerboard_models.Pokerboard(title="Marvel", description="Take down thanos", manager=self.user)
        # pokerboard_models.Ticket.objects.create(pokerboard=self.pokerboard)

    def test_order_tickets(self):
        pass
