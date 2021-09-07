from collections import OrderedDict

from django.urls import reverse

from rest_framework.test import APITestCase

import apps.group.models as group_models
import apps.user.models as user_models


class GroupTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    GROUP_URL = reverse('groups-list')
    CREATE_MEMBER_URL = reverse('create-members')

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

    def test_create_group(self):
        """
        Creates group, check for it's name and default group member
        """
        data = {
            "name": "Dominos"
        }
        response = self.client.post(self.GROUP_URL, data=data, format="json")
        res_data = response.data
        member = res_data["members"][0]["user"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(res_data["name"], data["name"])
        self.assertEqual(res_data["created_by"], self.user.id)
        self.assertEqual(len(res_data["members"]), 1)
        self.assertEqual(member["email"], self.user.email)
