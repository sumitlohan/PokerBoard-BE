from django.urls import reverse
from django.utils.http import urlencode

from rest_framework.test import APITestCase

from apps.user import models as user_models


class JqlTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    JQL_URL = reverse('jql')

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

    def test_search_jql(self):
        """
        Creates group, check for it's name and default group member
        """
        kwargs = {
            "jql": "issue IN (KD-1, KD-2)"
        }
        response = self.client.get(f"{self.JQL_URL}?{urlencode(kwargs)}")
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_data["issues"]), 2)

    def test_search_jql_for_invalid_jql(self):
        """
        Creates group, check for it's name and default group member
        """
        kwargs = {
            "jql": "issue IN "
        }
        response = self.client.get(f"{self.JQL_URL}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 400)