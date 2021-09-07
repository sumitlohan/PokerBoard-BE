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

    def test_create_group_unique_name(self):
        """
        Creates group, expects 400 response code on non-unique name
        """
        group_models.Group.objects.create(created_by=self.user, name="Dominos")
        data = {
            "name": "Dominos"
        }
        response = self.client.post(self.GROUP_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_group_failure_empty_name(self):
        """
        Create group, expects bad request on empty group name
        """
        data = {
            "name": ""
        }
        response = self.client.post(self.GROUP_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_group_failure_no_name(self):
        """
        Create group, expects bad request on no group name
        """
        data = {}
        response = self.client.post(self.GROUP_URL, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_list_group(self):
        """
        Get group list, checks for only group's name
        """
        group_models.Group.objects.create(created_by=self.user, name="Kung fu panda")
        response = self.client.get(self.GROUP_URL)
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_data), 1)
        group = res_data[0]
        self.assertEqual(group["name"], "Kung fu panda")

    def test_get_group_details(self):
        """
        Get group details by groupId, Expects 200 response code
        """
        group = group_models.Group.objects.create(created_by=self.user, name="Kung fu panda")
        response = self.client.get(reverse('groups-detail', args=[group.id]))
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        member = res_data["members"][0]["user"]
        self.assertEqual(res_data["name"], "Kung fu panda")
        self.assertEqual(res_data["created_by"], self.user.id)
        self.assertEqual(len(res_data["members"]), 1)
        self.assertEqual(member["email"], self.user.email)

    def test_get_group_details_failure(self):
        """
        Get group details by groupId, Expects 404 on invalid groupId
        """
        response = self.client.get(reverse('groups-detail', args=[7]))
        self.assertEqual(response.status_code, 404)

    def test_add_member_to_group(self):
        """
        Add member to group, Expects 201 response code
        """
        group = group_models.Group.objects.create(created_by=self.user, name="Kung fu panda")
        user = user_models.User.objects.create(email="sample@sample.com", password="Qwerty*1234")
        data = {
            "group": group.id,
            "email": user.email
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data, format='json')
        res_data = response.data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(res_data["group"], group.id)
        self.assertEqual(type(res_data["user"]), OrderedDict)
        self.assertEqual(res_data["user"]["id"], user.id)

    def test_add_member_failure_no_email(self):
        """
        Add member to group, Expects 400 response code on not providing email
        """
        group = group_models.Group.objects.create(created_by=self.user, name="Kung fu panda")
        data = {
            "group": group.id
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_add_member_failure_no_group(self):
        """
        Add member to group, Expects 400 response code on not providing group
        """
        user = user_models.User.objects.create(email="sample@sample.com", password="Qwerty*1234")
        data = {
            "email": user.email
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_add_member_multiple_times(self):
        """
        Add member to group, Expects 400 response code on adding a member two times
        """
        group = group_models.Group.objects.create(created_by=self.user, name="Kung fu panda")
        data = {
            "group": group.id,
            "email": self.user.email
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_add_member_for_non_existing_member(self):
        """
        Add member to group, Expects 400 response code on providing unregistered email
        """
        group = group_models.Group.objects.create(created_by=self.user, name="Kung fu panda")
        data = {
            "group": group.id,
            "email": "dummy@dummy.com"
        }
        response = self.client.post(self.CREATE_MEMBER_URL, data=data, format='json')
        self.assertEqual(response.status_code, 400)
