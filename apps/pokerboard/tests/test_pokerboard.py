from django.urls import reverse

from rest_framework.test import APITestCase

from apps.pokerboard import models as pokerboard_models
from apps.user import models as user_models


class PokerboardTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    POKERBOARD_URL = reverse('pokerboards-list')

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

    def test_create_pokerboard(self):
        data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "tickets": ["KD-1", "KD-2"]
        }
        expected_data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "status": "STARTED"
        }
        response = self.client.post(self.POKERBOARD_URL, data=data, format="json")
        res_data = response.data
        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset(expected_data, res_data)
        self.assertEqual(res_data["manager"]["email"], self.user.email)
        
    def test_create_pokerboard_without_title(self):
        data = {
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "tickets": ["KD-1", "KD-2"]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_pokerboard_without_description(self):
        data = {
            "title": "Marvel",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "tickets": ["KD-1", "KD-2"]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_pokerboard_without_tickets(self):
        data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
        }
        response = self.client.post(self.POKERBOARD_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_pokerboard_with_invalid_tickets(self):
        data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "tickets": ["KD-1", "K-2"]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_pokerboard_with_empty_tickets_array(self):
        data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "tickets": []
        }
        response = self.client.post(self.POKERBOARD_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    
    def test_pokerboard_details(self):
        kwargs = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "status": "STARTED",
            "manager": self.user,
        }
        expected_data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "status": "STARTED",
            "tickets": []
        }
        pokerboard = pokerboard_models.Pokerboard.objects.create(**kwargs)
        response = self.client.get(reverse("pokerboards-detail", args=[pokerboard.id]))
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(expected_data, res_data)
        self.assertEqual(res_data["manager"]["email"], self.user.email)

    def test_pokerboard_list(self):
        kwargs = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "status": "STARTED",
            "manager": self.user,
        }
        expected_data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": "FIBONACCI",
            "status": "STARTED"
        }
        pokerboard_models.Pokerboard.objects.create(**kwargs)

        response = self.client.get(self.POKERBOARD_URL)
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_data), 1)
        pokerboard_res = res_data[0]
        self.assertDictContainsSubset(expected_data, pokerboard_res)
        self.assertEqual(pokerboard_res["manager"]["email"], self.user.email)
