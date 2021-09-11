import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

from apps.pokerboard.tests import mock_data as pokerboard_mock_data
from apps.user import models as user_models


class CommentTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    COMMENTS_URL = reverse('comment')

    def setUp(self: APITestCase) -> None:
        """
        Setup method for creating default user and it's token
        """
        self.user = G(get_user_model())
        self.token = G(user_models.Token, user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_comments(self: APITestCase) -> None:
        """
        Test Get comments for an issue
        """
        with patch("apps.pokerboard.utils.requests.request") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = json.dumps(pokerboard_mock_data.COMMENTS_REPONSE)
            response = self.client.get(f"{self.COMMENTS_URL}?issueId=KD-4")
            self.assertEqual(response.status_code, 200)
            self.assertListEqual(response.data, pokerboard_mock_data.COMMENTS_REPONSE["comments"])

    def test_post_comments(self: APITestCase) -> None:
        """
        Test post comment on an issue
        """
        data = {
            "comment": "Hello there",
            "issue": "KD-2"
        }
        with patch("apps.pokerboard.utils.requests.request") as mock_get:
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
