import json
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.http import response
from django.urls import reverse
from django.utils.http import urlencode

from ddf import G
from rest_framework.test import APITestCase

from apps.group import models as group_models
from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models
)
from apps.pokerboard.tests import mock_data as pokerboard_mock_data
from apps.user import models as user_models


class PokerboardTestCases(APITestCase):
    """
    Test Pokerboard API. 
    """
    POKERBOARD_URL = reverse('pokerboards-list')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

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
        self.assertEqual(response.status_code, 201)
        pokerboard = pokerboard_models.Pokerboard.objects.filter(title=data["title"]).first()
        self.assertIsNotNone(pokerboard)
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


class SuggestionsTestCases(APITestCase):
    """
    Test Suggestion API
    """
    SUGGESTIONS_URL = reverse('suggestions')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_suggestions(self: APITestCase) -> None:
        """
        Test get pokerboard and sprint suggestions
        """
        response = self.client.get(self.SUGGESTIONS_URL)
        res_data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(res_data["sprints"]), list)
        self.assertEqual(type(res_data["projects"]), list)


class TicketOrderTestCases(APITestCase):
    """
    Test ticket order API
    """

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user)
        self.tickets = [
            G(pokerboard_models.Ticket, pokerboard=self.pokerboard, rank=1),
            G(pokerboard_models.Ticket, pokerboard=self.pokerboard, rank=2),
        ]

    def test_order_tickets(self: APITestCase) -> None:
        """
        Test change ticket ordering
        """
        ranks = [2, 1]
        data = []
        expected_data = []
        for ticket, rank in zip(self.tickets, ranks):
            obj = {
                "ticket_id": ticket.ticket_id,
                "rank": rank
            }
            data.append(obj)
            expected_obj = {
                "ticket_id": ticket.ticket_id,
                "rank": rank,
                "estimate": None
            }
            expected_data.append(expected_obj)
        url = reverse("order-tickets", args=[self.pokerboard.id])
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_data, response.data)

    def test_order_tickets_without_ticket_id(self: APITestCase) -> None:
        """
        Test change ticket ordering without ticket Id's
        """
        ranks = [2, 1]
        data = []
        expected_data = [
            {
                "ticket_id": [
                    "This field is required."
                ]
            },
            {
                "ticket_id": [
                    "This field is required."
                ]
            },
        ]
        for ticket, rank in zip(self.tickets, ranks):
            obj = {
                "rank": rank
            }
            data.append(obj)

        response = self.client.put(reverse("order-tickets", args=[self.pokerboard.id]), data=data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertListEqual(expected_data, response.data)

    def test_order_tickets_without_ranks(self: APITestCase) -> None:
        """
        Test change ticket ordering without ranks
        """
        ranks = [2, 1]
        data = []
        expected_data = [
            {
                "rank": [
                    "This field is required."
                ]
            },
            {
                "rank": [
                    "This field is required."
                ]
            },
        ]
        for ticket, rank in zip(self.tickets, ranks):
            obj = {
                "ticket_id": ticket.ticket_id
            }
            data.append(obj)

        response = self.client.put(reverse("order-tickets", args=[self.pokerboard.id]), data=data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertListEqual(expected_data, response.data)



class JqlTestCases(APITestCase):
    """
    Test jql API
    """
    JQL_URL = reverse('jql')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    @patch("apps.pokerboard.utils.requests.request")
    def test_search_jql(self: APITestCase, mock_get: Mock) -> None:
        """
        Creates group, check for it's name and default group member
        """
        kwargs = {
            "jql": "issue IN (KD-1, KD-2)"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(pokerboard_mock_data.JQL_RESPONSE)
        response = self.client.get(f"{self.JQL_URL}?{urlencode(kwargs)}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, pokerboard_mock_data.JQL_RESPONSE)


class CommentTestCases(APITestCase):
    """
    Test get comment and post comment API
    """
    COMMENTS_URL = reverse('comment')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    @patch("apps.pokerboard.utils.requests.request")
    def test_get_comments(self: APITestCase, mock_get: Mock) -> None:
        """
        Test Get comments for an issue
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(pokerboard_mock_data.COMMENTS_REPONSE)
        response = self.client.get(f"{self.COMMENTS_URL}?issueId=KD-4")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.data, pokerboard_mock_data.COMMENTS_REPONSE["comments"])

    @patch("apps.pokerboard.utils.requests.request")
    def test_post_comments(self: APITestCase, mock_get: Mock) -> None:
        """
        Test post comment on an issue
        """
        data = {
            "comment": "Hello there",
            "issue": "KD-2"
        }
        mock_get.return_value.status_code = 201
        mock_get.return_value.text = "{}"
        response = self.client.post(self.COMMENTS_URL, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, data)

    def test_post_comments_with_invalid_comment(self: APITestCase) -> None:
        """
        Test post comment with invalid comment
        """
        data = {
            "comment": "",
            "issue": "KD-2"
        }
        expected_data = {
            "comment": [
                "This field may not be blank."
            ]
        }
        response = self.client.post(self.COMMENTS_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(expected_data, response.data)


class InviteTestCases(APITestCase):
    """
    Invite testcases for testing invitee list, details and add/remove invitee functionality
    """
    INVITE_URL = reverse('members-list')
    # ACCEPT_INVITE_URL = reverse('members-detail')
    # MEMBERS_URL = reverse('members')
    # REMOVE_MEMBER_URL = reverse('remove-invitee')

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        token = G(user_models.Token, user=self.user)
        self.group1 = G(group_models.Group, created_by=self.user, name="Dummy Group")
        self.group2 = G(group_models.Group, created_by=self.user, name="Dummy Group 2")
        self.pokerboard = G(pokerboard_models.Pokerboard, manager=self.user, title="Dummy Pokerboard")
        self.invite_user = G(pokerboard_models.Invite, type=pokerboard_models.Invite.EMAIL, invitee=self.user.email,
                            pokerboard=self.pokerboard.id, role=pokerboard_models.Invite.CONTRIBUTOR)
        self.invite_group = G(pokerboard_models.Invite, type=pokerboard_models.Invite.GROUP, group=self.group1, group_name=self.group1.name,
                            pokerboard=self.pokerboard.id, role=pokerboard_models.Invite.CONTRIBUTOR)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_invite_user(self):
        """
        Invites user
        """
        data = {
            "type": pokerboard_models.Invite.EMAIL,
            "invitee": "test@gmail.com",
            "pokerboard": self.pokerboard.id,
            "role": pokerboard_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        invite = pokerboard_models.Invite.objects.get(invitee=data["invitee"], group_name=None)
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
            "type": pokerboard_models.Invite.GROUP,
            "group": self.group2,
            "group_name": self.group2.name,
            "pokerboard": self.pokerboard.id,
            "role": pokerboard_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        invite = pokerboard_models.Invite.objects.filter(pokerboard=data["pokerboard"], group_name=data["group_name"]).first()
        expected_data = {
            "invitee": None,
            "pokerboard": invite.pokerboard.id,
            "role": invite.role,
            "group": invite.group.id,
            "group_name": invite.group_name
        }
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, response.data)

    def test_user_already_invited(self):
        """
        Expects 400 response code on inviting already invited user
        """
        data = {
            "type": pokerboard_models.Invite.EMAIL,
            "invitee": self.invite_user.invitee,
            "pokerboard": self.invite_user.pokerboard.id,
            "role": pokerboard_models.Invite.CONTRIBUTOR
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
            "type": pokerboard_models.Invite.GROUP,
            "group": self.group1.id,
            "group_name": self.group1.name,
            "pokerboard": self.pokerboard.id,
            "role": pokerboard_models.Invite.CONTRIBUTOR
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
            "type": pokerboard_models.Invite.GROUP,
            "group": 3,
            "group_name": "Some unknown group",
            "pokerboard": self.pokerboard.id,
            "role": pokerboard_models.Invite.CONTRIBUTOR
        }
        response = self.client.post(self.INVITE_URL, data=data)
        expected_data = {
            "non_field_errors":[
                "Group does not exist"
            ]
        }
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)

    def test_invite_user_failure_incorrect_invitee(self):
        """
        Expects 400 response code on incorrect invitee email address
        """
        data = {
            "type": pokerboard_models.Invite.EMAIL,
            "invitee": "test",
            "pokerboard": self.pokerboard.id,
            "role": pokerboard_models.Invite.CONTRIBUTOR
        }
        expected_data = {
            "invitee": [
                "Enter a valid email address."
            ]
        }
        response = self.client.post(self.INVITE_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)
    
    def test_invalid_role(self):
        """
        Expects 400 response code on invalid role
        """
        data = {
            "type": pokerboard_models.Invite.EMAIL,
            "invitee": "test@gmail.com",
            "pokerboard": self.pokerboard.id,
            "role": 3
        }
        expected_data = {
            "role": [
                "\"3\" is not a valid choice."
            ]
        }
        response = self.client.post(self.INVITE_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_data)

    def test_accept_invite(self):
        """
        Expects 200 response code when requested by correct user
        """
        response = self.client.put(reverse('members-detail', args=[self.invite_user.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_members(self):
        """
        Get members of a pokerboard who have accepted invitation
        """
        self.invite_user.is_accepted = True
        self.invite_user.save()
        response = self.client.get(reverse('members-detail', args=[self.pokerboard.id]))
        expected_member = pokerboard_models.Invite.objects.get(pokerboard=self.pokerboard, is_accepted=True)
        expected_data = [
            {
                "id": expected_member.id,
                "invitee": expected_member.invitee,
                "pokerboard": expected_member.pokerboard.id,
                "group": expected_member.group,
                "role": expected_member.role,
                "is_accepted": expected_member.is_accepted,
                "group_name": expected_member.group_name
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_data, response.data)

    def test_remove_member(self):
        """
        Expects 200 response code when member is deleted
        """
        response = self.client.delete(reverse('members-detail', args=[self.invite_user.id]))
        self.assertEqual(response.status_code, 200)
