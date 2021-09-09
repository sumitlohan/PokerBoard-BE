from django.urls import reverse

from ddf import G
from rest_framework.test import APITestCase

from apps.user import models as user_models


class CommentTestCases(APITestCase):
    """
    Group testcases for testing group list, details and add member functionality
    """
    COMMENTS_URL = reverse('comment')

    def setUp(self):
        """
        Setup method for creating default user and it's token
        """
        self.user = G(user_models.User)
        self.token = G(user_models.Token, user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_comments(self):
        response = self.client.get(f"{self.COMMENTS_URL}?issueId=KD-4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), list)

    def test_post_comments(self):
        data = {
            "comment": "Hello there",
            "issue": "KD-2"
        }
        response = self.client.post(self.COMMENTS_URL, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, data)

    def test_post_comments_with_invalid_issue(self):
        data = {
            "comment": "Hello there",
            "issue": "KD-267"
        }
        expected_data = [
            "Issue does not exist or you do not have permission to see it."
        ]
        response = self.client.post(self.COMMENTS_URL, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertListEqual(expected_data, response.data)

    def test_post_comments_with_invalid_comment(self):
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
