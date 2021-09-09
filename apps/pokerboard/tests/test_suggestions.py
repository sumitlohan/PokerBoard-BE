from django.contrib.auth import get_user_model
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

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

    def test_get_all_sprints(self: APITestCase) -> None:
        """
        Test get all sprints
        """
        suggestions = pokerboard_utils.get_all_sprints()
        self.assertEqual(type(suggestions), list)
