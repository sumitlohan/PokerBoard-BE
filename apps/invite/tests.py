from apps import pokerboard
from apps import group
import poker
from django.contrib.auth import get_user_model
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

from apps.group import models as group_models
from apps.invite import models as invite_models
from apps.pokerboard import models as pokerboard_models
from apps.user import models as user_models


class InviteTestCases(APITestCase):
    """
    Invite testcases for testing invitee list, details and add/remove invitee functionality
    """
    INVITE_URL = reverse('invite')
    REMOVE_MEMBER_URL = reverse('remove-invitee')
    MEMBERS_URL = reverse('members')

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        self.token = G(user_models.Token, user=self.user)
        self.group = G(group_models.Group, created_by=self.user, name="Dummy Group")
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user, name="Dummy Pokerboard")
        self.invite_user = G(invite_models.Invite, invitee=self.user.email, group_name=None,
                            pokerboard=self.pokerboard, role=invite_models.Invite.CONTRIBUTOR)
        self.invite_group = G(invite_models.Invite, invitee=None, group=self.group.name,
                            pokerboard=self.pokerboard, role=invite_models.Invite.CONTRIBUTOR)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_invite_user(self):
        """
        Invites user
        """
        data = {
            "invitee": "test@gmail.com",
            "pokerboard": self.pokerboard,
            "group_name": None,
            "role": invite_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        invite = invite_models.Invite.objects.get(invitee=data["invitee"], group_name=None)
        expected_data = {
            "invitee": invite.invitee,
            "pokerboard": invite.pokerboard,
            "role": invite.role,
            "group_name": invite.group_name,
        }
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, response.data)

    def test_invite_group(self):
        """
        Invites group
        """
        data = {
            "invitee": None,
            "pokerboard": self.pokerboard,
            "group_name": "Dummy Group",
            "role": invite_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        invite = invite_models.Invite.objects.get(invitee=data["invitee"], group_name=data["group_name"])
        expected_data = {
            "invitee": invite.invitee,
            "role": invite.role,
            "group": invite.group,
            "group_name": invite.group_name,
            "pokerboard": invite.pokerboard
        }
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, response.data)

    def test_user_already_invited(self):
        """
        Expects 400 response code on inviting already invited user
        """
        data = {
            "invitee": self.invite_user.invitee,
            "pokerboard": self.pokerboard,
            "group_name": None,
            "role": invite_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        expected_data = {
            "non_field_errors":[
                "User already invited"
            ]
        }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)
    
    def test_group_already_invited(self):
        """
        Expects 400 response code on inviting already invited group
        """
        data = {
            "invitee": None,
            "pokerboard": self.pokerboard,
            "group_name": self.invite_group.group_name,
            "role": invite_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        expected_data = {
            "non_field_errors":[
                "Group already invited"
            ]
        }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)
    
    def test_group_does_not_exist(self):
        """
        Expects 400 response code on inviting a group which does not exist
        """
        data = {
            "invitee": None,
            "pokerboard": self.pokerboard,
            "group_name": "Some unknown group",
            "role": invite_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        expected_data = {
            "non_field_errors":[
                "Group does not exist"
            ]
        }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)
    