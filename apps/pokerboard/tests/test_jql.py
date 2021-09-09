from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlencode

from ddf import G
from rest_framework.test import APITestCase

from apps.user import models as user_models


class JqlTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    JQL_URL = reverse('jql')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        self.token = G(user_models.Token, user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_search_jql(self: APITestCase) -> None:
        """
        Creates group, check for it's name and default group member
        """
        kwargs = {
            "jql": "issue IN (KD-1, KD-2)"
        }
        response = self.client.get(f"{self.JQL_URL}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["issues"]), 2)

    def test_search_jql_for_invalid_jql(self: APITestCase) -> None:
        """
        Creates group, check for it's name and default group member
        """
        kwargs = {
            "jql": "issue IN "
        }
        expected_data = [
            "Error in JQL Query: Expecting either a value, list or function before the end of the query."
        ]
        response = self.client.get(f"{self.JQL_URL}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 400)
        self.assertListEqual(expected_data, response.data)
