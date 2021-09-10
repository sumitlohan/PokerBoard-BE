from django.contrib.auth import get_user_model
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models
)
from apps.user import models as user_models


class PokerboardTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    POKERBOARD_URL = reverse('pokerboards-list')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        self.token = G(user_models.Token, user=self.user).key
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_pokerboard(self: APITestCase) -> None:
        """
        Test create pokerboard
        """
        data = {
            "title": "Avengers",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": pokerboard_models.Pokerboard.FIBONACCI,
            "tickets": ["KD-1", "KD-2"]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data)
        pokerboard = pokerboard_models.Pokerboard.objects.get(title=data["title"])
        expected_data = {
            "id": pokerboard.id,
            "title": pokerboard.title,
            "description": pokerboard.description,
            "duration": pokerboard.duration,
            "estimation_type": pokerboard.estimation_type,
            "status": pokerboard.status,
            "created_at": pokerboard.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
            "manager": {
                "id": pokerboard.manager.id,
                "email": pokerboard.manager.email,
                "first_name": pokerboard.manager.first_name,
                "last_name": pokerboard.manager.last_name,
            }
        }
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, response.data)

    def test_create_pokerboard_without_title(self: APITestCase) -> None:
        """
        Test create pokerboard without title
        """
        data = {
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": pokerboard_models.Pokerboard.FIBONACCI,
            "tickets": ["KD-1", "KD-2"]
        }
        expected_data = {
            "title": [
                "This field is required."
            ]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_pokerboard_without_description(self: APITestCase) -> None:
        """
        Test create pokerboard without description
        """
        data = {
            "title": "Marvel",
            "duration": 60,
            "estimation_type": pokerboard_models.Pokerboard.FIBONACCI,
            "tickets": ["KD-1", "KD-2"]
        }
        expected_data = {
            "description": [
                "This field is required."
            ]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_pokerboard_without_tickets(self: APITestCase) -> None:
        """
        Test create pokerboard without tickets
        """
        data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": pokerboard_models.Pokerboard.FIBONACCI,
        }
        expected_data = {
            "tickets": [
                "This field is required."
            ]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_pokerboard_with_invalid_tickets(self: APITestCase) -> None:
        """
        Test create pokerboard with invalid tickets
        """
        data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": pokerboard_models.Pokerboard.FIBONACCI,
            "tickets": ["KD-1", "K-2"]
        }
        expected_data = {
            "non_field_errors": [
                "The issue key 'K-2' for field 'issue' is invalid."
            ]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_create_pokerboard_with_empty_tickets_array(self: APITestCase) -> None:
        """
        Test create pokerboard with empty tickets array
        """
        data = {
            "title": "Marvel",
            "description": "Take down thanos",
            "duration": 60,
            "estimation_type": pokerboard_models.Pokerboard.FIBONACCI,
            "tickets": []
        }
        expected_data = {
            "tickets": [
                "This field is required."
            ]
        }
        response = self.client.post(self.POKERBOARD_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)

    def test_pokerboard_details(self: APITestCase) -> None:
        """
        Test get pokerboard details
        """
        expected_data = {
            "id": self.pokerboard.id,
            "title": self.pokerboard.title,
            "description": self.pokerboard.description,
            "duration": self.pokerboard.duration,
            "estimation_type": self.pokerboard.estimation_type,
            "status": self.pokerboard.status,
            "created_at": self.pokerboard.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
            "tickets": [],
            "manager": {
                "id": self.pokerboard.manager.id,
                "email": self.pokerboard.manager.email,
                "first_name": self.pokerboard.manager.first_name,
                "last_name": self.pokerboard.manager.last_name,
            }
        }
        response = self.client.get(reverse("pokerboards-detail", args=[self.pokerboard.id]))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)

    def test_pokerboard_list(self: APITestCase) -> None:
        """
        Test list pokerboards
        """
        expected_data = [
            {
                "id": self.pokerboard.id,
                "title": self.pokerboard.title,
                "description": self.pokerboard.description,
                "duration": self.pokerboard.duration,
                "estimation_type": self.pokerboard.estimation_type,
                "status": self.pokerboard.status,
                "created_at": self.pokerboard.created_at.strftime(pokerboard_constants.DATETIME_FORMAT),
                "tickets": [],
                "manager": {
                    "id": self.pokerboard.manager.id,
                    "email": self.pokerboard.manager.email,
                    "first_name": self.pokerboard.manager.first_name,
                    "last_name": self.pokerboard.manager.last_name,
                }
            }
        ]

        response = self.client.get(self.POKERBOARD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_data, response.data)
