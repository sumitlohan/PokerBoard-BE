import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

from apps.pokerboard.tests import mock_data as pokerboard_mock_data
from apps.pokerboard import utils as pokerboard_utils
from apps.user import models as user_models


class SuggestionsTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    SUGGESTIONS_URL = reverse('suggestions')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        self.token = G(user_models.Token, user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_suggestions(self: APITestCase) -> None:
        """
        Test get pokerboard and sprint suggestions
        """
        response = self.client.get(self.SUGGESTIONS_URL)
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(res_data["sprints"]), list)
        self.assertEqual(type(res_data["projects"]), list)

    @patch("apps.pokerboard.utils.requests.request")
    def test_get_sprints(self: APITestCase, mock_get) -> None:
        """
        Test get sprints
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(pokerboard_mock_data.SPRINTS_RESPONSE)
        sprints = pokerboard_utils.get_sprints(1)
        self.assertEqual(sprints, pokerboard_mock_data.SPRINTS_RESPONSE["values"])

    @patch("apps.pokerboard.utils.requests.request")
    def test_get_boards(self: APITestCase, mock_get) -> None:
        """
        Test get boards
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(pokerboard_mock_data.BOARDS_RESPONSE)
        boards = pokerboard_utils.get_boards()
        self.assertEqual(boards, pokerboard_mock_data.BOARDS_RESPONSE["values"])

    @patch("apps.pokerboard.utils.get_boards")
    def test_get_all_sprints(self: APITestCase, boards_mock) -> None:
        """
        Test get all sprints
        """
        boards_mock.return_value = pokerboard_mock_data.BOARDS_RESPONSE["values"]
        with patch('requests.request') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = json.dumps(pokerboard_mock_data.SPRINTS_RESPONSE)
            sprints = pokerboard_utils.get_all_sprints()
            self.assertEqual(sprints, pokerboard_mock_data.SPRINTS_RESPONSE["values"])
