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

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """
        self.user = G(user_models.User)
        self.token = G(user_models.Token, user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_suggestions(self):
        response = self.client.get(self.SUGGESTIONS_URL)
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(res_data["sprints"]), list)
        self.assertEqual(type(res_data["projects"]), list)

    def test_get_all_sprints(self):
        suggestions = pokerboard_utils.get_all_sprints()
        self.assertEqual(type(suggestions), list)
