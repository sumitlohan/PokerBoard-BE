from django.contrib.auth import get_user_model
from django.db.models.fields import EmailField
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase
from apps import pokerboard
from apps import group

from apps.group import models as group_models
from apps.invite import models as invite_models
from apps.pokerboard import models as pokerboard_models
from apps.user import models as user_models


class InviteTestCases(APITestCase):
    """
    Invite testcases for testing invitee list, details and add/remove invitee functionality
    """
    INVITE_URL = reverse('members-list')
    # ACCEPT_INVITE_URL = reverse('accept-invite')
    # MEMBERS_URL = reverse('members')
    # REMOVE_MEMBER_URL = reverse('remove-invitee')

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.group = G(group_models.Group, created_by=self.user, name="Dummy Group")
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user, title="Dummy Pokerboard")
        self.invite_user = G(invite_models.Invite, type=invite_models.Invite.EMAIL, invitee=self.user.email,
                            pokerboard=self.pokerboard.id, role=invite_models.Invite.CONTRIBUTOR)
        self.invite_group = G(invite_models.Invite, type=invite_models.Invite.GROUP, group=self.group, group_name=self.group.name,
                            pokerboard=self.pokerboard.id, role=invite_models.Invite.CONTRIBUTOR)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_invite_user(self):
        """
        Invites user
        """
        data = {
            "type": invite_models.Invite.EMAIL,
            "invitee": "test@gmail.com",
            "pokerboard": self.pokerboard.id,
            "role": invite_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        invite = invite_models.Invite.objects.get(invitee=data["invitee"], group_name=None)
        expected_data = {
            "invitee": invite.invitee,
            "pokerboard": invite.pokerboard.id,
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
            "type": invite_models.Invite.GROUP,
            "pokerboard": self.pokerboard.id,
            "group_name": "Dummy Group 2",
            "role": invite_models.Invite.CONTRIBUTOR
        }
        import pdb
        pdb.set_trace()
        response = self.client.post(self.INVITE_URL, data=data)
        invite = invite_models.Invite.objects.filter(pokerboard=data["pokerboard"], group_name=data["group_name"]).first()
        print(invite)
        expected_data = {
            "invitee": invite.invitee,
            "pokerboard": invite.pokerboard.id,
            "role": invite.role,
            "group": 1,
            "group_name": invite.group_name
        }
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, response.data)

    # def test_user_already_invited(self):
    #     """
    #     Expects 400 response code on inviting already invited user
    #     """
    #     data = {
    #         "type": invite_models.Invite.EMAIL,
    #         "invitee": self.invite_user.invitee,
    #         "pokerboard": self.invite_user.pokerboard.id,
    #         "role": invite_models.Invite.CONTRIBUTOR
    #     }
    #     response = self.client.post(self.INVITE_URL, data=data)
    #     expected_data = {
    #         "non_field_errors":[
    #             "User already invited"
    #         ]
    #     }
    #     self.assertEqual(response.status_code, 400)
    #     self.assertDictEqual(response.data, expected_data)
    
    # def test_group_already_invited(self):
    #     """
    #     Expects 400 response code on inviting already invited group
    #     """
    #     data = {
    #         "type": invite_models.Invite.GROUP,
    #         "pokerboard": self.pokerboard.id,
    #         "group_name": self.invite_group.group.name,
    #         "role": invite_models.Invite.CONTRIBUTOR
    #     }
    #     response = self.client.post(self.INVITE_URL, data=data)
    #     expected_data = {
    #         "non_field_errors":[
    #             "Group already invited"
    #         ]
    #     }
    #     self.assertEqual(response.status_code, 400)
    #     self.assertDictEqual(response.data, expected_data)
    
    # def test_group_does_not_exist(self):
    #     """
    #     Expects 400 response code on inviting a group which does not exist
    #     """
    #     data = {
    #         "type": invite_models.Invite.GROUP,
    #         "pokerboard": self.pokerboard.id,
    #         "group_name": "Some unknown group",
    #         "role": invite_models.Invite.CONTRIBUTOR
    #     }
    #     response = self.client.post(self.INVITE_URL, data=data)
    #     expected_data = {
    #         "non_field_errors":[
    #             "Group does not exist"
    #         ]
    #     }
    #     self.assertEqual(response.status_code, 400)
    #     self.assertDictEqual(response.data, expected_data)

    # def test_invite_user_failure_empty_invitee(self):
    #     """
    #     Expects 400 response code on empty invitee name
    #     """
    #     data = {
    #         "type": invite_models.Invite.EMAIL,
    #         "invitee": "",
    #         "pokerboard": self.pokerboard.id,
    #         "role": invite_models.Invite.CONTRIBUTOR
    #     }
    #     expected_data = {
    #         "invitee": [
    #             "This field may not be blank."
    #         ]
    #     }
    #     response = self.client.post(self.INVITE_URL, data=data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertDictEqual(response.data, expected_data)

    # def test_invite_user_failure_incorrect_invitee(self):
    #     """
    #     Expects 400 response code on incorrect invitee email address
    #     """
    #     data = {
    #         "invitee": "test",
    #         "group_name": None,
    #         "pokerboard": self.pokerboard,
    #         "role": invite_models.Invite.CONTRIBUTOR
    #     }
    #     expected_data = {
    #         "invitee": [
    #             "Enter a valid email address."
    #         ]
    #     }
    #     response = self.client.post(self.INVITE_URL, data=data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertDictEqual(response.data, expected_data)
    
    # def test_invite_group_failure_empty_group_name(self):
    #     """
    #     Expects 400 response code on empty group name
    #     """
    #     data = {
    #         "invitee": None,
    #         "pokerboard": self.pokerboard,
    #         "group_name": "",
    #         "role": invite_models.Invite.CONTRIBUTOR
    #     }
    #     expected_data = {
    #         "group_name": [
    #             "This field may not be blank."
    #         ]
    #     }
    #     response = self.client.post(self.INVITE_URL, data=data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertDictEqual(response.data, expected_data)

    # def test_invalid_role(self):
    #     """
    #     Expects 400 response code on invalid role
    #     """
    #     data = {
    #         "invitee": "test@gmail.com",
    #         "pokerboard": self.pokerboard,
    #         "group_name": None,
    #         "role": 3
    #     }
    #     expected_data = {
    #         "role": [
    #             "\"3\" is not a valid choice."
    #         ]
    #     }
    #     response = self.client.post(self.GROUP_URL, data=data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertDictEqual(response.data, expected_data)

    # def test_accept_invite(self):
    #     pass

    # def test_get_members(self):
    #     """
    #     Get members of a pokerboard who have accepted invitation
    #     """
    #     response = self.client.get(self.MEMBERS_URL, self.pokerboard.id)
    #     expected_member = invite_models.Invite.objects.get(pokerboard=self.pokerboard, is_accepted=True)

    #     expected_data = [
    #         {
    #             "id": expected_member.id,
    #             "invitee": expected_member.invitee,
    #             "pokerboard": expected_member.pokerboard,
    #             "group": expected_member.group,
    #             "role": expected_member.role,
    #             "is_accepted": expected_member.is_accepted,
    #             "group_name": expected_member.group_name
    #         }
    #     ]
    #     self.assertEqual(response.status_code, 200)
    #     self.assertListEqual(expected_data, response.data)

    # def test_remove_member(self):
    #     pass
